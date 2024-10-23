import os

import redis


class Redis:
    def __init__(self):

        redis_host = "localhost"
        redis_port = "6379"
        redis_db = "0"

        self.cache = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
        )
        if self.cache.ping():
            print("Connected to Redis successfully!")
        else:
            print("Failed to connect to Redis")
            raise Exception("Failed to connect to Redis")

    def get_cache_db(self, cache_db: int = 0):
        if cache_db != 0:
            self.cache.execute_command("SELECT", cache_db)
            self.cache.setex
            return self.cache
        else:
            return self.cache
