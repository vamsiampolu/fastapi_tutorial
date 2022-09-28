from fastapi import FastAPI, Path, Query, Body
from pydantic import Required
from model import ModelName
from item_model import Item
from user_model import User
from offer_model import Offer

app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items")
async def read_items_paginated(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.post("/items")
async def create_item(item: Item):
    return item


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="Id of the Item", gt=1, le=125),
    item: Item,
    user: User,
    q: str | None = None,
    importance: int = Body()
):
    result = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        result.update({"q": q})
    return result


@app.get("/items/{item_id}")
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


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: str, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "This is an amazing item that has a really long description"
            }
        )
    return item


@app.get("/models/{model_name}")
async def get_model(
    model_name: ModelName,
    q: str = Query(default=Required, min_length=3, max_length=50, regex="^fixedquery$"),
):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW", "q": q}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images", "q": q}
    return {"model_name": model_name, "message": "Have some residuals", "q": q}


@app.get("/cars/{car_name}")
async def get_car(
    car_name: str = Path(title="The name of the car"),
    q: list[str] = Query(default=["foo", "bar"]),
):
    return {"q": q, "car_name": car_name}


@app.put("/cars/{car_id}")
async def update_car(
    *,
    car_id: str,
    car_name: str = Query(default=Required),
    item: Item = Body(embed=True)
):
    results = {"car_id": car_id, "item": item, "car_name": car_name}
    return results


@app.get("/offers/{offer_id}")
async def getOffer(offer_id: str):
    return Offer(
        id=offer_id,
        name="My Offer",
        description="This is my offer",
        price=122.24,
        items=[
            Item(
                name="my item",
                price=200.125,
                tags={"electronics", "mobile", "accessories"},
            )
        ],
    )
