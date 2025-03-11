import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    API_KEY = os.getenv("TMDB_API_KEY")
    SECRET_KEY = os.getenv("TMDB_SECRET_KEY")
    ACCESS_TOKENS = {
        "abcdef1234567890": {"id": 1, "role": "ADMIN"},
        "1234567890": {"id": 2, "role": "USER"},
    }
