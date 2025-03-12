import pytest
import redis

from app import create_app
from app.config import Config


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            # Initialize any required data here
            yield client


@pytest.fixture(scope="module")
def redis_client():
    client = redis.StrictRedis.from_url(Config.REDIS_URL)
    yield client
    client.flushall()


@pytest.fixture(scope="function", autouse=True)
def clear_cache(redis_client):
    redis_client.flushall()
