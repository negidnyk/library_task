from typing import Any, List, Optional
from pydantic import BaseModel, Field, PastDate
from pydantic_extra_types.isbn import ISBN
from datetime import date, datetime, time, timedelta


class Book(BaseModel):
    title: str = Field(gt=0, le=100, description="Length of title should be more than 0 and less than 100 chars")
    isbn: ISBN = Field(description="(International Standard Book Number) is a numeric commercial book identifier")
    publisher_id: int
    publish_date: PastDate
    author_id: int
    genre_id: int


class BookInfo(Book):
    id: int

    class Config:
        from_attributes = True


class BookAdd(Book):

    class Config:
        from_attributes = True


