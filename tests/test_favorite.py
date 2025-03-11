USER_TOKEN = "1234567890"


def test_add_favorite(client):
    response = client.post(
        "/movies/favorites/10", headers={"Authorization": f"Bearer {USER_TOKEN}"}
    )
    assert response.status_code == 200
    assert response.json == {"message": "Movie 10 added to favorites"}


def test_remove_favorite(client):
    response = client.delete(
        "/movies/favorites/10", headers={"Authorization": f"Bearer {USER_TOKEN}"}
    )
    assert response.status_code == 200
    assert response.json == {"message": "Movie 10 removed from favorites"}
