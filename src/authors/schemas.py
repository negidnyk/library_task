from pydantic import BaseModel, Field, PastDate


class Author(BaseModel):
    name: str
    birthdate: PastDate


class AuthorInfo(Author):
    id: int

    class Config:
        from_attributes = True


class AuthorAdd(Author):

    class Config:
        from_attributes = True


