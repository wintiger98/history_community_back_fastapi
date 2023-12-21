from .config import client


def test_user_register():
    response = client.post(
        "/auth/register",
        json={
            "email": "test12@test.com",
            "password": "testpassword",
            "nickname": "nunu1",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test12@test.com"
    assert data["nickname"] == "nunu1"
    assert "id" in data
    user_id = data["id"]


def test_user_login():
    response = client.post(
        "/auth/register",
        json={
            "email": "test13@test.com",
            "password": "testpassword",
            "nickname": "nunu32",
        },
    )

    response = client.post(
        "/auth/token",
        data={"username": "test13@test.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
