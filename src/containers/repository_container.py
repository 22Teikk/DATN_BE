import os

from src.adapters.database.redis import Redis
from src.adapters.repositories.mongo_repository import MongoRepository
from src.adapters.database.mongodb import MongoDB
from src.adapters.repositories.redis_cache import RedisCache



class RepositoryContainer:
    def __init__(self):
        self._cache = RedisCache(Redis())
        self._database = MongoDB()
        self.init_collections()

    def init_collections(self):
        self.entity_repository = MongoRepository(
            self._database.get_collection("entities"), self._cache
        )
        self.categories_repository = MongoRepository(
            self._database.get_collection("categories"), self._cache
        )
