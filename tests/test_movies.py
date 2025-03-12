import time

MOVIES_URL = "/movies"


def test_get_movies(client):
    response = client.get(MOVIES_URL)
    assert response.status_code == 200
    assert "data" in response.json
    assert response.json.get("success")


def test_get_movies_with_cache(client, redis_client):

    response = client.get(MOVIES_URL)
    assert response.status_code == 200

    response = client.get(MOVIES_URL)
    assert response.status_code == 200
    assert response.json.get("success")
    assert isinstance(response.json["data"], list)
    assert redis_client.exists("movies_popular") == 1


def test_get_movies_cache_expiration(client, redis_client):
    response = client.get(MOVIES_URL)
    assert response.status_code == 200

    initial_ttl = redis_client.ttl("movies_popular")
    assert initial_ttl > 0  # TTL is set

    # Wait for expiration (adjust based on TTL)
    time.sleep(initial_ttl + 1)
    assert redis_client.exists("movies_popular") == 0
