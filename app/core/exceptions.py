from fastapi import Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

# 기본 예외 핸들러이 필요하면 사용
# from fastapi.exception_handlers import (
#     http_exception_handler,
#     request_validation_exception_handler,
# )


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    message = "Validation errors:"
    for error in exc.errors():
        message += f"\nField: {error['loc']}, Error: {error['msg']}"
    return PlainTextResponse(message, status_code=400)


async def http_exception_handler(request, exc: HTTPException):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
    # return await http_exception_handler(request, exc)
