from sqlalchemy import Table, Column, String, Text, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from ..database import metadata

documents = Table(
    "documents",
    metadata,
    Column("id", String, primary_key=True),
    Column("title", String, nullable=False),
    Column("original_text", Text, nullable=False),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
)
