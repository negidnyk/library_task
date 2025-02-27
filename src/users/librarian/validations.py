from fastapi import HTTPException


async def is_librarian(role_id):
    if role_id != 1:
        raise HTTPException(status_code=403, detail="This option is for librarians only")
