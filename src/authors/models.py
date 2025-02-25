from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from database import Base


class AuthorsModel(Base):
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
