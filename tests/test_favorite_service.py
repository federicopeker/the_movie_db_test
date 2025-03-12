from app.models.movie import Movie
from app.services.favorite_service import FavoriteService


def test_add_favorite():
    service = FavoriteService()
    movie = Movie(id=132, title="The Gorge", release_date="2025-02-13", rating=0)

    service.add_favorite(user_id=1, movie=movie)
    favorites = service.get_favorites(user_id=1)

    assert len(favorites) == 1
    assert favorites[0]["id"] == 132
    assert favorites[0]["title"] == "The Gorge"


def test_remove_favorite():
    service = FavoriteService()
    movie = Movie(id=132, title="The Gorge", release_date="2025-02-13", rating=0)

    service.add_favorite(user_id=1, movie=movie)
    service.remove_favorite(user_id=1, movie_id=132)

    assert len(service.get_favorites(user_id=1)) == 0


def test_update_rating():
    service = FavoriteService()
    movie = Movie(id=132, title="The Gorge", release_date="2025-02-13", rating=0)

    service.add_favorite(user_id=1, movie=movie)
    service.update_rating(user_id=1, movie_id=132, new_rating=5)

    favorites = service.get_favorites(user_id=1)
    assert favorites[0]["rating"] == 5


def test_remove_all_favorites():
    service = FavoriteService()
    movie1 = Movie(id=132, title="The Gorge", release_date="2025-02-13", rating=0)
    movie2 = Movie(id=150, title="Inception", release_date="2010-07-16", rating=0)

    service.add_favorite(user_id=1, movie=movie1)
    service.add_favorite(user_id=1, movie=movie2)
    service.remove_all_favorites(user_id=1)

    assert len(service.get_favorites(user_id=1)) == 0


def test_get_favorite_sorted():
    service = FavoriteService()
    movie = Movie(id=132, title="The Gorge", release_date="2025-02-13", rating=0)

    service.add_favorite(user_id=1, movie=movie)
    movie = Movie(id=23, title="Titanic", release_date="2025-01-13", rating=3)

    service.add_favorite(user_id=1, movie=movie)
    favorites = service.get_favorites_sorted(
        user_id=1, sort_by=["release_date", "rating"]
    )

    assert len(favorites) == 2
    assert favorites[0]["id"] == 23
    assert favorites[0]["title"] == "Titanic"
    assert favorites[1]["id"] == 132
    assert favorites[1]["title"] == "The Gorge"


def test_get_favorite_sorted_other():
    service = FavoriteService()
    movie = Movie(id=132, title="The Gorge", release_date="2025-02-13", rating=0)

    service.add_favorite(user_id=1, movie=movie)
    movie = Movie(id=23, title="Titanic", release_date="2025-01-13", rating=3)

    service.add_favorite(user_id=1, movie=movie)
    favorites = service.get_favorites_sorted(
        user_id=1, sort_by=["rating", "release_date"]
    )

    assert len(favorites) == 2
    assert favorites[0]["id"] == 132
    assert favorites[0]["title"] == "The Gorge"
    assert favorites[1]["id"] == 23
    assert favorites[1]["title"] == "Titanic"
