from fastapi import FastAPI
from .routers import books

app = FastAPI(title="Books API", version="1.0.0")

app.include_router(books.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}
