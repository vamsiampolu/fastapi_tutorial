from uuid import UUID

from fastapi import APIRouter, Body, Path, Query
from pydantic import Required

from app.models.item import Item

router = APIRouter()


@router.get("/cars/{car_name}")
async def get_car(
    car_name: str = Path(title="The name of the car"),
    q: list[str] = Query(default=["foo", "bar"]),
):
    return {"q": q, "car_name": car_name}


@router.put("/cars/{car_id}")
async def update_car(
    *,
    car_id: UUID,
    car_name: str = Query(default=Required),
    item: Item = Body(embed=True),
):
    results = {"car_id": car_id, "item": item, "car_name": car_name}
    return results
