from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc, update, delete
from .models import Book


class BookDAO:
    async def get_all_books(self, db: AsyncSession):
        """Get all books."""
        statement =  select(Book).order_by(desc(Book.created_at))
        result = await db.exec(statement)
        return result.all()
    
    async def add_book(self, db: AsyncSession, book: Book):
        """Add a new book."""
        db.add(book)
        await db.commit()
        await db.refresh(book)
        return book
    
    async def get_book_by_uid(self, db: AsyncSession, book_uid: str):
        """Get a book by its UID."""
        statement = select(Book).where(Book.uid == book_uid)
        result = await db.exec(statement)
        return result.first()
    
    async def update_book(self, db: AsyncSession, update_data: Book):
        
        await db.commit()
        await db.refresh(update_data)
        return update_data
    
    async def delete_book(self, db: AsyncSession, book_uid: str):
        book = await db.get(Book, book_uid)
        if not book:
            return None
        await db.delete(book)
        await db.commit()
        return book