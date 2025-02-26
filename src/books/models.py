from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData, BigInteger
from sqlalchemy.orm import declarative_base, as_declarative, declared_attr, mapped_column, Mapped, relationship
from datetime import date, datetime, time, timedelta
from database import Base


class BooksModel(Base):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    isbn: Mapped[str] = mapped_column(String(13), nullable=False, unique=True)
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publishers.id"), nullable=False)
    publish_date: Mapped[date] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), nullable=False)
    is_borrowed: Mapped[bool] = mapped_column(nullable=False, default=False)


class BorrowedBooks(Base):
    __tablename__ = "borrowed_books"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    borrow_date: Mapped[date] = mapped_column(nullable=False, default=datetime.today())
    return_date: Mapped[date] = mapped_column(nullable=True)





