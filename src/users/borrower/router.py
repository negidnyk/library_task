from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.auth.base_config import fastapi_users
from src.users.borrower.services import UserCrud
from src.auth.schemas import UserUpdate
from src.auth.models import User


router = APIRouter(
    prefix="/borrowers",
    tags=["Borrowers"]
)


current_active_user = fastapi_users.current_user(active=True)


@router.post("/borrow/", status_code=200)
async def get_me(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    return await UserCrud.get_my_profile(session, user)


@router.patch("/return/", status_code=201)
async def complete_profile(profile: UserUpdate, session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_active_user)):
    return await UserCrud.change_profile(profile, session, user)


@router.patch("/update_me/", status_code=201)
async def update_my_profile(profile: UserUpdate, session: AsyncSession = Depends(get_async_session),
                            user: User = Depends(current_active_user)):
    return await UserCrud.change_profile(profile, session, user)


@router.get("/{user_id}/", status_code=200)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    return await UserCrud.get_single_user(session, user_id, user)


@router.delete("/delete_me/", status_code=201)
async def delete_profile(session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    return await UserCrud.remove_profile(session, user)
