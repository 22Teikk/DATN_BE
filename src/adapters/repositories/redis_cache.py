import json
from src.adapters.repositories.entity_cache import EntityCache
from src.adapters.database.redis import Redis


class RedisCache(EntityCache):

    def __init__(self, redis: Redis):
        self.redis = redis

    def set_cache(
        self,
        key: str,
        value: list[dict],
        expire: int=0,
        cache_db: int = 0,
        chunk_size: int = 50000,
    ):
        if cache_db == None:
            cache_db = 0
        # Đếm số lượng phần tử trong danh sách
        num_rows = len(value)

        # Chia nhỏ danh sách nếu cần
        if num_rows <= chunk_size:
            data_chunks = [value]
        else:
            data_chunks = [
                value[i : i + chunk_size] for i in range(0, num_rows, chunk_size)
            ]

        # Lưu từng chunk vào Redis
        for i, chunk in enumerate(data_chunks):
            redis_key = f"{key}:{i}"
            chunk_data = json.dumps(chunk)  # Chuyển đổi chunk thành chuỗi JSON

            # Chọn set hoặc setex tùy thuộc vào expire
            if expire>0:
                self.redis.get_cache_db(cache_db).setex(redis_key, expire, chunk_data)
            else:
                self.redis.get_cache_db(cache_db).set(redis_key, chunk_data)

            print(f"Set cache for {redis_key} with {len(chunk)} items")

    def get_cache(self, key: str, cache_db: int = 0) -> list[dict]:
        chunks = []
        i = 0
        while True:
            redis_key = f"{key}:{i}"
            data = self.redis.get_cache_db(cache_db).get(
                redis_key
            )  # Đọc dữ liệu từ Redis
            if data:
                print(f"get cache {key} {i}")
                data = data.decode("utf-8")
                chunk_df = json.loads(data)
                chunks.extend(chunk_df)
                i += 1
            else:
                break
        if chunks:
            return chunks
        else:
            print(f'Not found data with key "{key}".')
            return None

    def delete_cache(self, key: str, cache_db: int = 0):
        keys = self.redis.get_cache_db(cache_db).keys(f"{key}:*")
        if len(keys) > 0:
            for key in keys:
                self.redis.get_cache_db(cache_db).delete(key)

    def find_cache_keys(self, key_pattern: str, cache_db: int = 0) -> list[str]:
        return self.redis.get_cache_db(cache_db).keys(key_pattern)

    def clean_cache(self, cache_db: int = 0):
        self.redis.get_cache_db(cache_db).flushall()

    def get_cache_manager(self):
        return self
