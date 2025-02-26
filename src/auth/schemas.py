from typing import Any, List, Optional
from fastapi_users import schemas
from pydantic import BaseModel, Field


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    is_deleted: bool

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    role_id: int = Field(description="1 - Librarian, 2 - Borrower")
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    is_deleted: bool = Field(default=False)

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None


class UserInBorrowHistory(BaseModel):
    id: int
    email: str
    username: str
