from typing import List, Union, Callable, Any, Type

import fastapi
import pydantic
import uvicorn

from dirba.models import AbstractModel, Predict


class AbstractInput(pydantic.BaseModel):
    content: Any


class FileModelInput(AbstractInput):
    content: bytes


class TextModelInput(pydantic.BaseModel):
    content: str


class ModelOutput(pydantic.BaseModel):
    data: Union[List[Predict]]


class APIRunner:
    def __init__(self, model: AbstractModel, host: str = 'localhost', port=5005,
                 model_input: Union[Type[AbstractInput], Type[FileModelInput]] = AbstractInput):
        self.ModelInput = model_input
        self.model = model
        self.port = port
        self.host = host
        self.app = fastapi.FastAPI()
        self.set_app_route()

    def run(self):
        uvicorn.run(self.app, host=self.host, port=self.port)

    def predict_resp(self) -> Callable:
        if self.ModelInput is FileModelInput:
            def wrapper(data: bytes = fastapi.File(...)) -> ModelOutput:
                result = self.model(data)
                response = ModelOutput(data=result)
                return response
        else:
            InputType = self.ModelInput

            def wrapper(data: InputType) -> ModelOutput:
                result = self.model(data.content)
                response = ModelOutput(data=result)
                return response

        return wrapper

    def set_app_route(self):
        self.app.add_api_route('/predict', self.predict_resp(), response_model=ModelOutput)


if __name__ == '__main__':
    runner = APIRunner('', model_input=FileModelInput)
    runner.run()
