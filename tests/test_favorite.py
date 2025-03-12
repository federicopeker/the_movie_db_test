import time
from unittest.mock import patch

import pytest
import redis

from app.config import Config

USER_TOKEN = "1234567890"
ADMIN_TOKEN = "abcdef1234567890"
HEADERS_USER = {"Authorization": f"Bearer {USER_TOKEN}"}
ID_USER = 2
HEADERS_ADMIN = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
FAVORITES_URL = "/favorites"


@pytest.fixture(scope="module")
def redis_client():
    client = redis.StrictRedis.from_url(Config.REDIS_URL)
    yield client
    client.flushall()


@pytest.fixture(scope="function", autouse=True)
def clear_cache(redis_client):
    redis_client.flushall()


def test_add_favorite(client):
    data = {"release_date": "2022-01-01", "title": "Test Movie", "id": 10}
    response = client.post(FAVORITES_URL, json=data, headers=HEADERS_USER,)
    data.update({"rating": 0})
    assert response.status_code == 201
    assert response.json.get("success")
    assert response.json.get("data") == data


def test_add_favorite_without_data(client):
    response = client.post(FAVORITES_URL, json={}, headers=HEADERS_USER,)
    assert response.status_code == 400
    assert not response.json.get("success")
    assert response.json.get("error") == "400 Bad Request: Request body is missing"


def test_add_favorite_without_title(client):
    data = {"release_date": "2022-01-01", "id": 10}

    response = client.post(FAVORITES_URL, json=data, headers=HEADERS_USER,)
    assert response.status_code == 400
    assert not response.json.get("success")
    assert (
        response.json.get("error")
        == "400 Bad Request: Missing required fields: 'id', 'title' and 'release_date'"
    )


def test_add_favorite_without_id(client):
    data = {"release_date": "2022-01-01", "title": "Test Movie"}

    response = client.post(FAVORITES_URL, json=data, headers=HEADERS_USER,)
    assert response.status_code == 400
    assert not response.json.get("success")
    assert (
        response.json.get("error")
        == "400 Bad Request: Missing required fields: 'id', 'title' and 'release_date'"
    )


def test_add_favorite_without_release_date(client):
    data = {"title": "Test Movie", "id": 10}

    response = client.post(FAVORITES_URL, json=data, headers=HEADERS_USER,)
    assert response.status_code == 400
    assert not response.json.get("success")
    assert (
        response.json.get("error")
        == "400 Bad Request: Missing required fields: 'id', 'title' and 'release_date'"
    )


def test_add_favorite_internal_server_error(client):
    """Test if the endpoint correctly handles an internal server error"""
    with patch(
        "app.services.favorite_service.FavoriteService.add_favorite"
    ) as mock_service:
        mock_service.side_effect = Exception("FavoriteService.add_favorite failed")

        data = {"release_date": "2022-01-01", "title": "Test Movie", "id": 10}

        response = client.post(FAVORITES_URL, json=data, headers=HEADERS_USER,)

        assert response.status_code == 500
        assert response.json == {"success": False, "error": "Internal Server Error"}


def test_remove_favorite(client):
    response = client.delete(f"{FAVORITES_URL}/10", headers=HEADERS_USER)
    assert response.status_code == 200
    assert response.json.get("success")
    assert response.json.get("message") == "Movie 10 removed from favorites"


def test_remove_favorite_internal_server_error(client):
    with patch(
        "app.services.favorite_service.FavoriteService.remove_favorite"
    ) as mock_service:
        mock_service.side_effect = Exception("FavoriteService.remove_favorite failed")
        response = client.delete(f"{FAVORITES_URL}/10", headers=HEADERS_USER)

        assert response.status_code == 500
        assert response.json == {"success": False, "error": "Internal Server Error"}


def test_get_sorted_favorites(client):
    response = client.get(FAVORITES_URL, headers=HEADERS_USER)
    assert response.status_code == 200
    assert response.json.get("success")
    assert isinstance(response.json["data"], list)


def test_get_sorted_favorites_internal_server_error(client):
    with patch(
        "app.services.favorite_service.FavoriteService.get_favorites"
    ) as mock_service:
        mock_service.side_effect = Exception("FavoriteService.get_favorites failed")
        response = client.get(FAVORITES_URL, headers=HEADERS_USER)

        assert response.status_code == 500
        assert response.json == {"success": False, "error": "Internal Server Error"}


