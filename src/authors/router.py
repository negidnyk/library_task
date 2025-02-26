from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.auth.base_config import fastapi_users
from src.authors.services import AuthorCrud
from src.authors.schemas import AuthorAdd, AuthorInfo, Author
from src.auth.models import UserModel

router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)

current_active_user = fastapi_users.current_user(active=True)


@router.post("/add/", status_code=201)
async def add_new_author(author_details: AuthorAdd, session: AsyncSession = Depends(get_async_session),
                         user: UserModel = Depends(current_active_user)):
    return await AuthorCrud.create_author(author_details, session)


@router.get("/list/", status_code=200)
async def get_all_authors(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session),
                          user: UserModel = Depends(current_active_user)):
    return await AuthorCrud.get_all_authors(skip, limit, session)


@router.get("/{author_id}/", status_code=200)
async def get_author_by_id(author_id: int, session: AsyncSession = Depends(get_async_session),
                           user: UserModel = Depends(current_active_user)):
    return await AuthorCrud.get_author_by_id(author_id, session)


@router.get("/{author_id}/books/", status_code=200)
async def get_books_by_author(author_id: int, skip: int = 0, limit: int = 10,
                              session: AsyncSession = Depends(get_async_session),
                              user: UserModel = Depends(current_active_user)):
    return await AuthorCrud.get_books_of_author(skip, limit, author_id, session)
