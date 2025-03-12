from typing import Dict, List, Tuple


class FavoriteService:
    _favorites: Dict[int, List[Tuple[int, str, int]]] = {}

    @classmethod
    def add_favorite(
        cls, user_id: int, movie_id: int, release_date: str, rating: int = 0
    ):
        if user_id not in cls._favorites:
            cls._favorites[user_id] = []
        if not any(movie[0] == movie_id for movie in cls._favorites[user_id]):
            cls._favorites[user_id].append((movie_id, release_date, rating))

    @classmethod
    def remove_favorite(cls, user_id: int, movie_id: int):
        if user_id in cls._favorites:
            cls._favorites[user_id] = [
                movie for movie in cls._favorites[user_id] if movie[0] != movie_id
            ]

    @classmethod
    def get_favorites(cls, user_id: int) -> List[Tuple[int, str, int]]:
        return sorted(cls._favorites.get(user_id, []), key=lambda x: (x[1], x[2]))

    @classmethod
    def update_rating(cls, user_id: int, movie_id: int, new_rating: int):
        if user_id in cls._favorites:
            for i, movie in enumerate(cls._favorites[user_id]):
                if movie[0] == movie_id:
                    cls._favorites[user_id][i] = (movie_id, movie[1], new_rating)
                    break

    @classmethod
    def remove_all_favorites(cls, user_id: int):
        if user_id in cls._favorites:
            del cls._favorites[user_id]