def test_update_rating(client):
    data = {"release_date": "2022-01-01", "title": "Test Movie", "id": 10}
    client.post(
        FAVORITES_URL, json=data, headers=HEADERS_USER,
    )
    response = client.patch(
        f"{FAVORITES_URL}/10", json={"rating": 3}, headers=HEADERS_USER,
    )
    assert response.status_code == 200
    assert response.json.get("success")
    assert response.json.get("message") == "Rating for movie 10 updated to 3"


def test_update_favorite_without_rating(client):
    response = client.patch(f"{FAVORITES_URL}/1", headers=HEADERS_USER, json={})
    assert response.status_code == 400
    assert not response.json.get("success")
    assert (
        response.json.get("error")
        == "400 Bad Request: Missing required field: 'rating'"
    )


def test_update_favorite_with_rating_negative(client):
    data = {"release_date": "2022-01-01", "title": "Test Movie", "id": 10}
    client.post(
        FAVORITES_URL, json=data, headers=HEADERS_USER,
    )
    response = client.patch(
        f"{FAVORITES_URL}/10", json={"rating": -1}, headers=HEADERS_USER,
    )
    assert response.status_code == 400
    assert not response.json.get("success")
    assert (
        response.json.get("error")
        == "400 Bad Request: Rating must be an integer between 0 and 5"
    )


def test_update_favorite_with_rating_greather_5(client):
    data = {"release_date": "2022-01-01", "title": "Test Movie", "id": 10}
    client.post(
        FAVORITES_URL, json=data, headers=HEADERS_USER,
    )
    response = client.patch(
        f"{FAVORITES_URL}/10", json={"rating": 6}, headers=HEADERS_USER,
    )
    assert response.status_code == 400
    assert not response.json.get("success")
    assert (
        response.json.get("error")
        == "400 Bad Request: Rating must be an integer between 0 and 5"
    )


def test_update_favorite_internal_server_error(client):
    with patch(
        "app.services.favorite_service.FavoriteService.update_rating"
    ) as mock_service:
        mock_service.side_effect = Exception("FavoriteService.update_rating failed")
        data = {"release_date": "2022-01-01", "title": "Test Movie", "id": 10}
        client.post(
            FAVORITES_URL, json=data, headers=HEADERS_USER,
        )
        response = client.patch(
            f"{FAVORITES_URL}/10", json={"rating": 4}, headers=HEADERS_USER,
        )

        assert response.status_code == 500
        assert response.json == {"success": False, "error": "Internal Server Error"}


def test_remove_all_favorites(client):
    data = {"release_date": "2022-01-01", "title": "Test Movie", "id": 10}
    client.post(
        FAVORITES_URL, json=data, headers=HEADERS_USER,
    )
    response = client.delete("/admin/users/2/favorites", headers=HEADERS_ADMIN)
    assert response.status_code == 200
    assert response.json.get("success")
    assert response.json.get("message") == "All favorites for user 2 removed"


def test_get_favorites_with_cache(client, redis_client):
    data = {"release_date": "2022-01-01", "title": "Test Movie", "id": 10}
    client.post(
        FAVORITES_URL, json=data, headers=HEADERS_USER,
    )
    response = client.get(FAVORITES_URL, headers=HEADERS_USER)
    assert response.status_code == 200

    response = client.get(FAVORITES_URL, headers=HEADERS_USER)
    assert response.status_code == 200
    assert response.json.get("success")
    assert isinstance(response.json["data"], list)
    cache_key = f"favorites_{ID_USER}"
    assert redis_client.exists(cache_key) == 1


def test_cache_expiration(client, redis_client):
    data = {"release_date": "2022-01-01", "title": "Test Movie", "id": 10}
    client.post(
        FAVORITES_URL, json=data, headers=HEADERS_USER,
    )
    client.get(FAVORITES_URL, headers=HEADERS_USER)
    cache_key = f"favorites_{ID_USER}"

    initial_ttl = redis_client.ttl(cache_key)
    assert initial_ttl > 0  # TTL is set

    # Wait for expiration (adjust based on TTL)
    time.sleep(initial_ttl + 1)
    assert redis_client.exists(cache_key) == 0  # Cache expired


def test_remove_all_favorites_internal_server_error(client):
    with patch(
        "app.services.favorite_service.FavoriteService.remove_all_favorites"
    ) as mock_service:
        mock_service.side_effect = Exception(
            "FavoriteService.remove_all_favorites failed"
        )
        response = client.delete(
            f"/admin/users/{ID_USER}/favorites", headers=HEADERS_ADMIN
        )

        assert response.status_code == 500
        assert response.json == {"success": False, "error": "Internal Server Error"}
