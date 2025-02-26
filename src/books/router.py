from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.auth.base_config import fastapi_users
from src.books.services import BookCrud
from src.books.schemas import Book, BookAdd, BookInfo
from src.auth.models import UserModel

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

current_active_user = fastapi_users.current_user(active=True)


@router.post("/add/", status_code=201)
async def add_new_book(book_details: BookAdd, session: AsyncSession = Depends(get_async_session),
                       user: UserModel = Depends(current_active_user)):
    return await BookCrud.create_book(book_details, session)


@router.get("/list/", status_code=200)
async def get_all_books(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session),
                        user: UserModel = Depends(current_active_user)):
    return await BookCrud.get_all_books(skip, limit, session)


@router.get("/{book_id}/", status_code=200)
async def get_book_by_id(book_id: int, session: AsyncSession = Depends(get_async_session),
                         user: UserModel = Depends(current_active_user)):
    return await BookCrud.get_book_by_id(book_id, session)


@router.post("/borrow/{book_id}/", status_code=201)
async def borrow_book(book_id: int, session: AsyncSession = Depends(get_async_session),
                      user: UserModel = Depends(current_active_user)):
    return await BookCrud.borrow_book(book_id, session, user)


@router.post("/return/{book_id}/", status_code=201)
async def return_book(book_id: int, session: AsyncSession = Depends(get_async_session),
                      user: UserModel = Depends(current_active_user)):
    return await BookCrud.return_book(book_id, session, user)


@router.get("/{book_id}/history/", status_code=200)
async def get_book_borrow_history(book_id: int, session: AsyncSession = Depends(get_async_session),
                                  user: UserModel = Depends(current_active_user)):
    return await BookCrud.get_book_borrowing_history(book_id, session)
