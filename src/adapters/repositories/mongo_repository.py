import json
from typing import Callable
import numpy as np
from pymongo import UpdateOne
from src.adapters.repositories.entity_cache import EntityCache
from src.adapters.repositories.entity_repository import EntityRepository
from pymongo.collection import Collection
from flask import jsonify
import redis
from src.domain.entities.utils import get_md5_from_str



class MongoRepository(EntityRepository):
    def __init__(self, collection: Collection, cache: EntityCache):
        self._collection = collection
        self._cache = cache

    def update(self, data: dict) -> dict:
        return self._collection.update_one(
            {"_id": data["_id"]}, {"$set": data}
        ).raw_result

    def chunk(
        self,
        query: dict = {},
        chunk_size: int = 10000,
        on_data_ready: Callable[[list[dict]], None] = lambda x: None,
    ):
        total_documents = self._collection.count_documents(query)
        for skip in range(0, total_documents, chunk_size):
            cursor = self._collection.find(query).skip(skip).limit(chunk_size)
            data_chunk = list(cursor)
            on_data_ready(data_chunk)

    def find_by_query(self, query: dict = {}) -> list[dict]:
        total_documents = self._collection.count_documents(query)
        chunk_size = 10000
        datas = []
        for skip in range(0, total_documents, chunk_size):
            chunk = list(self._collection.find(query).skip(skip).limit(chunk_size))
            datas.extend(chunk)
        return datas if datas else []

    def find_by_id(self, _id: str) -> dict:
        return self._collection.find_one({"_id": str(_id)})

    def find_by_dict(self, dict: dict) -> list[dict]:
        return list(self._collection.find(dict))

    def insert(self, data) -> int:
        try:
            return self._collection.insert_one(data).inserted_id
        except Exception as e:
            print(f"insert error: {e}")
        return -1

    def upserts(self, datas) -> dict:
        items = [
            UpdateOne({"_id": data["_id"]}, {"$set": data}, upsert=True)
            for data in datas
        ]
        try:
            results = self._collection.bulk_write(items, ordered=False)
            return results.bulk_api_result
        except Exception as e:
            print(f"upserts error: {e}")
            pass
        return "Error"

    def delete(self, _id) -> dict:
        return self._collection.delete_one({"_id": _id}).deleted_count

    def clean(self):
        return self._collection.delete_many({}).deleted_count

    def get_collection_manager(self):
        return self._collection

    def get_cache_manager(self):
        return self._cache

    def set_cache(
        self,
        key: str,
        values: list[dict],
        expire:int=0 ,
        cache_db: int = 0,
        chunk_size: int = 10000,
    ):
        return self._cache.set_cache(key, values, expire, cache_db, chunk_size)

    def find_cache_keys(self, key_pattern: str) -> list[str]:
        return self._cache.find_cache_keys(key_pattern)

    def delete_cache(self, key_pattern: str):
        return self._cache.delete_cache(key_pattern)

    def clean_cache(self):
        return self._cache.clean_cache()

    def get_cache(self, key: str) -> list[dict]:
        return self._cache.get_cache(key)
