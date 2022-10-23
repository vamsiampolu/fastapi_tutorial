from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class User(BaseModel):
    username: str
    full_name: str


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass  # pass is a keyword in python for future code, it is a no-op but no error occurs


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print(user_in_db)
    print("User saved...not really")
    return user_in_db
