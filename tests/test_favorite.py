USER_TOKEN = "1234567890"


def test_add_favorite(client):
    response = client.post(
        "/movies/favorites/10",
        json={"release_date": "2022-01-01"},
        headers={"Authorization": f"Bearer {USER_TOKEN}"},
    )
    assert response.status_code == 200
    assert response.json == {"message": "Movie 10 added to favorites"}


def test_remove_favorite(client):
    response = client.delete(
        "/movies/favorites/10", headers={"Authorization": f"Bearer {USER_TOKEN}"}
    )
    assert response.status_code == 200
    assert response.json == {"message": "Movie 10 removed from favorites"}


def test_get_sorted_favorites(client):
    response = client.get(
        "/movies/favorites", headers={"Authorization": f"Bearer {USER_TOKEN}"}
    )
    assert response.status_code == 200
    assert "result" in response.json.keys()
    assert isinstance(response.json["result"], list)


def test_update_rating(client):
    client.post(
        "/movies/favorites/10",
        json={"release_date": "2022-01-01"},
        headers={"Authorization": f"Bearer {USER_TOKEN}"},
    )
    response = client.patch(
        "/movies/favorites/10",
        json={"rating": 8},
        headers={"Authorization": f"Bearer {USER_TOKEN}"},
    )
    assert response.status_code == 200
    assert response.json == {"message": "Rating for movie 10 updated to 8"}


def test_update_favorite_without_rating(client):
    response = client.patch(
        "/movies/favorites/1", headers={"Authorization": "Bearer 1234567890"}, json={}
    )
    assert response.status_code == 400
    assert response.json == {"error": "Rating not provided"}
