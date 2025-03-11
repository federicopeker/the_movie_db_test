def test_get_popular_movies(client):
    response = client.get("/movies/popular")
    assert response.status_code == 200
    assert "results" in response.json
