from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from .database import database, metadata, engine
from .api.users import router as users_router
from .api.document import router as documents_router
from .api.auth import router as auth_router

from .core.logging import setup_logging
from .core.exceptions import init_exception_handlers
from .middleware.request_id import request_id_middleware


# Create database tables
metadata.create_all(bind=engine)

# Configure logging before app starts
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context for startup/shutdown tasks."""
    try:
        await database.connect()
        logging.info("✅ Database connection established successfully.")
    except Exception as e:
        logging.exception(f"❌ Database connection failed on startup: {e}")
        raise

    yield  # Application runs here

    try:
        await database.disconnect()
        logging.info("✅ Database connection closed successfully.")
    except Exception as e:
        logging.exception(f"❌ Database disconnection failed: {e}")


# Initialize FastAPI app with lifespan
app = FastAPI(title="Document Connector API", lifespan=lifespan)

# Middleware
app.middleware("http")(request_id_middleware)

# Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(documents_router)

# Exception handlers
init_exception_handlers(app)
