from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert, and_
from src.genres.models import GenresModel


async def is_genre_unique(name, session):
    query = select(GenresModel).where(GenresModel.name == name.lower())
    genre = await session.execute(query)
    result = genre.scalar_one_or_none()
    if result:
        raise HTTPException(status_code=400, detail="Genre with such genre is already exists in DB")
