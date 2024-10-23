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
        self.user_repository = MongoRepository(
            self._database.get_collection("users"), self._cache
        )
        self.file_repository = MongoRepository(
            self._database.get_collection("files"), self._cache
        )
        self.user_file_repository = MongoRepository(
            self._database.get_collection("user_files"), self._cache
        )
        self.user_event_repository = MongoRepository(
            self._database.get_collection("user_events"), self._cache
        )
        self.user_data_repository = MongoRepository(
            self._database.get_collection("user_datas"), self._cache
        )
        self.user_directory_repository = MongoRepository(
            self._database.get_collection("user_directorys"), self._cache
        )
        self.user_location_repository = MongoRepository(
            self._database.get_collection("user_location"), self._cache
        )
        self.ad_remote_repository = MongoRepository(
            self._database.get_collection("ad_remotes"), self._cache
        )
        self.data_remote_repository = MongoRepository(
            self._database.get_collection("data_remotes"), self._cache
        )
        self.test_repository = MongoRepository(
            self._database.get_collection("test"), self._cache
        )
        self.user_from_repository = MongoRepository(
            self._database.get_collection("user_froms"), self._cache
        )
        self.user_locale_repository = MongoRepository(
            self._database.get_collection("user_locales"), self._cache
        )
        self.user_platform_repository = MongoRepository(
            self._database.get_collection("user_platforms"), self._cache
        )
        self.user_profile_repository = MongoRepository(
            self._database.get_collection("user_profiles"), self._cache
        )
        self.socket_message_repository = MongoRepository(
            self._database.get_collection("socket_messages"), self._cache
        )
        self.user_socket_session_repository = MongoRepository(
            self._database.get_collection("user_socket_sessions"), self._cache
        )
