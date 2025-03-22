from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, create_engine
from .routers import books
from app.database import engine
from app.models import Book


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Books API", version="1.0.0", lifespan=lifespan)

app.include_router(books.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}
