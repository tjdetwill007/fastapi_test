from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
import src.routers.books.dao as dao
from fastapi import HTTPException, status
from datetime import date, datetime
from .models import Book

class BookService:
    """Service class for book operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_books(self):
        """Get all books."""
        all_books = await dao.BookDAO().get_all_books(self.session)
        if not all_books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Books Found",
            )
        return all_books

    async def get_book_by_uid(self, book_uid: str) -> Book:
        """Get a book by its UID."""
        a_book = await dao.BookDAO().get_book_by_uid(self.session, book_uid)
        if not a_book or a_book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found",
            )
        print("Testing Type of book object: ",type(a_book))
        return a_book   

    async def create_book(self, book_data: BookCreateModel):
        """Create a new book."""
        book_data = book_data.model_dump()
        date_string = book_data.pop("published_date")  # Remove string date from dict
    
        # Convert string to date object
        published_date = date.fromisoformat(date_string)
        book_data = Book(**book_data, published_date=published_date)
        book = await dao.BookDAO().add_book(self.session, book_data)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book creation failed",
            )
        return book

    async def update_book(self, book_uid: str, update_data: BookUpdateModel):
        """Update an existing book."""
        update_book = await self.get_book_by_uid(book_uid) #Get the book to update using the uid
        if not update_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found",
            )
        update_data = update_data.model_dump() # Convert to dict
        
        for key, value in update_data.items():
            if value is not None:
                setattr(update_book, key, value) # Update the book object with new values
        # Update the updated_at field to the current datetime
        setattr(update_book, "updated_at", datetime.now())

        # Call the DAO to update the book in the database
        updated_book = await dao.BookDAO().update_book(self.session, update_book)
        if not updated_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book update failed",
            )
        return updated_book

    async def delete_book(self, book_uid: str):
        """Delete a book."""
        deleted_book = await dao.BookDAO().delete_book(self.session, book_uid)
        if not deleted_book or deleted_book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found to delete"
            )
        return deleted_book
