from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import session

from app.database import SessionDep
from app.models import Book

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_books(session: SessionDep):
    books = session.query(Book).all()
    return {"books": books}


@router.get("/{book_id}")
async def get_book(book_id: int, session: SessionDep):
    book = session.query(Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book": book}


@router.post("/")
async def add_book(book: Book, session: SessionDep):
    session.add(book)
    session.commit()
    session.refresh(book)
    return {"book": book}


@router.delete("/{book_id}")
async def delete_book(book_id: int, session: SessionDep):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"ok": True}
