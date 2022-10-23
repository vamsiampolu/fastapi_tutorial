from fastapi import APIRouter
from app.unicorn_exception import UnicornException

router = APIRouter()

# Unicorn API:
@router.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
