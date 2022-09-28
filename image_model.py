""" A pydantic model representing images of items in the store/offers"""
from pydantic import BaseModel, Field, HttpUrl


class Image(BaseModel):
    url: HttpUrl = Field(description="The url of the image")
    name: str = Field(description="Name or title of the image provided by the creater")
