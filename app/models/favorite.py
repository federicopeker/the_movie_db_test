from typing import Dict, List


class FavoriteMoviesDB:
    _favorites: Dict[int, List[int]] = {}

    @classmethod
    def add_favorite(cls, user_id: int, movie_id: int):
        if user_id not in cls._favorites:
            cls._favorites[user_id] = []
        if movie_id not in cls._favorites[user_id]:
            cls._favorites[user_id].append(movie_id)

    @classmethod
    def remove_favorite(cls, user_id: int, movie_id: int):
        if user_id in cls._favorites and movie_id in cls._favorites[user_id]:
            cls._favorites[user_id].remove(movie_id)

    @classmethod
    def get_favorites(cls, user_id: int) -> List[int]:
        return cls._favorites.get(user_id, [])
