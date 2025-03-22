from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, create_engine
from .routers import books
import os
from dotenv import load_dotenv
from .models import Book

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Books API", version="1.0.0", lifespan=lifespan)

app.include_router(books.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}
