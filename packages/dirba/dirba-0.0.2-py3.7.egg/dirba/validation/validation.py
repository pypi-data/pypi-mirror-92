from typing import Iterable, Type, Dict

import pydantic

from dirba.models import AbstractModel

from dirba.validation.dataset import AbstractDataset
from dirba.validation.metrics import AbstractMetric

Name = str
Metric = float


class ValidationResult(pydantic.BaseModel):
    size: int
    metrics_scores: Dict[Name, Metric]


class Validator:
    def __init__(self, dataset: AbstractDataset, model: AbstractModel, metrics_classes: Iterable[Type[AbstractMetric]]):
        self.metrics_classes = metrics_classes
        self.model = model
        self.dataset = dataset

    def produce(self) -> Dict[Name, Metric]:
        y_true = []
        y_predicted = []
        for row in self.dataset.features():
            model_result = self.model(row.x)

            max_result = max(model_result, key=lambda val: val.score)
            true_max_values = list(filter(lambda val: val.score, row.y))

            if len(true_max_values) > 1 or len(true_max_values) == 0:
                raise ValueError(f"Wrong data in dataset true values. Only 1 target category allowed, but got: {row}")
            true_max = true_max_values[0]

            predicted_category = max_result.category
            true_category = true_max.category

            y_true.append(true_category)
            y_predicted.append(predicted_category)

        results = {}
        for MetricClass in self.metrics_classes:
            metric = MetricClass(y_true, y_predicted)
            results[metric.name] = metric.evaluate()

        return results

    def result(self) -> ValidationResult:
        metrics = self.produce()
        return ValidationResult(size=self.dataset.size(), metrics_scores=metrics)

    def describe(self):
        validation_result = self.result()
        print('-------------------------------------------------------')
        print(f'Running validation on {validation_result.size} values')
        print(*[f'{name.capitalize()}: {score}' for name, score in
                validation_result.metrics_scores.items()], sep='\n')
        print('-------------------------------------------------------')
