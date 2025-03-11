# app/utils/cache.py
import json

import redis

from app.config import Config

redis_client = redis.StrictRedis.from_url(Config.REDIS_URL)


def cache_response(key, response, duration=Config.CACHE_DURATION):
    redis_client.setex(key, duration, json.dumps(response))


def get_cached_response(key):
    cached_response = redis_client.get(key)
    if cached_response:
        return json.loads(cached_response)
    return None
