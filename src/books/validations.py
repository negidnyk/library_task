from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert, and_
from src.books.models import BooksModel, BorrowedBooks
from src.authors.models import AuthorsModel
from src.books.schemas import Book, BookAdd, BookInfo


async def is_isbn_unique(isbn, session):
    query = select(BooksModel).where(BooksModel.isbn == isbn)
    book = await session.execute(query)
    result = book.scalar_one_or_none()
    if result:
        raise HTTPException(status_code=400, detail="Book with such ISBN already exists in DB")


async def is_author_exists_in_db(author_id, session):
    query = select(AuthorsModel).where(AuthorsModel.id == author_id)
    author = await session.execute(query)
    result = author.scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=400, detail="Submitted author does not exist in DB")


async def is_book_borrowed(book_id, session):
    query = select(BooksModel).where(BooksModel.id == book_id)
    book = await session.execute(query)
    result = book.scalar_one_or_none()
    if result.is_borrowed:
        raise HTTPException(status_code=400, detail="Book with such id is already borrowed")


async def is_book_not_borrowed(book_id, session):
    query = select(BooksModel).where(BooksModel.id == book_id)
    book = await session.execute(query)
    result = book.scalar_one_or_none()
    if not result.is_borrowed:
        raise HTTPException(status_code=400, detail="Book with such id is not borrowed")


async def is_borrower(book_id, session, user):
    query = select(BorrowedBooks).filter(and_(BorrowedBooks.book_id == book_id,
                                              BorrowedBooks.user_id == user.id,
                                              BorrowedBooks.return_date.is_(None)))

    borrowed_book = await session.execute(query)
    result = borrowed_book.scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=400, detail="Given user did not borrow a book with submitted id")


async def is_book_exist(book_id, session):
    query = select(BooksModel).where(BooksModel.id == book_id)
    book = await session.execute(query)
    result = book.scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=404, detail="Book with such id does not exist")

# async def is_borrow_history_empty(book_id, session):
#     query = select(BorrowedBooks).where(BorrowedBooks.book_id == book_id)
#     borrowed_book = await session.execute(query)
#     result = borrowed_book.scalar_one_or_none()
#     if not result:
#         raise HTTPException(status_code=400, detail="Given book`s history ")
