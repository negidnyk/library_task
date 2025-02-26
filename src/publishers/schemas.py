from pydantic import BaseModel, PastDate, Field


class Publisher(BaseModel):
    name: str = Field(min_length=1,
                      max_length=100,
                      description="Length of name should be more than 0 and less than 100 chars")

    established_year: PastDate


class PublisherInfo(Publisher):
    id: int

    class Config:
        from_attributes = True


class PublisherAdd(Publisher):

    class Config:
        from_attributes = True