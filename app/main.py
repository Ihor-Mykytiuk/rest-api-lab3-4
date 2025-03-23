from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel
from .routers import books
from app.database import engine


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
