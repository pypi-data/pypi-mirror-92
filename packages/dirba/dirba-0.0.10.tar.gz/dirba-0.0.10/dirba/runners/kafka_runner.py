import json
import logging
import uuid
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
from asyncio.events import AbstractEventLoop
from typing import Type, Any, NamedTuple, Optional, Union, List, Tuple
from uuid import UUID

import aiohttp
import aiomisc
import asyncio

import pydantic
import orjson
from pydantic import ValidationError
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from dirba.models.abc import AbstractModel, Predict, Author


class KafkaConfig(NamedTuple):
    input_topic: str
    output_topic: str
    group_id: Optional[str]
    bootstrap_servers: Union[List[str], str]


class AbstractKafkaRunner(ABC):

    def __init__(self, model: AbstractModel, connection_config: KafkaConfig, loop: Optional[AbstractEventLoop], from_topic_begin=False):
        self.from_topic_begin = from_topic_begin
        self.model = model
        self.kafka_config = connection_config
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self.consumer = self.create_consumer()
        self.producer = self.create_producer()

        self.logger = logging.getLogger(self.__class__.__name__)

    def create_consumer(self) -> AIOKafkaConsumer:
        return AIOKafkaConsumer(self.kafka_config.input_topic,
                                loop=self.loop, bootstrap_servers=self.kafka_config.bootstrap_servers,
                                group_id=self.kafka_config.group_id,
                                value_deserializer=orjson.loads,
                                auto_offset_reset="earliest" if self.from_topic_begin else 'latest',
                                auto_commit_interval_ms=1000)

    def create_producer(self):
        return AIOKafkaProducer(client_id=self.kafka_config.group_id,
                                loop=self.loop, bootstrap_servers=self.kafka_config.bootstrap_servers,
                                value_serializer=orjson.dumps)

    async def run(self):
        """
        Запускает consumer кафки для сохранения материалов
        """
        await self.consumer.start()
        await self.producer.start()
        self.logger.info(f'Start consuming {self.kafka_config.input_topic}')

        try:
            async for msg in self.consumer:
                try:
                    self.logger.info(' '.join(map(str, ["consumed: ", msg.topic, msg.partition, msg.offset,
                                                        msg.key, msg.value, msg.timestamp])))

                    record = self.InputModel(**msg.value)

                    if not self.is_adorable(record):
                        continue

                    feature = await self.extract_model_feature(record)

                    model_result = await self.model.async_call(feature)
                    self.logger.info(f'model produced {model_result}')
                    for predict in model_result:
                        packed_result = self.pack(record, predict)
                        if packed_result is None:
                            continue
                        self.logger.info(f'packed {packed_result}')

                        await self.producer.send(self.kafka_config.output_topic, packed_result.dict())
                except ValidationError:
                    self.logger.info(f'Unable to parse message {msg.value}')
                    await asyncio.sleep(0.5)
                except Exception as e:
                    self.logger.error(f'Error processing {e}', exc_info=True)
                    await asyncio.sleep(0.5)
        finally:
            await self.consumer.stop()

    # TODO check output type
    @abstractmethod
    def pack(self, input_message: 'InputModel', model_result: Predict) -> Optional[pydantic.BaseModel]:
        """
        Функция для упаковки сообщения полученного от топика и результата работы модели в новое сообщение.

        Если функция возвращает `None`, то сообщение не будет отправлено
        :param input_message: входящее сообщение
        """
        pass

    @abstractmethod
    def is_adorable(self, input_message: 'InputModel') -> bool:
        """
        Проверка сообщения на применимость данной модели к нему
        :param input_message: входящее сообщение
        :return: True если сообщение должно быть обработано, иначе False
        """
        pass

    @abstractmethod
    async def extract_model_feature(self, input_message: 'InputModel') -> dict:
        """
        Выделяет из сообщения информацию для запуска модели
        :param input_message:
        :return:
        """
        pass

    @property
    @abstractmethod
    def InputModel(self) -> Type[pydantic.BaseModel]:
        """
        Класс для сообщений, получаемых из kafka
        """
        pass

    @property
    @abstractmethod
    def OutputModel(self) -> Type[pydantic.BaseModel]:
        """
        Класс для сообщений, создаваемых после обработки моделью
        """
        pass


class LoaderMessage(pydantic.BaseModel):
    uid_query: UUID
    query_id: int
    driver_id: int
    category_id: int
    type_id: int
    uid_search: UUID
    uid_filter_link: UUID
    uid_loader: UUID
    uid_loaded_data: UUID
    author: Author
    type_content: str
    result: int


class ModelOutput(pydantic.BaseModel):
    category: int
    estimate: float


class AnalysisResult(pydantic.BaseModel):
    type_content: str
    content_ref: int
    model: ModelOutput


class AnalysisMessage(pydantic.BaseModel):
    uid_query: UUID
    query_id: int
    driver_id: int
    category_id: int
    type_id: int
    uid_search: UUID
    uid_filter_link: UUID
    uid_loader: UUID
    uid_loaded_data: UUID
    uid_analysis: UUID
    author: Author
    result: AnalysisResult


class TextKafkaRunner(AbstractKafkaRunner):
    """
    Класс для работы с текстовыми данными в kafka
    """

    def __init__(self, model: AbstractModel, connection_config: KafkaConfig, loop: AbstractEventLoop, data_api_url: str,
                 from_topic_begin=True):
        super().__init__(model, connection_config, loop, from_topic_begin=from_topic_begin)
        self.data_api_url = data_api_url

    def is_adorable(self, input_message: 'InputModel') -> bool:
        return input_message.type_content == 'text'

    def pack(self, input_message: 'InputModel', predict: Predict) -> 'OutputModel':
        if predict.score == 0:
            self.logger.info('Skipping predict with null score')
            return None
        model_output = ModelOutput(category=predict.category, estimate=predict.score)
        analysis_result = AnalysisResult(type_content='text', content_ref=input_message.result, model=model_output)
        message = self.OutputModel(uid_query=input_message.uid_query, uid_analysis=uuid.uuid4(),
                                   author=self.model.author(), uid_filter_link=input_message.uid_filter_link,
                                   uid_loaded_data=input_message.uid_loaded_data, uid_loader=input_message.uid_loader,
                                   uid_search=input_message.uid_search,
                                   query_id=input_message.query_id, driver_id=input_message.driver_id,
                                   category_id=input_message.category_id, type_id=input_message.type_id,
                                   result=analysis_result)

        return message

    async def extract_model_feature(self, input_message: 'InputModel') -> dict:
        text_url, text = await self.get_text(input_message.result)
        return {'text': text}

    @property
    def InputModel(self) -> Type[LoaderMessage]:
        return LoaderMessage

    @property
    def OutputModel(self) -> Type[AnalysisMessage]:
        return AnalysisMessage

    TEXT = str
    TEXT_URL = str

    @aiomisc.asyncbackoff(10, 30, 0.1)
    async def get_text(self, text_id: int) -> Tuple[TEXT_URL, TEXT]:
        """
        Метод получения url текста и самого текста.
        :param text_id:
        :type text_id: int
        :param api_path: расположение API (url)
        :type api_path: str
        :return: url текста, сам текст
        :rtype: tuple[str, str]
        """
        async with aiohttp.ClientSession() as session:
            text_url = self.data_api_url + str(text_id)
            response = await session.get(text_url)

            if response.status != 200:
                raise ConnectionError(f"Error via connection with data api")

            data = await response.json()
            text = data["content"]

            return text_url, text
