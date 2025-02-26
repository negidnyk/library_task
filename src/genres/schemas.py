from pydantic import BaseModel, Field


class Genre(BaseModel):
    name: str = Field(min_length=1,
                      max_length=100,
                      description="Length of name should be more than 0 and less than 100 chars")


class GenreInfo(Genre):
    id: int

    class Config:
        from_attributes = True


class GenreAdd(Genre):

    class Config:
        from_attributes = True