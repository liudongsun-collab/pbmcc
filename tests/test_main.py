import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from pbmcc"}


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_get_users_empty(client: AsyncClient):
    response = await client.get("/users")
    assert response.status_code == 200
    assert response.json() == {"users": []}


@pytest.mark.asyncio
async def test_get_users_with_data(client: AsyncClient):
    from sqlalchemy import text
    from tests.conftest import TestSessionLocal

    async with TestSessionLocal() as session:
        await session.execute(
            text("INSERT INTO users (name, email) VALUES (:name, :email)"),
            {"name": "Alice", "email": "alice@example.com"},
        )
        await session.commit()

    response = await client.get("/users")
    assert response.status_code == 200
    users = response.json()["users"]
    assert len(users) == 1
    assert users[0]["name"] == "Alice"
    assert users[0]["email"] == "alice@example.com"


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/users", json={"name": "Bob", "email": "bob@example.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Bob"
    assert data["email"] == "bob@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client: AsyncClient):
    payload = {"name": "Bob", "email": "bob@example.com"}
    await client.post("/users", json=payload)
    response = await client.post("/users", json=payload)
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"
