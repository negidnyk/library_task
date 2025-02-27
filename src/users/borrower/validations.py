from fastapi import HTTPException


async def is_borrower(role_id):
    if role_id != 2:
        raise HTTPException(status_code=403, detail="This option is for borrowers only")
