from sqlalchemy import Table, Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.database import metadata
import uuid

users = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("username", String, unique=True, index=True),
    Column("email", String, unique=True, index=True),
    Column("hashed_password", String),
    Column("is_active", Boolean, default=True),
)
