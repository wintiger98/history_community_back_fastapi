from .config import client
from .config import Base, engine


def setup_function(function):
    # 테스트 데이터베이스 초기화
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


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


def test_read_me():
    email = "test@test.com"
    password = "testpassword"
    nickname = "test"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "nickname": nickname,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["nickname"] == nickname

    response = client.post(
        "/auth/token",
        data={"username": email, "password": password},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

    token = data.get("access_token")

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)

    assert response.status_code == 200


def test_put_me():
    email = "test@test.com"
    password = "testpassword"
    nickname = "test"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "nickname": nickname,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["nickname"] == nickname

    response = client.post(
        "/auth/token",
        data={"username": email, "password": password},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

    token = data.get("access_token")

    headers = {"Authorization": f"Bearer {token}"}
    user_data = {"password": "", "nickname": "new_test"}
    response = client.put("/auth/me", headers=headers, json=user_data)

    assert response.status_code == 200
    assert response.json() == {"detail": "User updated"}


def test_delete_me():
    email = "test@test.com"
    password = "testpassword"
    nickname = "test"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "nickname": nickname,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["nickname"] == nickname

    response = client.post(
        "/auth/token",
        data={"username": email, "password": password},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

    token = data.get("access_token")

    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(
        "/auth/me",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted"}
