from datetime import datetime
from typing import AsyncGenerator, List
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData, BigInteger
from sqlalchemy.orm import Session, registry, declarative_base, as_declarative, declared_attr, mapped_column, Mapped, relationship
from datetime import date, datetime, time, timedelta
from database import Base


# class Role(Base):
#     __tablename__ = "role"
#     __table_args__ = {'extend_existing': True}
#     id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
#     name = Column(String, nullable=False)
#     permissions = Column(Integer, nullable=False)
#
#
# class User(SQLAlchemyBaseUserTable[int], Base):
#     __tablename__ = "borrower"
#     __table_args__ = {'extend_existing': True}
#     id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
#     email = Column(String, nullable=False)
#     username = Column(String, nullable=False)
#     bio = Column(String(200), nullable=True)
#     avatar_id = Column(Integer, ForeignKey("files.id"), nullable=True)
#     registered_at = Column(TIMESTAMP, default=datetime.utcnow)
#     role_id = Column(Integer, ForeignKey("role.id"))
#     hashed_password = Column(String, nullable=True)
#     is_active = Column(Boolean, default=True, nullable=False)
#     is_superuser = Column(Boolean, default=False, nullable=False)
#     is_verified = Column(Boolean, default=False, nullable=False)
#     is_deleted = Column(Boolean, default=False, nullable=False)


# @as_declarative()
# class AbstractModel(SQLAlchemyBaseUserTable[int], Base):
#     id: Mapped[int] = mapped_column(primary_key=True)


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



