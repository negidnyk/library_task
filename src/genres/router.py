from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.auth.base_config import fastapi_users
from src.genres.services import GenreCrud
from src.genres.schemas import Genre, GenreInfo, GenreAdd
from src.auth.models import UserModel

router = APIRouter(
    prefix="/genres",
    tags=["Genres"]
)

current_active_user = fastapi_users.current_user(active=True)


@router.post("/add/", status_code=201)
async def add_new_genre(genre_details: GenreAdd, session: AsyncSession = Depends(get_async_session),
                       user: UserModel = Depends(current_active_user)):
    return await GenreCrud.create_genre(genre_details, session, user)


@router.get("/list/", status_code=200)
async def get_all_genres(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session),
                        user: UserModel = Depends(current_active_user)):
    return await GenreCrud.get_all_genres(skip, limit, session)

