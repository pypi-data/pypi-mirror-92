pip install git+http://git2.uriit.local/CIAS/dirba.git@master#egg=dirba
Мини библиотечка для уменьшения рутины связанной с моделями.

Возможности:
 - [ ] базовые классы для моделей
 - [ ] запуск моделей в kafka
 - [ ] запуск моделей в rest api
 - [ ] валидация
 
Пример использования валидации 
```python
from dirba.models.dambo import DamboModel
from dirba.runners import APIRunner
from dirba.validation import ProhibitedTexValidationDataset
from dirba.validation import PrecisionMetric
from dirba.validation import Validator

if __name__ == '__main__':
    dataset = ProhibitedTexValidationDataset()
    model = DamboModel()

    validator = Validator(dataset,model, [PrecisionMetric])
    validator.describe()

```