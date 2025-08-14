# app/schemas/document_schema.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class DocumentCreate(BaseModel):
    title: str
    original_text: str

class Document(BaseModel):
    id: UUID
    title: str
    original_text: str
    user_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)  # Pydantic v2
