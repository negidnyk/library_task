from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from database import Base


class GenresModel(Base):
    __tablename__ = 'genres'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
