from fastapi import APIRouter, status, HTTPException, Depends
from src.routers.books.book_data import books
from src.routers.books.schemas import Books, BookUpdateModel, BookCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
import src.routers.books.service as service
from src.db.main import get_session

book_router = APIRouter(prefix="/books", tags=["Books"])


@book_router.get("/", response_model=List[Books])
async def get_all_books(db: AsyncSession = Depends(get_session)) -> list[Books]:
    """Get all books."""
    all_books = await service.BookService(db).get_all_books()
    return all_books
    


@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: BookCreateModel, db: AsyncSession = Depends(get_session)) -> dict:
    new_book = await service.BookService(db).create_book(book_data)
    return dict(new_book)


@book_router.get("/{book_id}")
async def get_book(book_id: str, db: AsyncSession = Depends(get_session)) -> dict:
    """Get a book by its ID."""
    a_book = await service.BookService(db).get_book_by_uid(book_id)
    print(f"A Book {book_id}: ",a_book)
    print("Type of book object: ",type(a_book))
    return dict(a_book)


@book_router.patch("/{book_id}")
async def update_book(book_id: str, book_update_data: BookUpdateModel, db: AsyncSession = Depends(get_session)) -> dict:
    update_book = await service.BookService(db).update_book(book_id, book_update_data)
    return dict(update_book)

    


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, db: AsyncSession = Depends(get_session)):
    delete_book = await service.BookService(db).delete_book(book_id)
    return {
        "Details": f"Requested book {delete_book.title} was deleted successfully"
    }
