from app.config import Config


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


def test_valid_token_returns_200(client):
    response = client.get(
        "/movies/favorites", headers={"Authorization": "Bearer 1234567890"}
    )
    assert response.status_code == 200
    assert "result" in response.json.keys()


def test_unauthorized_role_returns_403(client):
    response = client.get(
        "/movies/favorites", headers={"Authorization": "Bearer unauthorized_token"}
    )
    assert response.status_code == 403
    assert response.json == {"error": "Invalid token"}


def test_valid_token_without_role_returns_403(client):
    USER_TOKEN = "1234567890withoutrole"
    Config.ACCESS_TOKENS.update({USER_TOKEN: {"id": 3, "role": None}})
    response = client.get(
        "/movies/favorites", headers={"Authorization": f"Bearer {USER_TOKEN}"}
    )
    assert response.status_code == 403
    assert response.json == {"error": "Unauthorized"}
