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
