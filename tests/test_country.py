from .config import client
from .config import Base, engine


def setup_function(function):
    # 테스트 데이터베이스 초기화
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_post_country():
    response = client.post(
        "/countries",
        json={"name": "South Korea"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "South Korea"


def test_get_all_countries():
    response = client.post(
        "/countries",
        json={"name": "South Korea"},
    )
    response = client.get("/countries")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_get_country():
    response = client.post(
        "/countries",
        json={"name": "South Korea"},
    )
    response = client.get("/countries/1")
    assert response.status_code == 200
    assert response.json()["name"] == "South Korea"


def test_put_country():
    response = client.post(
        "/countries",
        json={"name": "South Korea"},
    )
    response = client.put(
        "/countries/1",
        json={"name": "South Korea"},
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "Country updated"


def test_delete_country():
    response = client.post(
        "/countries",
        json={"name": "South Korea"},
    )
    response = client.delete("/countries/1")
    assert response.status_code == 200
    assert response.json()["detail"] == "Country deleted"


def test_cheer_country():
    response = client.post(
        "/countries",
        json={"name": "South Korea"},
    )

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

    data = response.json()

    token = data.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/countries/1/cheer", headers=headers)
    assert response.status_code == 200
    assert "Successfully" in response.json()["detail"]
