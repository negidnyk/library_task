from datetime import datetime
from typing import AsyncGenerator, List
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData, BigInteger
from sqlalchemy.orm import Session, registry, declarative_base, as_declarative, declared_attr, mapped_column, Mapped, relationship
from datetime import date, datetime, time, timedelta
from database import Base


class RolesModel(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column()
    users: Mapped[List["UserModel"]] = relationship()


class UserModel(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    role: Mapped["RolesModel"] = relationship(back_populates="users")



