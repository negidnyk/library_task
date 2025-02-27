from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert, and_
from src.books.models import BooksModel, BorrowedBooks
from src.books.schemas import Book, BookAdd, BookInfo, BookBorrowHistory
from src.books.validations import is_isbn_unique, is_author_exists_in_db, is_book_borrowed, is_book_not_borrowed, \
    is_borrower, is_book_exist, is_genre_exists_in_db, is_publisher_exists_in_db
from src.books.helpers import get_user
from src.validations.validations import validate_int_id
from src.users.borrower.validations import is_borrower
from src.users.librarian.validations import is_librarian
from datetime import date


class BookCrud:
    @staticmethod
    async def create_book(book_details, session, user):

        await is_isbn_unique(book_details.isbn, session)
        await is_author_exists_in_db(book_details.author_id, session)
        await is_genre_exists_in_db(book_details.genre_id, session)
        await is_publisher_exists_in_db(book_details.publisher_id, session)

        try:
            stmt = insert(BooksModel).values(title=book_details.title,
                                             isbn=book_details.isbn,
                                             publisher_id=book_details.publisher_id,
                                             publish_date=book_details.publish_date,
                                             author_id=book_details.author_id,
                                             genre_id=book_details.genre_id)
            await session.execute(stmt)
            await session.commit()

            query = select(BooksModel).where(BooksModel.isbn == book_details.isbn)
            last_created_book = await session.execute(query)
            result = last_created_book.scalar_one_or_none()

            return BookInfo(id=result.id,
                            title=result.title,
                            isbn=result.isbn,
                            publisher_id=result.publisher_id,
                            publish_date=result.publish_date,
                            author_id=result.author_id,
                            genre_id=result.genre_id,
                            is_borrowed=result.is_borrowed)

        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in add book api service. Details:\n{e}")

    @staticmethod
    async def get_all_books(skip, limit, session, sort_by, order):

        if sort_by == "title" and order == "asc":

            try:
                query = select(BooksModel).limit(limit).offset(skip).order_by(BooksModel.title.asc())
                books_list = await session.execute(query)
                result_list = books_list.scalars().all()
                return [BookInfo(id=book.id,
                                 title=book.title,
                                 isbn=book.isbn,
                                 publisher_id=book.publisher_id,
                                 publish_date=book.publish_date,
                                 author_id=book.author_id,
                                 genre_id=book.genre_id,
                                 is_borrowed=book.is_borrowed) for book in result_list]

            except Exception as e:
                raise HTTPException(status_code=500,
                                    detail=f"Something went wrong in get all books api service. Details:\n{e}")

        if sort_by == "title" and order == "desc":

            try:
                query = select(BooksModel).limit(limit).offset(skip).order_by(BooksModel.title.desc())
                books_list = await session.execute(query)
                result_list = books_list.scalars().all()
                return [BookInfo(id=book.id,
                                 title=book.title,
                                 isbn=book.isbn,
                                 publisher_id=book.publisher_id,
                                 publish_date=book.publish_date,
                                 author_id=book.author_id,
                                 genre_id=book.genre_id,
                                 is_borrowed=book.is_borrowed) for book in result_list]

            except Exception as e:
                raise HTTPException(status_code=500,
                                    detail=f"Something went wrong in get all books api service. Details:\n{e}")

        if sort_by == "publish_date" and order == "asc":

            try:
                query = select(BooksModel).limit(limit).offset(skip).order_by(BooksModel.publish_date.asc())
                books_list = await session.execute(query)
                result_list = books_list.scalars().all()
                return [BookInfo(id=book.id,
                                 title=book.title,
                                 isbn=book.isbn,
                                 publisher_id=book.publisher_id,
                                 publish_date=book.publish_date,
                                 author_id=book.author_id,
                                 genre_id=book.genre_id,
                                 is_borrowed=book.is_borrowed) for book in result_list]

            except Exception as e:
                raise HTTPException(status_code=500,
                                    detail=f"Something went wrong in get all books api service. Details:\n{e}")

        if sort_by == "publish_date" and order == "desc":

            try:
                query = select(BooksModel).limit(limit).offset(skip).order_by(BooksModel.publish_date.desc())
                books_list = await session.execute(query)
                result_list = books_list.scalars().all()
                return [BookInfo(id=book.id,
                                 title=book.title,
                                 isbn=book.isbn,
                                 publisher_id=book.publisher_id,
                                 publish_date=book.publish_date,
                                 author_id=book.author_id,
                                 genre_id=book.genre_id,
                                 is_borrowed=book.is_borrowed) for book in result_list]

            except Exception as e:
                raise HTTPException(status_code=500,
                                    detail=f"Something went wrong in get all books api service. Details:\n{e}")

    @staticmethod
    async def get_book_by_id(book_id, session):

        await validate_int_id(book_id)

        try:
            query = select(BooksModel).where(BooksModel.id == book_id)
            author = await session.execute(query)
            result = author.scalar_one_or_none()

        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in get book by id api service. Details:\n{e}")

        if not result:
            raise HTTPException(status_code=404, detail="Book with submitted id is not found")

        else:
            return BookInfo(id=result.id,
                            title=result.title,
                            isbn=result.isbn,
                            publisher_id=result.publisher_id,
                            publish_date=result.publish_date,
                            author_id=result.author_id,
                            genre_id=result.genre_id,
                            is_borrowed=result.is_borrowed)

    @staticmethod
    async def borrow_book(book_id, session, user):

        await is_borrower(user.id)
        await validate_int_id(book_id)
        await is_book_exist(book_id, session)
        await is_book_borrowed(book_id, session)

        try:
            stmt = update(BooksModel).where(BooksModel.id == book_id).values(is_borrowed=True)
            await session.execute(stmt)
            await session.commit()

            stmt2 = insert(BorrowedBooks).values(book_id=book_id, user_id=user.id)
            await session.execute(stmt2)
            await session.commit()

            query = select(BooksModel).where(BooksModel.id == book_id)
            borrowed_book = await session.execute(query)
            result = borrowed_book.scalar_one_or_none()

            return BookInfo(id=result.id,
                            title=result.title,
                            isbn=result.isbn,
                            publisher_id=result.publisher_id,
                            publish_date=result.publish_date,
                            author_id=result.author_id,
                            genre_id=result.genre_id,
                            is_borrowed=result.is_borrowed)

        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in add author api service. Details:\n{e}")

    @staticmethod
    async def return_book(book_id, session, user):

        await is_borrower(user.id)
        await validate_int_id(book_id)
        await is_book_exist(book_id, session)
        await is_book_not_borrowed(book_id, session)
        await is_borrower(book_id, session, user)

        try:
            stmt = update(BooksModel).where(BooksModel.id == book_id).values(is_borrowed=False)
            await session.execute(stmt)
            await session.commit()

            stmt2 = update(BorrowedBooks).\
                filter(and_(BorrowedBooks.book_id == book_id,
                            BorrowedBooks.user_id == user.id,
                            BorrowedBooks.return_date.is_(None))).values(return_date=date.today())
            await session.execute(stmt2)
            await session.commit()

            query = select(BooksModel).where(BooksModel.id == book_id)
            borrowed_book = await session.execute(query)
            result = borrowed_book.scalar_one_or_none()

            return BookInfo(id=result.id,
                            title=result.title,
                            isbn=result.isbn,
                            publisher_id=result.publisher_id,
                            publish_date=result.publish_date,
                            author_id=result.author_id,
                            genre_id=result.genre_id,
                            is_borrowed=result.is_borrowed)

        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in add author api service. Details:\n{e}")

    @staticmethod
    async def get_book_borrowing_history(book_id, session, user):

        await is_librarian(user.id)
        await validate_int_id(book_id)
        await is_book_exist(book_id, session)

        try:
            query = select(BorrowedBooks).where(BorrowedBooks.book_id == book_id)
            borrowed_books = await session.execute(query)
            result_list = borrowed_books.scalars().all()

            return [BookBorrowHistory(id=result.id,
                                      user=await get_user(result.user_id, session),
                                      borrow_date=result.borrow_date,
                                      return_date=result.return_date) for result in result_list]

        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in get borrowing history api service. Details:\n{e}")

    @staticmethod
    async def delete_book(book_id, session, user):

        await is_librarian(user.id)
        await validate_int_id(book_id)
        await is_book_exist(book_id, session)
        await is_book_borrowed(book_id, session)
        #добавить првоерку на юзера

        try:
            stmt = delete(BooksModel).where(BooksModel.id == book_id)
            await session.execute(stmt)
            await session.commit()

        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in delete book api service. Details:\n{e}")
