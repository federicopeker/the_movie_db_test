import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    API_KEY = os.getenv("TMDB_API_KEY")
    SECRET_KEY = os.getenv("TMDB_SECRET_KEY")
    REDIS_URL = os.getenv("TMDB_REDIS_URL")
    CACHE_DURATION = int(os.getenv("TMDB_CACHE_DURATION", 30))
    ACCESS_TOKENS = {
        "abcdef1234567890": {"id": 1, "role": "ADMIN"},
        "1234567890": {"id": 2, "role": "USER"},
    }
