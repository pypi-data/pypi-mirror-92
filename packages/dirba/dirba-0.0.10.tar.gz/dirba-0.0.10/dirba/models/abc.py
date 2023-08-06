import logging
from typing import List, Any, Dict, Tuple, Union, Mapping
from abc import abstractmethod, ABC

import asyncio
import pydantic
import aiomisc

CategoryDatasetName = str
CategoryName = str
CategoryId = Union[int, str]


class Predict(pydantic.BaseModel):
    """
    Объект для получения оценки от модели. В зависимости от
    типа модели, данный объект может быть дополнен другими полями
    """
    score: float
    category: CategoryId


class BinaryPredict(Predict):
    """
    Бинарная оценка
    """
    score: int = pydantic.Field(..., ge=0, le=1)


# TODO batch predict support

class Author(pydantic.BaseModel):
    name: str
    version: str


class AbstractModel(ABC):
    """
    Абстрактный класс для любой модели машинного обучения или нейронной
    сети
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, input: Any) -> List[Predict]:
        """
        Вызов модели для получения результата
        :param input:
        :return:
        """
        processed = self.preprocess(input)
        return self.predict(processed)

    @abstractmethod
    def author(self) -> Author:
        pass

    @aiomisc.threaded_separate
    def async_call(self, input: Any) -> List[Predict]:
        return self.__call__(input)

    @abstractmethod
    def preprocess(self, features: Mapping[str, Any]) -> Any:
        """
        Обрабатывает данные для последующей отправки в модель.

        Данный метод должен содержать всю предобработку для объекта, поступившего на оценку.
        При наличии нескольких параметров, необходимых для предобработки, они упаковываются в кортеж, но
        аргумент должен быть всегда один
        :param features: объект, который необходимо обработать
        :return: объект, готовый для отправки на получение оценки
        """
        pass

    @abstractmethod
    def predict(self, features: Mapping[str, Any]) -> List[Predict]:
        """
        Метод для получения оценки модели.
        При наличии нескольких параметров, необходимых для получения оценки, они упаковываются в кортеж, но
        аргумент должен быть всегда один
        :param features: предобработанный объект
        :return: список оценок от модели
        """
        pass


class AbstractProhibitedModel(AbstractModel, ABC):
    """
    Абстрактный класс для моделей, работающих с категориями АИС ПОИСК
    """
    classes: Dict[CategoryId, Tuple[CategoryName, CategoryDatasetName]] = {
        -1: ('is_legal', 'Легально'), # виртуальная категория. Используется в обучении и валидации, но должна 
        25: ('is_drug', 'Наркоторговля'),
        14: ('is_extremism', 'Экстремизм'),
        15: ('is_terrorism', 'Терроризм'),
        19: ('is_porn', 'Проституция'),
        23: ('is_gaming', 'Игорная деятельность')}
