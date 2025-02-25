from fastapi import HTTPException


async def is_user(role_id):
    if role_id != 3:
        raise HTTPException(status_code=403, detail="This option is for users only")


async def is_admin(role_id):
    if role_id != 1 or role_id != 2:
        raise HTTPException(status_code=403, detail="This option is for librarian only")


async def is_master(role_id):
    if role_id != 4:
        raise HTTPException(status_code=403, detail="This option is for masters only")


async def is_user_or_master(role_id):
    if role_id != 3 or role_id != 4:
        raise HTTPException(status_code=403, detail="This option is for masters and users only")


async def is_deleted(user):
    if user.is_deleted is True:
        raise HTTPException(status_code=400, detail=f"User: {user.username} is deleted!")
