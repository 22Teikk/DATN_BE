from src.adapters.repositories.entity_cache import EntityCache
from src.adapters.repositories.entity_repository import EntityRepository
from src.domain.services.entity_service import EntityService


class EntityServiceImpl(EntityService):
    def __init__(self, entity_repository: EntityRepository):
        self.entity_repository = entity_repository
        self.entity_cache = entity_repository.get_cache_manager()

    def find_by_query(self, query: dict = ...) -> list[dict]:
        return self.entity_repository.find_by_query(query)

    def find_by_id(self, _id):
        return self.entity_repository.find_by_id(_id)

    def update(self, data: dict) -> int:
        return self.entity_repository.update(data)

    def upserts(self, datas) -> dict:
        return self.entity_repository.upserts(datas)

    def insert(self, data: dict) -> int:
        return self.entity_repository.insert(data)

    def delete(self, _id):
        return self.entity_repository.delete(_id)

    def chunk(self, data, chunk_size):
        return self.entity_repository.chunk(data, chunk_size)

    def clean(self):
        return self.entity_repository.clean()

    def set_cache(self, key: str, values: list[dict], expire:int=0 ):
        return self.entity_cache.set_cache(key, values, expire)

    def get_cache(self, key: str) -> list[dict]:
        return self.entity_cache.get_cache(key)

    def find_cache_keys(self, key_pattern: str) -> list[str]:
        return self.entity_cache.find_cache_keys(key_pattern)

    def delete_cache(self, key_pattern: str):
        return self.entity_cache.delete_cache(key_pattern)

    def clean_cache(self):
        return self.entity_cache.clean_cache()

    def get_cache_manager(self):
        return self.entity_cache.get_cache_manager()

    def get_collection_manager(self):
        return self.entity_repository.get_collection_manager()

    def get_session_manager(self):
        return self.entity_repository.get_session_manager()