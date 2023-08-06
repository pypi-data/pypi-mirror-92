import json
import logging
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
from typing import Type, Any, NamedTuple, Optional, Union, List

import pydantic
from pydantic import ValidationError

from dirba.models import AbstractModel


class AnalyzeMessage(pydantic.BaseModel):
    """
    Сообщение для топика анализа
    """
    pass


class LoaderMessage(pydantic.BaseModel):
    """
    Сообщение для топика загрузки
    """
    pass


class KafkaConfig(NamedTuple):
    topic: str
    group_id: Optional[str]
    bootstrap_servers: Union[List[str], str]


class AbstractKafkaRunner(ABC):

    def __init__(self, model: AbstractModel, connection_config: KafkaConfig, loop: AbstractEventLoop):
        self.model = model
        self.kafka_config = connection_config
        self.loop = loop
        self.consumer = self.create_consumer()

        self.logger = logging.getLogger(self.__class__.__name__)

    def create_consumer(self) -> AIOKafkaConsumer:
        return AIOKafkaConsumer(self.kafka_config.topic,
                                loop=self.loop, bootstrap_servers=self.kafka_config.bootstrap_servers,
                                group_id=self.kafka_config.group_id,
                                value_deserializer=lambda x: json.loads(x, encoding='utf-8'),
                                auto_commit_interval_ms=1000)

    def create_producer(self):
        return AIOKafkaProducer(
            loop=self.loop, bootstrap_servers=self.kafka_config.bootstrap_servers,)

    async def run(self):
        """
        Запускает consumer кафки для сохранения материалов
        """
        await self.consumer.start()
        self.logger.info('Start consuming materials')

        try:
            async for msg in self.consumer:

                try:
                    self.logger.debug(' '.join(map(str, ["consumed: ", msg.topic, msg.partition, msg.offset,
                                                         msg.key, msg.value, msg.timestamp])))

                    record = self.InputModel(**msg.value)
                    feature = self.extract_model_feature(record)
                    model_result = self.model(feature)
                    packed_result = self.pack(record, model_result)

                except ValidationError:
                    self.logger.debug(f'Unable to parse message {msg.value}')
                except Exception as e:
                    self.logger.error(f'Error due element saving {e}', exc_info=True)
        finally:
            await self.consumer.stop()

    # TODO check output type
    @staticmethod
    @abstractmethod
    def pack(input_message: 'InputModel', model_result: Any) -> pydantic.BaseModel:
        """
        Функция для упаковки сообщения полученного от топика и результата работы модели в новое сообщение
        :param input_message: входящее сообщение
        :param model_result: результат работы модели
        :return:
        """
        pass

    @staticmethod
    @abstractmethod
    def extract_model_feature(input_message: 'InputModel') -> Any:
        """
        Выделяет из сообщения информацию для запуска модели
        :param input_message:
        :return:
        """
        pass

    @property
    @abstractmethod
    def InputModel(self) -> Type[pydantic.BaseModel]:
        pass

    @property
    @abstractmethod
    def OutputModel(self) -> Type[pydantic.BaseModel]:
        pass
