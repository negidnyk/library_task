from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert, and_
from src.genres.models import GenresModel
from src.genres.schemas import Genre, GenreAdd, GenreInfo
from src.genres.validations import is_genre_unique
from datetime import date


class GenreCrud:

    @staticmethod
    async def create_genre(genre_details, session):

        await is_genre_unique(genre_details.name.lower(), session)

        try:
            stmt = insert(GenresModel).values(name=genre_details.name.lower())
            await session.execute(stmt)
            await session.commit()

            query = select(GenresModel).where(GenresModel.name == genre_details.name.lower())
            genre = await session.execute(query)
            result = genre.scalar_one_or_none()

            return GenreInfo(id=result.id, name=result.name)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong in add genre api service. Details:\n{e}")

    @staticmethod
    async def get_all_genres(skip, limit, session):

        try:
            query = select(GenresModel).limit(limit).offset(skip)
            genre_list = await session.execute(query)
            result_list = genre_list.scalars().all()

            return [GenreInfo(id=result.id, name=result.name) for result in result_list]

        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in get all genres api service. Details:\n{e}")
