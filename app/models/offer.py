from pydantic import BaseModel

from .item import Item


class Offer(BaseModel):
    id: str
    name: str
    description: str | None = None
    price: float
    items: list[Item]
