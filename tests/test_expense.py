import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.auth import get_current_user


class MockUser:
    id = 1
    email = "mockuser@test.com"


def override_get_current_user():
    return MockUser()


app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.mark.asyncio
async def test_get_expenses_success():

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:

        response = await client.get("/expenses")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_expense_success():

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:

        response = await client.post(
            "/expenses",
            json={
                "title": "Lunch",
                "amount": 100,
                "category": "Food"
            }
        )

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Lunch"
    assert data["amount"] == 100
    assert data["category"] == "Food"


@pytest.mark.asyncio
async def test_delete_expense_success():

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:

        # Create expense first
        create_response = await client.post(
            "/expenses",
            json={
                "title": "Coffee",
                "amount": 50,
                "category": "Food"
            }
        )

        expense_id = create_response.json()["id"]

        # Delete expense
        delete_response = await client.delete(f"/expenses/{expense_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "successfully deleted expense"

