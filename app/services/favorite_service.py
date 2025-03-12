from typing import Dict, List

from app.models.movie import Movie


class FavoriteService:
    _favorites: Dict[int, List[Movie]] = {}

    @classmethod
    def add_favorite(cls, user_id: int, movie: Movie):
        if user_id not in cls._favorites:
            cls._favorites[user_id] = []
        if not any(fav.id == movie.id for fav in cls._favorites[user_id]):
            cls._favorites[user_id].append(movie)

    @classmethod
    def remove_favorite(cls, user_id: int, movie_id: int):
        """Removes a favorite movie from the user's list."""
        if user_id in cls._favorites:
            cls._favorites[user_id] = [
                fav for fav in cls._favorites[user_id] if fav.id != movie_id
            ]

    @classmethod
    def get_favorites(cls, user_id: int) -> List[Dict[str, str | int]]:
        """Returns all favorite movies for a user, sorted by release date and rating."""
        return sorted(
            [fav.to_dict() for fav in cls._favorites.get(user_id, [])],
            key=lambda x: (x["release_date"], x["rating"]),
        )

    @classmethod
    def update_rating(cls, user_id: int, movie_id: int, new_rating: int):
        """Updates the rating of a specific favorite movie."""
        if user_id in cls._favorites:
            for fav in cls._favorites[user_id]:
                if fav.id == movie_id:
                    fav.rating = new_rating
                    break

    @classmethod
    def remove_all_favorites(cls, user_id: int):
        """Removes all favorite movies for a user."""
        cls._favorites.pop(user_id, None)
