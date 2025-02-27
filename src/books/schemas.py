from typing import Any, List, Optional
from pydantic import BaseModel, Field, PastDate
from enum import Enum
from pydantic_extra_types.isbn import ISBN
from datetime import date, datetime, time, timedelta
from src.auth.schemas import UserInBorrowHistory


class Book(BaseModel):
    title: str = Field(min_length=1,
                       max_length=100,
                       description="Length of title should be more than 0 and less than 100 chars")
    isbn: ISBN = Field(description="(International Standard Book Number) is a numeric commercial book identifier")
    publisher_id: int
    publish_date: PastDate
    author_id: int
    genre_id: int


class BookInfo(Book):
    id: int
    is_borrowed: bool

    class Config:
        from_attributes = True


class BookAdd(Book):

    class Config:
        from_attributes = True


class BookBorrowHistory(BaseModel):
    id: int
    user: UserInBorrowHistory
    borrow_date: date
    return_date: date


class BookSortBy(str, Enum):
    title = "title"
    publish_date = "publish_date"


class BookSortDirections(str, Enum):
    asc = "asc"
    desc = "desc"
