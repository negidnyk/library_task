from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from database import Base
from datetime import date


class PublishersModel(Base):
    __tablename__ = 'publishers'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    established_year: Mapped[date] = mapped_column(nullable=False)
