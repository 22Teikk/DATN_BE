from sqlalchemy import Table, create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import insert

from src.adapters.repositories.entity_repository import EntityRepository

class MySQLRepository(EntityRepository):
    def __init__(self, table: Table, cache):
        self.table = table
        self._cache = cache

    def update(self, table, data: dict):
        try:
            self.session.query(table).filter_by(id=data['id']).update(data)
            self.session.commit()
            return {"status": "success"}
        except Exception as e:
            self.session.rollback()
            print(f"Update error: {e}")
            return {"status": "error", "error": str(e)}

    def chunk(self, table, chunk_size=10000, on_data_ready=lambda x: None):
        total_documents = self.session.query(table).count()
        for offset in range(0, total_documents, chunk_size):
            data_chunk = self.session.query(table).offset(offset).limit(chunk_size).all()
            on_data_ready(data_chunk)

    def find_by_query(self, table, query: dict = {}) -> list:
        return self.session.query(table).filter_by(**query).all()

    def find_by_id(self, table, _id: int):
        return self.session.query(table).filter_by(id=_id).first()

    def insert(self, table, data):
        try:
            self.session.add(table(**data))
            self.session.commit()
            return {"status": "success", "id": data.get('id')}
        except Exception as e:
            self.session.rollback()
            print(f"Insert error: {e}")
            return {"status": "error", "error": str(e)}

    def upserts(self, table, datas: list):
        try:
            for data in datas:
                stmt = insert(table).values(data).on_duplicate_key_update(data)
                self.session.execute(stmt)
            self.session.commit()
            return {"status": "success"}
        except Exception as e:
            self.session.rollback()
            print(f"Upsert error: {e}")
            return {"status": "error", "error": str(e)}

    def delete(self, table, _id: int):
        try:
            result = self.session.query(table).filter_by(id=_id).delete()
            self.session.commit()
            return result
        except Exception as e:
            self.session.rollback()
            print(f"Delete error: {e}")
            return {"status": "error", "error": str(e)}

    def clean(self, table):
        try:
            result = self.session.query(table).delete()
            self.session.commit()
            return result
        except Exception as e:
            self.session.rollback()
            print(f"Clean error: {e}")
            return {"status": "error", "error": str(e)}

    # Cache methods
    def get_cache_manager(self):
        return self._cache

    def get_table_manager(self):
        return self.session

    def set_cache(self, key, values, expire=0, cache_db=0, chunk_size=10000):
        return self._cache.set_cache(key, values, expire, cache_db, chunk_size)

    def find_cache_keys(self, key_pattern):
        return self._cache.find_cache_keys(key_pattern)

    def delete_cache(self, key_pattern):
        return self._cache.delete_cache(key_pattern)

    def clean_cache(self):
        return self._cache.clean_cache()

    def get_cache(self, key):
        return self._cache.get_cache(key)

    def find_by_dict(self, dict: dict):
        raise NotImplementedError

    def get_collection_manager(self):
        pass

