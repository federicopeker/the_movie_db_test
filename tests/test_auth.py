from app.config import Config

ID_USER = 2
FAVORITES_URL = f"/users/{ID_USER}/favorites"


def test_auth_required(client):
    response = client.get(FAVORITES_URL)
    assert response.status_code == 401
    assert response.json == {"error": "Token is missing"}


def test_auth_invalid_token(client):
    response = client.get(
        FAVORITES_URL, headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 403
    assert response.json == {"error": "Invalid token"}


def test_valid_token_returns_200(client):
    response = client.get(FAVORITES_URL, headers={"Authorization": "Bearer 1234567890"})
    assert response.status_code == 200
    assert response.json.get("success")


def test_unauthorized_role_returns_403(client):
    response = client.get(
        FAVORITES_URL, headers={"Authorization": "Bearer unauthorized_token"}
    )
    assert response.status_code == 403
    assert response.json == {"error": "Invalid token"}


def test_valid_token_without_role_returns_403(client):
    USER_TOKEN = "1234567890withoutrole"
    Config.ACCESS_TOKENS.update({USER_TOKEN: {"id": 3, "role": None}})
    response = client.get(
        FAVORITES_URL, headers={"Authorization": f"Bearer {USER_TOKEN}"}
    )
    assert response.status_code == 403
    assert response.json == {"error": "Unauthorized"}
