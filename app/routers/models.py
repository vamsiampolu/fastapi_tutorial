from fastapi import APIRouter, Query
from pydantic import Required

from app.models.model import ModelName

router = APIRouter()


@router.get("/models/{model_name}")
async def get_model(
    model_name: ModelName,
    query_item: str = Query(
        default=Required, min_length=3, max_length=50, regex="^fixedquery$", alias="q"
    ),
):
    if model_name is ModelName.Alexnet:
        return {
            "model_name": model_name,
            "message": "Deep Learning FTW",
            "q": query_item,
        }
    if model_name.value == "lenet":
        return {
            "model_name": model_name,
            "message": "LeCNN all the images",
            "q": query_item,
        }
    return {"model_name": model_name, "message": "Have some residuals", "q": query_item}
