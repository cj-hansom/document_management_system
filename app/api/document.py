# app/api/document.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import uuid4, UUID
import logging
from sqlalchemy import and_

from ..schemas.document_schema import Document, DocumentCreate
from ..database import database
from ..models.document_model import documents
from ..dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/", response_model=Document, status_code=status.HTTP_201_CREATED)
async def create_document(payload: DocumentCreate, current_user=Depends(get_current_user)):
    try:
        doc_id = uuid4()
        await database.execute(
            documents.insert().values(
                id=str(doc_id),
                title=payload.title,
                original_text=payload.original_text,
                user_id=str(current_user.id),  
            )
        )
        row = await database.fetch_one(documents.select().where(documents.c.id == str(doc_id)))
        if not row:
            raise HTTPException(status_code=500, detail="Insert succeeded but fetch failed")
        return dict(row) 
    except HTTPException:
        raise
    except Exception:
        logger.exception("Failed to create document")
        raise HTTPException(status_code=500, detail="Failed to create document")

@router.get("/", response_model=List[Document])
async def list_documents(current_user=Depends(get_current_user)):
    try:
        rows = await database.fetch_all(
            documents.select().where(documents.c.user_id == current_user.id)
        )
        return [dict(r) for r in rows]
    except Exception:
        logger.exception("Failed to list documents")
        raise HTTPException(status_code=500, detail="Failed to list documents")

@router.get("/{doc_id}", response_model=Document)
async def get_document(doc_id, current_user=Depends(get_current_user)):
    try:
        row = await database.fetch_one(
            documents.select().where(
                and_(documents.c.id == doc_id, documents.c.user_id == current_user.id)
            )
        )
        if not row:
            raise HTTPException(status_code=404, detail="Document not found")
        return dict(row)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Failed to get document")
        raise HTTPException(status_code=500, detail="Failed to get document")

@router.put("/{doc_id}", response_model=Document)
async def update_document(doc_id, updated: DocumentCreate, current_user=Depends(get_current_user)):
    try:
        await database.execute(
            documents.update()
            .where(and_(documents.c.id == doc_id, documents.c.user_id == current_user.id))
            .values(title=updated.title, original_text=updated.original_text)
        )
        row = await database.fetch_one(documents.select().where(documents.c.id == str(doc_id)))
        if not row:
            raise HTTPException(status_code=404, detail="Document not found")
        return dict(row)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Failed to update document")
        raise HTTPException(status_code=500, detail="Failed to update document")

@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(doc_id, current_user=Depends(get_current_user)):
    try:
        await database.execute(
            documents.delete().where(
                and_(documents.c.id == doc_id, documents.c.user_id == current_user.id)
            )
        )
        return None
    except Exception:
        logger.exception("Failed to delete document")
        raise HTTPException(status_code=500, detail="Failed to delete document")
