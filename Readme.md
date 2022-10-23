To install poetry:

```shell
$ brew install poetry
```

To install poe, a task runner for poetry:

* First, install pipx

```shell
$ brew install pipx
$ pipx ensurepath
```

* Install poe with pipx to make sure it is globally available:

```shell
$ pipx install poethepoet
```

---

**Setting up the project from scratch**

Setup poetry inside the project directory:

```shell
$ poetry init
```

follow the interactive prompts


To install fastapi and uvicorn:

```
$ poetry add "fastapi[all]"
$ poetry ad "uvicorn[standard]"
```

The `zsh` shell treats `[]` as special characters, using double quotes prevents this from happening.

---

Create a script to run `main.py` using poe:

```toml
[tool.poe.tasks]
dev = "uvicorn main:app --reload"
```

Run the server:

```shell
$ poe dev
```

The app comes with [swagger docs](http://localhost:8000/docs) and [redoc](http://localhost:8000/redoc). The raw schema is available at [openapi.json](http://localhost:8000/openapi.json)

---

Routes are read in order, we cannot redefine a route or define a parameterized route before a static route.

By specifying parameter types, we can automatically get fastapi to validate the type of the param

FastAPI uses Pydantic under the hood to perform validations.

---

Any parameter not declared as a path parameter in the function definition is considered a path parameter (and represented as such with the appropriate types in the openapi schema).

Optional parameters are initialized to None.

To setup a route with optional params:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("items/{item_id}")
async def read_item(item_id: int, q: String | None = None):
  if q:
      return {"item_id": item_id, "q": q}
  return {"item_id": item_id}
```

Boolean query params can be represented in the url as `1 | 0`, `true | false`, `on | off`, `True | False` and `yes | no`.

FastAPI uses a Pydantic model as the request body, it recognizes a path parameter declared in the decorator and treats all other params as query params.

We can add additional validation for query parameters called `Query`

---

Use `*` as the first parameter when defining `Path` and `Query` to use with the function params.

This sets the rest of the params as `kwargs` even if they don't have a deafault value

---

Use multiple body parameters or an embedded body parameter inside the body.

Validate individual fields inside the body using a `Field` from pydantic

A Pydantic model can also have nested types for fields to represent complex data

Pydantic also supports some exotic types such as HttpUrl and deeply nested models.

---

**Open API Examples**

* Provide extra config using `Config` and `schema_extra`

```python
from pydantic import BaseModel, Field
from image_model import Image

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(
        gt=0, description="The price of item, must be greater than zero"
    )
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice item",
                "price": 35.4,
                "tax": 3.2,
            }
        }
```

* Setting up an example at the field level

```python
from pydantic import BaseModel, Field
from image_model import Image

class Item(BaseModel):
    name: str = Field(example="Foo")
    description: str | None = Field(
        default=None,
        title="The description of the item",
        max_length=300,
        example="A very nice item",
    )
    price: float = Field(
        gt=0, description="The price of item, must be greater than zero", example=35.4
    )
    tax: float | None = Field(default=None, example=3.2)
    tags: set[str] = Field(
        default=set(), example={"electronics", "accessories", "audio"}
    )
    image: Image | None = None
```

* Adding multiple examples to the `Body` of a request:

```python
from fastapi import FastAPI, Body

app = FastAPI()

@app.post("/items")
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
```

The `examples` is part of the json schema of the pydantic model, `example` is defined by `openapi` which relies on an older version of json schema

pydantic and fastapi work it out such that we can use the examples also end up in the appropriate place in the openapi spec and the json schema

---

We can also use `Cookie` and `Header`, when reading headers, we can use `snake_case` without worrying that the headers are kebab case.

Also, we can receive multiple values for a header using `list[str]`

---

Pydantic will filter out data from an input model that must not be a part of the output model:

```python
from pydantic import BaseModel
from FastAPI import FastAPI

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

app = FastAPI()

@app.post("/users", response_model=UserOut)
async def create_user(user: UserIn):
  return user
```

---

We can configure what gets shown in the response:

* `response_model_exclude_unset`: this excludes any values that have not been set in the `response_model`. this will not include any `default` values in the response

* we can use `response_model_exclude_defaults`, `response_model_exclude_None`. We can also use `response_model_include` and `response_model_exclude` from the response.

---

Unwrapping a Pydantic Model:

Every pydantic model has a `dict()` which would convert the model into a dict.

```python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")

user_in.dict() 
"""
{
  'username': 'john',
  'password': 'secret',
  'email': 'john.doe@example.com',
  'full_name': None,
}
"""
```

`UserInDB(**user_in.dict())` pass the keys and values of the dict as key value arguments.

It is the same as:

```python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

We can pass additional arguments using `UserInDB(**user_in.dict(), hashed_password=hashed_password)`

To setup models with reuse:

```python
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass  # pass is a keyword in python for future code, it is a no-op but no error occurs


class UserInDB(UserBase):
    hashed_password: str

```

To respond with one or two models:

```python
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI

class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"

app = FastAPI()

@app.get("/items/{item_id}", response_model=Union[CarItem, PlaneItem])
async def get_item_by_id(item_id: str):
    return items[item_id]
```

When passing a Union as an argument instead of a type annotation, we must use `Union[A, B]` instead of `A | B`

---

We can specify `status_code` to be sent for a successful response

```python
from fastapi import FastAPI, status
from item_model import Item

app = FastAPI()

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item)
  return item
```

---

We can receive `form-data` from the client using:

```python
from fastapi import FastAPI, File

app = FastAPI()

@app.post('/files/')
async def create_file(file: bytes = File()):
  return {"file_size": len(file)}
```

---

There are two ways of handling form-data:

`Form()` represents data from a form that is non binary and `File()` and `UploadFile()` represents
data that is binary.

---

When we want to send the user a Http exception, we use:

```python
from fastapi import FastAPI, HTTPException, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: str = Path(description="The id of an item")):
    if item_id in db:
        raise HTTPException(status_code=404, detail={"message": "Item not found", "success": "no"})
      
    return db.findById(item_id)
```

We can pass a string or something that can be serialized to Json.

---

Handling exceptions:

* create a custom exception:

```python
class UnicornException(Exception):
    def __init__(self, name: str):
        this.name = name
```

* add an exception handler:

```python
from fastpai import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):

    return JSONResponse(status_code=418, content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."})
```

---

FastAPI has some default exception handlers, if a request has invalid data, it raises a `RequestValidationError`.

---

Partially updating a pydantic model immutably:

```python
stored_item_model.copy(update=update_data)
```

We can use this with the `PATCH` HTTP method for partial updates on data

---

A project with multiple files:

```
app
|__  __init__.py
|__  main.py
|__ dependencies.py
|__ routers
|  |__ __init__.py
|  |__ items.py
|  |__ users.py
|
|__internal
   |__ __init__.py
   |__ main.py

```

---

Run multiple tasks in series with poe:

```toml
[tools.poe.tasks]
format_code = "black app"
format_imports = "isort app"
format.sequence = ["format_code", "format_imports"]
```

---


The `__init__.py` turns a directory into a `package` from which we may import.

Anything imported into `__init__.py` can be imported from the package directly.
