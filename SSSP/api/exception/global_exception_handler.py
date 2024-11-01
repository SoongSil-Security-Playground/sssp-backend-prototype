import traceback, logging
from fastapi import Request, status
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.DEBUG)


# Exception Handler for General Exceptions
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(
        f"[*] ExceptionHandler>> Exception occurred: {exc} by Request {request}"
    )
    error_details = traceback.format_exc()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_name": "Internal Server Error",
            "error_message": error_details,
        },
    )
