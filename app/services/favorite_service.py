from typing import Dict, List, Union

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
        """Returns all favorite movies for a user, sorted by specified fields."""
        return [fav.to_dict() for fav in cls._favorites.get(user_id, [])]

    @classmethod
    def get_favorites_sorted(
        cls, user_id: int, sort_by: [List[str]]
    ) -> List[Dict[str, Union[str, int]]]:
        """Returns all favorite movies for a user, sorted by specified fields.

        Args:
            user_id: ID of the user to get favorites for
            sort_by: Fields to sort by

        Returns:
            List of sorted favorite movies as dictionaries
        """
        sort_fields = sort_by or ["release_date", "rating"]

        favorites = cls.get_favorites(user_id)

        return sorted(
            favorites, key=lambda x: tuple(x[field] for field in sort_fields),
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
