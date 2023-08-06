import logging
from typing import List, Any, Dict, Tuple
from abc import abstractmethod, ABC

import pydantic


class Predict(pydantic.BaseModel):
    """
    Объект для получения оценки от модели. В зависимости от
    типа модели, данный объект может быть дополнен другими полями
    """
    score: float
    category: float


class BinaryPredict(Predict):
    """
    Бинарная оценка
    """
    score: float = pydantic.Field(..., ge=0, le=1)

# TODO batch predict support


class AbstractModel(ABC):
    """
    Абстрактный класс для любой модели машинного обучения или нейронной
    сети
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, input: Any) -> List[Predict]:
        processed = self.preprocess(input)
        return self.predict(processed)

    @abstractmethod
    def preprocess(self, features: Any) -> Any:
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
    def predict(self, features: Any) -> List[Predict]:
        """
        Метод для получения оценки модели.
        При наличии нескольких параметров, необходимых для получения оценки, они упаковываются в кортеж, но
        аргумент должен быть всегда один
        :param features: предобработанный объект
        :return: список оценок от модели
        """
        pass


CategoryDatasetName = str
CategoryName = str
CategoryId = int


class AbstractProhibitedModel(AbstractModel, ABC):
    classes: Dict[CategoryId, Tuple[CategoryName, CategoryDatasetName]] = {
        -1: ('is_legal', 'Легально'),
        25: ('is_drug', 'Наркоторговля'),
        14: ('is_extremism', 'Экстремизм'),
        15: ('is_terrorism', 'Терроризм'),
        19: ('is_porn', 'Проституция'),
        23: ('is_gaming', 'Игорная деятельность')}
