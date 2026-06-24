from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.config.settings import get_settings
from src.core.exceptions.base import AppException
from src.core.exceptions.handlers import app_exception_handler
from src.core.logging.logger import configure_logger
from src.presentation.api.router import (
    api_router,
)

configure_logger()

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.include_router(
    api_router
)



@app.get("/")
async def root():
    return {
        "message": "RAG SQL Chatbot API"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


@app.get("/version")
async def version():
    return {
        "version": settings.APP_VERSION
    }
