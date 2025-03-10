import requests

from app.config import Config


class MovieService:
    BASE_URL = "https://api.themoviedb.org/3"

    @staticmethod
    def get_popular_movies():
        response = requests.get(
            f"{MovieService.BASE_URL}/movie/popular", params={"api_key": Config.API_KEY}
        )
        response.raise_for_status()
        return response.json()
