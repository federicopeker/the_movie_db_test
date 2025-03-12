import pytest
import redis

from app.config import Config

USER_TOKEN = "1234567890"
ADMIN_TOKEN = "abcdef1234567890"
HEADERS_USER = {"Authorization": f"Bearer {USER_TOKEN}"}
HEADERS_ADMIN = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
FAVORITES_URL = "/movies/favorites"


@pytest.fixture(scope="module")
def redis_client():
    client = redis.StrictRedis.from_url(Config.REDIS_URL)
    yield client
    client.flushall()


@pytest.fixture(scope="function", autouse=True)
def clear_cache(redis_client):
    redis_client.flushall()


def test_add_favorite(client):
    response = client.post(
        f"{FAVORITES_URL}/10",
        json={"release_date": "2022-01-01", "title": "Test Movie", "movie_id": 10},
        headers=HEADERS_USER,
    )
    assert response.status_code == 200
    assert response.json == {"message": "Movie 10 added to favorites"}


def test_remove_favorite(client):
    response = client.delete(f"{FAVORITES_URL}/10", headers=HEADERS_USER)
    assert response.status_code == 200
    assert response.json == {"message": "Movie 10 removed from favorites"}


def test_get_sorted_favorites(client):
    response = client.get(FAVORITES_URL, headers=HEADERS_USER)
    assert response.status_code == 200
    assert "result" in response.json.keys()
    assert isinstance(response.json["result"], list)


def test_update_rating(client):
    client.post(
        f"{FAVORITES_URL}/10",
        json={"release_date": "2022-01-01"},
        headers=HEADERS_USER,
    )
    response = client.patch(
        f"{FAVORITES_URL}/10", json={"rating": 8}, headers=HEADERS_USER,
    )
    assert response.status_code == 200
    assert response.json == {"message": "Rating for movie 10 updated to 8"}


def test_update_favorite_without_rating(client):
    response = client.patch(f"{FAVORITES_URL}/1", headers=HEADERS_USER, json={})
    assert response.status_code == 400
    assert response.json == {"error": "Rating not provided"}


def test_remove_all_favorites(client):
    client.post(
        f"{FAVORITES_URL}/10",
        json={"release_date": "2022-01-01"},
        headers=HEADERS_USER,
    )
    response = client.delete("/admin/users/2/favorites", headers=HEADERS_ADMIN)
    assert response.status_code == 200
    assert response.json == {"message": "All favorites for user 2 removed"}


def test_get_favorites_with_cache(client, redis_client):
    client.post(
        f"{FAVORITES_URL}/10",
        json={"release_date": "2022-01-01"},
        headers=HEADERS_USER,
    )
    response = client.get(FAVORITES_URL, headers=HEADERS_USER)
    assert response.status_code == 200
    assert "result" in response.json.keys()
    assert isinstance(response.json["result"], list)

    response = client.get(FAVORITES_URL, headers=HEADERS_USER)
    assert response.status_code == 200
    assert "result" in response.json.keys()
    assert isinstance(response.json["result"], list)
