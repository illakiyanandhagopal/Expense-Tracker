import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.auth import get_current_user


class MockUser:
    id = 1


def override_get_current_user():
    return MockUser()


app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.mark.asyncio
async def test_expense_persistence():

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:

        create_response = await client.post(
            "/expenses",
            json={
                "title": "Dinner",
                "amount": 200,
                "category": "Food"
            }
        )

        assert create_response.status_code == 200

        get_response = await client.get("/expenses")

    expenses = get_response.json()

    # verify our created expense exists
    assert any(expense["title"] == "Dinner" for expense in expenses)