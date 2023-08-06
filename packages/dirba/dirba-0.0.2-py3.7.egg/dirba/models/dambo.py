from typing import Any, List, Mapping

import pydantic

from dirba.models import AbstractProhibitedModel, Predict


class DamboInput(pydantic.BaseModel):
    text: str


class DamboModel(AbstractProhibitedModel):

    def predict(self, features: Any) -> List[Predict]:
        return [Predict(score=1, category=i) for i in self.classes.keys()]

    def preprocess(self, features: Mapping[str, Any]) -> DamboInput:
        return DamboInput(text=features['text'])
