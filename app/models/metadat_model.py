import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .database import metadata



metadata_table = sqlalchemy.Table(
    "metadata",
    metadata,
    sqlalchemy.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    sqlalchemy.Column("document_id", UUID(as_uuid=True), sqlalchemy.ForeignKey("documents.id")),
    sqlalchemy.Column("key", sqlalchemy.String),
    sqlalchemy.Column("value", sqlalchemy.String),
)
