import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_get_popular_movies(client):
    response = client.get("/movies/popular")
    assert response.status_code == 200
    assert "results" in response.json
