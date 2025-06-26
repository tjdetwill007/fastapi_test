from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
from uuid import UUID, uuid4


class Book(SQLModel, table=True):
    """Book model for the database.
    sa_column is used to define the SQLAlchemy column type and properties.
    we are using postgresql dialect for UUID and TIMESTAMP so that we have perfect types for columns.
    """

    __tablename__ = "books"

    uid: UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, nullable=False, default=uuid4())
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))

    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"
