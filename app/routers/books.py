from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.database import SessionDep
from app.models import Book, BookCreate

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_books(
        session: SessionDep,
        limit: int = Query(1, ge=1),
        cursor: Optional[int] = Query(None, ge=1),
):
    query = session.query(Book).order_by(Book.id)
    if cursor is not None:
        query = query.filter(Book.id > cursor)

    books = query.limit(limit).all()

    next_cursor = books[-1].id if books else None

    return {"books": books, "limit": limit, "next_cursor": next_cursor}


@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int, session: SessionDep):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", status_code=201, response_model=Book)
async def add_book(book: BookCreate, session: SessionDep):
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: int, session: SessionDep):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return
