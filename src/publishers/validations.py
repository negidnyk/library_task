from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert, and_
from src.publishers.models import PublishersModel


async def is_publisher_unique(name, session):
    query = select(PublishersModel).where(PublishersModel.name == name.lower())
    publisher = await session.execute(query)
    result = publisher.scalar_one_or_none()
    if result:
        raise HTTPException(status_code=400, detail="Publisher with such name is already exists in DB")
