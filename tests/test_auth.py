import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_auth_required(client):
    response = client.get("/movies/favorites")
    assert response.status_code == 401
    assert response.json == {"error": "Token is missing"}


def test_auth_invalid_token(client):
    response = client.get(
        "/movies/favorites", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 403
    assert response.json == {"error": "Invalid token"}
