from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from database import Base
from datetime import date, datetime, time, timedelta


class AuthorsModel(Base):
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    birthdate: Mapped[date] = mapped_column(default=datetime.date)
