import abc
from typing import Iterable

from sklearn import metrics

FeatureClass = str
Probability = float


class AbstractMetric(abc.ABC):

    def __init__(self, features_true: Iterable, features_predicted: Iterable):
        self.features_true = features_true
        self.features_predicted = features_predicted

    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplementedError("Override property before use")

    @abc.abstractmethod
    def evaluate(self) -> float:
        """
        Подсчитывает общую метрику для всех классов в совокупности
        :return:
        """
        pass


class PrecisionMetric(AbstractMetric):

    def evaluate(self) -> float:
        return metrics.precision_score(self.features_true, self.features_predicted, average='weighted')

    @property
    def name(self):
        return 'precision'
