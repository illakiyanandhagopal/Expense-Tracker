import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

from app.auth import get_current_user

class MockUser:
    id = 1
    email = "test@test.com"

def override_get_current_user():
    return MockUser()

app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.mark.asyncio
async def test_create_expense_missing_title():

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:

        response = await client.post(
            "/expenses",
            json={
                "amount": 100,
                "category": "Food"
            }
        )

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_expense_invalid_amount():

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:

        response = await client.post(
            "/expenses",
            json={
                "title": "Dinner",
                "amount": "invalid",
                "category": "Food"
            }
        )

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_register_invalid_email():

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:

        response = await client.post(
            "/users/register",
            json={
                "email": "notanemail",
                "password": "password123"
            }
        )

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_expense_empty_title():

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:

        response = await client.post(
            "/expenses",
            json={
                "title": "",
                "amount": 100,
                "category": "Food"
            }
        )

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_expense_negative_amount():

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:

        response = await client.post(
            "/expenses",
            json={
                "title": "Dinner",
                "amount": -50,
                "category": "Food"
            }
        )

    assert response.status_code == 422