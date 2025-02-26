from fastapi import HTTPException


async def validate_int_id(id):
    if id <= 0 or id > 2147483647:
        raise HTTPException(status_code=400, detail="'id' value should be more than 0 and less than 2147483647")
