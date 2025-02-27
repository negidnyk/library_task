from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert, and_
from src.authors.models import AuthorsModel
from src.authors.models import AuthorsModel


async def is_name_unique(author_name, session):
    query = select(AuthorsModel).where(AuthorsModel.name == author_name)
    book = await session.execute(query)
    result = book.scalar_one_or_none()
    if result:
        raise HTTPException(status_code=400, detail="Author with such name already exists in DB")
