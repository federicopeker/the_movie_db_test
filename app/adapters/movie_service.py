from app.config import Config
from app.utils.retry import make_request_with_retry


class MovieService:
    BASE_URL = "https://api.themoviedb.org/3"

    @staticmethod
    def get_popular_movies():
        response = make_request_with_retry(
            url=f"{MovieService.BASE_URL}/movie/popular",
            method="GET",
            params={"api_key": Config.API_KEY},
        )
        response.raise_for_status()
        data = response.json()
        return data.get("results") if data.get("results") else []
