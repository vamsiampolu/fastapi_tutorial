from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
import fake_items

from app.routers import (
    cars_router,
    files_router,
    items_router,
    logistics_router,
    models_router,
    unicorn_router,
    users_router,
)

from .unicorn_exception import UnicornException

app = FastAPI(title="Python FastAPI Tutorial")


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/offers/{offer_id}")
async def get_offer(offer_id: str):
    return fake_items.create_offer(offer_id)


@app.get("/keyword-weights", response_model=dict[str, float])
def get_keyword_weights():
    return fake_items.keyword_weights


# Login Endpoint:
@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}


app.include_router(items_router, tags=["items"])
app.include_router(users_router, tags=["users"])
app.include_router(logistics_router, tags=["logistics"])
app.include_router(cars_router, tags=["cars"])
app.include_router(files_router, tags=["files"])
app.include_router(models_router, tags=["models"])
app.include_router(unicorn_router, tags=["unicorn"])
