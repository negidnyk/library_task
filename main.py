from fastapi import FastAPI, Depends
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.auth.models import UserModel
from src.auth.router import router as auth_router

app = FastAPI(title="Library App")

app.include_router(auth_router)

current_active_user = fastapi_users.current_user()


@app.get("/")
async def root(user: UserModel = Depends(current_active_user)):
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
