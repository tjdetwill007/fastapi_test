from .books.routes import book_router
from fastapi import APIRouter

books_router = APIRouter()
books_router.include_router(book_router)
