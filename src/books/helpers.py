from src.auth.models import UserModel
from src.auth.schemas import UserInBorrowHistory
from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert


async def get_user(user_id, session):
    try:
        query = select(UserModel).where(UserModel.id == user_id)
        user = await session.execute(query)
        result = user.scalar_one_or_none()

        return UserInBorrowHistory(id=result.id, email=result.email, username=result.username)

    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Something went wrong get_user for borrow history helper. Details:\n{e}")

