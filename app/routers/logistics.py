from typing import Union

from fastapi import APIRouter

from app import fake_items
from app.models.item import BaseItem, CarItem, PlaneItem

router = APIRouter()


def item_dict_to_base_item(item_dict: dict[str, str]):
    return BaseItem(**item_dict)


@router.get("/logisitics/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def get_logisitics_item(item_id: str):
    return fake_items.logisitics_items[item_id]


@router.get("/logisitics/items", response_model=list[BaseItem])
async def get_logistics_items():
    item_list = list(fake_items.logisitics_items.values())
    item_models = map(item_dict_to_base_item, item_list)
    return list(item_models)
