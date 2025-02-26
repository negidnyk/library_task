from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.auth.base_config import fastapi_users
from src.publishers.schemas import Publisher, PublisherAdd, PublisherInfo
from src.publishers.services import PublisherCrud
from src.auth.models import UserModel

router = APIRouter(
    prefix="/publishers",
    tags=["Publishers"]
)

current_active_user = fastapi_users.current_user(active=True)


@router.post("/add/", status_code=201)
async def add_new_publisher(publisher_details: PublisherAdd, session: AsyncSession = Depends(get_async_session),
                            user: UserModel = Depends(current_active_user)):
    return await PublisherCrud.create_publisher(publisher_details, session)


@router.get("/list/", status_code=200)
async def get_all_publishers(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session),
                             user: UserModel = Depends(current_active_user)):
    return await PublisherCrud.get_all_publishers(skip, limit, session)
