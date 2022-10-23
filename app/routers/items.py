import fake_items as fake_items
from fastapi import (APIRouter, Body, Cookie, Header, HTTPException, Path,
                     Query, status)

from app.models.item import Item

router = APIRouter()


@router.get("/items")
async def read_items_paginated(
    skip: int = 0,
    limit: int = 10,
    ads_id: str | None = Cookie(default=None),
    user_agent: str | None = Header(default=None),
):
    return fake_items.fake_items_db[skip : skip + limit]


@router.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: Item = Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A *normal* item works correctly",
                "value": {
                    "name": "Foo",
                    "description": "A very nice item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price strings into actual `number` values",
                "value": {"price": "35.4", "name": "Bar"},
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {"name": "Baz", "price": "thirty five point four"},
            },
        },
    )
):
    return item


@router.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="Id of the Item", gt=1, le=125),
    item: Item = Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A *normal* item works correctly",
                "value": {
                    "name": "Foo",
                    "description": "A very nice item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price strings into actual `number` values",
                "value": {"price": "35.4", "name": "Bar"},
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {"name": "Baz", "price": "thirty five point four"},
            },
        },
    ),
    user: User,
    q: str | None = None,
    importance: int = Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A *normal* item works correctly",
                "value": 1,
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price strings into actual `number` values",
                "value": "1",
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": "one",
            },
        }
    ),
):
    result = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        result.update({"q": q})
    return result


@router.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    if not item_id in fake_items.fake_items_db2:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return fake_items.fake_items_db2[item_id]


@router.get("/items/{item_id}/public", response_model_exclude={"tax"})
async def read_item(
    item_id: int,
    q: str
    | None = Query(
        default=None,
        min_length=3,
        max_length=50,
        title="Query Str",
        description="Query string for the items to search in the database that have a good match",
        alias="item-query",
    ),
    short: bool = False,
):
    if q:
        return {"item_id": item_id, "q": q}
    if not short:
        return {"item_id": item_id, "description": "Amazing long description"}
    return {"item_id": item_id}
