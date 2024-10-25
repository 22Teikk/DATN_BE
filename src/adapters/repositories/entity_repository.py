from abc import ABC, abstractmethod
from typing import Callable

from src.adapters.repositories.entity_cache import EntityCache


class EntityRepository(EntityCache):
    @abstractmethod
    def find_by_query(self, query: dict = {}) -> list[dict]:
        pass

    @abstractmethod
    def find_by_id(self, _id):
        pass

    @abstractmethod
    def find_by_dict(self, dict: dict):
        pass

    @abstractmethod
    def insert(self, data: dict) -> int:
        pass

    @abstractmethod
    def update(self, data: dict) -> int:
        pass

    @abstractmethod
    def upserts(self, datas: list[dict]) -> dict:
        pass

    @abstractmethod
    def delete(self, _id):
        pass

    @abstractmethod
    def chunk(
        self,
        query: dict = {},
        chunk_size: int = 10000,
        on_data_ready: Callable[[list[dict]], None] = lambda x: None,
    ):
        pass

    @abstractmethod
    def clean(self):
        pass

    @abstractmethod
    def get_collection_manager(self):
        pass