import json

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class Unicorn(BaseModel):
    name: str
    color: str


def pydantic_model_to_json(data):
    return json.dumps(jsonable_encoder(data))


unicorn = Unicorn(name="yolo", color="fuschia")
unicorn_json = pydantic_model_to_json(unicorn)
print(unicorn_json)
