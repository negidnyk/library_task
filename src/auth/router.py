from fastapi import APIRouter, Depends
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate


router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/jwt",
    tags=["Auth"],
)