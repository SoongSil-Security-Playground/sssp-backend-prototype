import traceback
import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import DataError, IntegrityError

logging.basicConfig(level=logging.DEBUG)


# SQLAlchemy DataError Handler
async def sqlalchemy_data_error_handler(request: Request, exc: DataError):
    logging.error(f"[*] DataError>> {exc} for Request {request.url}")
    error_details = traceback.format_exc()
    logging.debug(str(exc.orig))
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error_name": "Database Error",
            "error_message": str(exc.orig),  # 원본 SQL 오류 메시지
            "details": error_details,
        },
    )


# SQLAlchemy IntegrityError Handler
async def sqlalchemy_integrity_error_handler(request: Request, exc: IntegrityError):
    logging.error(f"[*] IntegrityError>> {exc} for Request {request.url}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error_name": "Integrity Error",
            "error_message": "A database constraint was violated.",
        },
    )


# General Exception Handler
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(
        f"[*] ExceptionHandler>> Exception occurred: {exc} by Request {request.url}"
    )
    error_details = traceback.format_exc()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_name": "Internal Server Error",
            "error_message": "An unexpected error occurred. Please contact support.",
            "details": error_details,
        },
    )


# Validation Exception Handler
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(
        f"[*] ValidationExceptionHandler>> Validation error: {exc} for Request {request.url}"
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error_name": "Validation Error",
            "details": exc.errors(),
            "body": exc.body,
        },
    )
