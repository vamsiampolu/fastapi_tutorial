"""A pydantic model that represents an Item in a store or offer"""

from pydantic import BaseModel, Field
from image_model import Image


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(
        gt=0, description="The price of item, must be greater than zero"
    )
    tax: float | None = Field(default=None)
    tags: set[str] = Field(default=set())
    image: Image | None = None
