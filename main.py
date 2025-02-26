from fastapi import FastAPI, Depends
from src.auth.router import router as auth_router
from src.authors.router import router as authors_router
from src.books.router import router as books_router
from src.genres.router import router as genres_router
from src.publishers.router import router as publishers_router

app = FastAPI(title="Library App")

app.include_router(auth_router)
app.include_router(authors_router)
app.include_router(books_router)
app.include_router(genres_router)
app.include_router(publishers_router)