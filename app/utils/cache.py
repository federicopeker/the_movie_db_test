import json

import redis

from app.config import Config


class Cache:
    def __init__(self, redis_url=Config.REDIS_URL):
        self.redis_client = redis.StrictRedis.from_url(redis_url)

    def cache_response(self, key, response, duration=Config.CACHE_DURATION):
        self.redis_client.setex(key, duration, json.dumps(response))

    def get_cached_response(self, key):
        cached_response = self.redis_client.get(key)
        if cached_response:
            return json.loads(cached_response)
        return None
