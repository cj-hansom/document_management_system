import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

logger = logging.getLogger(__name__)

def init_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning("Validation error: %s", exc)
        return JSONResponse(
            status_code=422,
            content={"detail": "Invalid request payload."}
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        # Avoid leaking internals, but log details
        level = logging.WARNING if exc.status_code < 500 else logging.ERROR
        logger.log(level, "HTTPException %s: %s", exc.status_code, exc.detail)
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception")
        return JSONResponse(
            status_code=500,
            content={"detail": "Unexpected server error. Please try again later."}
        )
