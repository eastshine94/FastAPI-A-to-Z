from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, HTTPException, Query

from fastapi.exceptions import RequestValidationError
from sqlmodel import Field, SQLModel, select
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routers import api_router

from app.core.database import create_db_and_tables
from app.core.exceptions import (
    UnicornException,
    unicorn_exception_handler,
    validation_exception_handler,
    http_exception_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # DB 테이블 생성
    create_db_and_tables()
    yield
    print("shutdown!!!")


app = FastAPI(
    title="My FastAPI Project",
    description="API documentation",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_exception_handler(UnicornException, unicorn_exception_handler)

# 요청 검증 예외 오버라이드
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# HTTPException 오버라이드
app.add_exception_handler(StarletteHTTPException, http_exception_handler)

app.include_router(api_router, prefix="/api/v1")
