from fastapi import APIRouter

from app.models.user import UserIn, UserOut, fake_save_user

router = APIRouter()


@router.get("/users/me")
async def read_user_me():
    return {"user_id": "current user"}


@router.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@router.get("/users/{user_id}/items/{item_id}")
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


@router.post("/users", response_model=UserOut)
async def create_user(user: UserIn):
    user_saved = fake_save_user(user)
    return user_saved
