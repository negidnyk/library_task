from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert
from src.authors.models import AuthorsModel
from src.books.models import BooksModel
from src.books.schemas import Book, BookAdd, BookInfo
from src.authors.schemas import Author, AuthorInfo, AuthorAdd
from src.validations.validations import validate_int_id
from src.users.librarian.validations import is_librarian


class AuthorCrud:
    @staticmethod
    async def create_author(author_details, session, user):

        await is_librarian(user.id)

        try:
            stmt = insert(AuthorsModel).values(name=author_details.name, birthdate=author_details.birthdate)
            await session.execute(stmt)
            await session.commit()

            query = select(AuthorsModel).where(AuthorsModel.name == author_details.name)
            last_created_author= await session.execute(query)
            result = last_created_author.scalar_one_or_none()

            return AuthorInfo(id=result.id, name=result.name, birthdate=result.birthdate)

        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in add author api service. Details:\n{e}")

    @staticmethod
    async def get_all_authors(skip, limit, session):

        try:
            query = select(AuthorsModel).limit(limit).offset(skip)
            authors_list = await session.execute(query)
            result_list = authors_list.scalars().all()
            return [AuthorInfo(id=author.id, name=author.name, birthdate=author.birthdate) for author in result_list]

        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in get all authors api service. Details:\n{e}")

    @staticmethod
    async def get_author_by_id(author_id, session):

        await validate_int_id(author_id)

        try:
            query = select(AuthorsModel).where(AuthorsModel.id == author_id)
            author = await session.execute(query)
            result = author.scalar_one_or_none()

        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in get author by id api service. Details:\n{e}")

        if not result:
            raise HTTPException(status_code=404, detail="Author with submitted id is not found")

        else:
            return AuthorInfo(id=result.id, name=result.name, birthdate=result.birthdate)

    @staticmethod
    async def get_books_of_author(skip, limit, author_id, session):

        await validate_int_id(author_id)

        try:
            query = select(BooksModel).limit(limit).offset(skip).where(BooksModel.author_id == author_id)
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
                                detail=f"Something went wrong in get all books by author api service. Details:\n{e}")