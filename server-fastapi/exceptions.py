from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

async def http_exception_handler(request: Request, exc: HTTPException):
    """Convert HTTPException to use 'error' key instead of 'detail'"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Convert validation errors to 400 with error message"""
    errors = exc.errors()
    if errors:
        # Get first error message
        first_error = errors[0]
        field = first_error.get("loc", [""])[-1]
        msg = first_error.get("msg", "Validation error")
        error_msg = f"{field}: {msg}" if field else msg
    else:
        error_msg = "Validation error"
    
    return JSONResponse(
        status_code=400,
        content={"error": error_msg}
    )
