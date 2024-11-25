import traceback
import logging
from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import DataError, IntegrityError
from pydantic import ValidationError

logging.basicConfig(level=logging.WARNING)


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
    logging.error(f"[*] ExceptionHandler>> Stacktrace: {error_details}")

    try:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error_name": "Internal Server Error",
                "error_message": str(exc),
                "details": (
                    error_details if not isinstance(exc, HTTPException) else None
                ),
            },
        )
    except Exception as e:
        logging.critical(f"[*] ExceptionHandler>> Failed to handle exception: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error_message": "Critical error in exception handler"},
        )


# Validation Exception Handler
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    logging.error(
        f"[*] PydanticValidationHandler>> Validation error: {exc} for Request {request.url}"
    )
    error_details = exc.errors()
    logging.debug(f"Validation error details: {error_details}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error_name": "Validation Error",
            "detail": error_details,
            "message": "입력 데이터 검증 실패",
        },
    )
