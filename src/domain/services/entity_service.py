from abc import ABC, abstractmethod


class EntityService(ABC):
    @abstractmethod
    def find_by_query(self, query: dict = {}) -> list[dict]:
        pass

    @abstractmethod
    def find_by_id(self, _id) -> dict:
        pass

    @abstractmethod
    def find_by_dict(self, dict: dict):
        pass

    @abstractmethod
    def upserts(self, datas) -> dict:
        pass

    @abstractmethod
    def update(self, data: dict) -> dict:
        pass

    @abstractmethod
    def insert(self, data: dict) -> dict:
        pass

    @abstractmethod
    def delete(self, _id):
        pass

    @abstractmethod
    def chunk(self, data, chunk_size):
        pass

    @abstractmethod
    def clean(self):
        pass

    @abstractmethod
    def set_cache(
        self,
        key: str,
        values: list[dict],
        expire:int=0 ,
        cache_db: int = 0,
        chunk_size: int = 10000,
    ):
        pass

    @abstractmethod
    def get_cache(self, key: str) -> list[dict]:
        pass

    @abstractmethod
    def find_cache_keys(self, key_pattern: str) -> list[str]:
        pass

    @abstractmethod
    def delete_cache(self, key_pattern: str):
        pass

    @abstractmethod
    def clean_cache(self):
        pass

    @abstractmethod
    def get_cache_manager(self):
        pass

    @abstractmethod
    def get_collection_manager(self):
        pass
