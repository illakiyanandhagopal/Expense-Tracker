import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_register_user():

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/users/register",
            json={
                "email": "testuser@example.com",
                "password": "strongpassword"
            }
        )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_register_duplicate_user():

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:

        user_data = {
            "email": "duplicate@example.com",
            "password": "password123"
        }

        await client.post("/users/register", json=user_data)

        response = await client.post("/users/register", json=user_data)

    assert response.status_code == 400