from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert
from src.auth.models import UserModel
from src.auth.schemas import UserRead
from src.users.borrower.validations import is_user, is_deleted


class BorrowerCrud:
    pass



