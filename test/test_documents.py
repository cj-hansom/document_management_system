# tests/test_documents.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import database  # correct import
from app.dependencies import get_current_user

# Mock user
class MockUser:
    beartoken = "mocktoken"
    id = "b5f5a4d4-cda3-4d88-b2c9-c6ec08309257"

# Override auth
app.dependency_overrides[get_current_user] = lambda: MockUser()

@pytest.mark.asyncio
async def test_document_crud():
    await database.connect()
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Create
            doc_data = {"title": "Test Doc", "original_text": "Hello world"}
            response = await client.post("/documents/", json=doc_data)
            assert response.status_code == 201
            created = response.json()
            doc_id = str(created["id"])



            # Read
            response = await client.get(f"/documents/{doc_id}")
            assert response.status_code == 200
            assert response.json()["title"] == "Test Doc"

            # Delete
            response = await client.delete(f"/documents/{doc_id}")
            assert response.status_code == 204

            # Confirm deletion
            response = await client.get(f"/documents/{doc_id}")
            assert response.status_code == 404
    finally:
        await database.disconnect()
