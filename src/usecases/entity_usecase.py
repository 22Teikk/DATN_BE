from src.domain.services.entity_service import EntityService


class EntityUsecase:
    def __init__(self, service: EntityService):
        self.service = service

    def find_by_dict(self, query: dict) -> list[dict]:
        return self.service.find_by_dict(query)

    def find_by_query(self, query: dict = {}) -> list[dict]:
        return self.service.find_by_query(query)

    def find_by_id(self, _id) -> dict:
        return self.service.find_by_id(_id)

    def insert(self, data: dict) -> int:
        return self.service.insert(data)

    def upserts(self, datas: list[dict]) -> dict:
        return self.service.upserts(datas)

    def update(self, data: dict) -> dict:
        return self.service.update(data)

    def delete(self, _id) -> int:
        return self.service.delete(_id)

    def chunk(self, data, chunk_size):
        return self.service.chunk(data, chunk_size)

    def clean(self):
        return self.service.clean()

    def set_cache(
        self,
        key: str,
        values: list[dict],
        expire:int=0 ,
        cache_db: int = 0,
        chunk_size: int = 10000,
    ):
        return self.service.set_cache(key, values, expire, cache_db, chunk_size)

    def get_cache(self, key: str) -> list[dict]:
        return self.service.get_cache(key)

    def find_cache_keys(self, key_pattern: str) -> list[str]:
        return self.service.find_cache_keys(key_pattern)

    def delete_cache(self, key_pattern: str):
        return self.service.delete_cache(key_pattern)

    def clean_cache(self):
        return self.service.clean_cache()
