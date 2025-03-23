from datetime import datetime

from sqlmodel import SQLModel, Field


class BookBase(SQLModel):
    title: str = Field(..., max_length=100)
    author: str = Field(..., max_length=255)
    published_year: int = Field(..., ge=1000, le=datetime.now().year)


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class BookCreate(BookBase):
    pass