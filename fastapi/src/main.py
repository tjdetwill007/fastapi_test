from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routers import books_router
from src.db.main import init_db, close_db

version = "v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup logic here")
    await init_db()
    yield  # <-- app runs while paused here
    print("Shutdown logic here")
    await close_db()


app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version=version,
    lifespan=lifespan,
)

app.include_router(books_router, prefix=f"/api/{version}")
