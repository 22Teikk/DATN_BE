from sqlalchemy import Table, create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import insert
from typing import Callable, Dict, List, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.adapters.repositories.entity_repository import EntityRepository

class MySQLRepository(EntityRepository):
    def __init__(self, session: Session, table: Table, cache, schema):
        self.session = session
        self.table = table
        self._cache = cache
        self.schema = schema

    def find_by_query(self, query: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        """Tìm kiếm bản ghi theo truy vấn."""
        try:
            if query == {}:
                return self.session.query(self.table).all()
            else: 
                return self.session.query(self.table).filter_by(**query).all()
        except Exception as e:
            self.session.rollback()  # Ensure rollback on error
            print(f"Error in find_by_query: {e}")
            return []

    def find_by_id(self, _id: Any) -> Dict[str, Any]:
        """Tìm kiếm bản ghi theo ID."""
        try:
            return self.schema.dump(self.session.query(self.table).filter_by(_id=_id).first())
        except Exception as e:
            self.session.rollback()  # Ensure rollback on error
            print(f"Error in find_by_id: {e}")
            return {}

    def insert(self, data: Dict[str, Any]) -> int:
        """Chèn một bản ghi mới vào bảng."""
        try:
            stmt = insert(self.table).values(**data)
            result = self.session.execute(stmt)
            self.session.commit()  # Commit transaction
            return result.inserted_primary_key[0]
        except IntegrityError as e:
            self.session.rollback()  # Ensure rollback on integrity error
            print(f"Integrity error occurred during insert: {e}")
            return -1  # Handle integrity error
        except Exception as e:
            self.session.rollback()  # Ensure rollback on any other error
            print(f"Insert error: {e}")
            return -1  # Handle generic errors

    def update(self, data: Dict[str, Any]) -> int:
        """Cập nhật bản ghi đã tồn tại."""
        try:
            data_update = {key: value for key, value in data.items() if key != '_sa_instance_state'}
            print(data_update)
            self.session.query(self.table).filter_by(_id=data['_id']).update(data_update)
            self.session.commit()  # Commit transaction
            return data['_id']
        except Exception as e:
            self.session.rollback()  # Ensure rollback on error
            print(f"Update error: {e}")
            return -1  # Handle error

    def upserts(self, datas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Chèn hoặc cập nhật nhiều bản ghi."""
        try:
            for data in datas:
                stmt = insert(self.table).values(data).on_duplicate_key_update(**data)
                self.session.execute(stmt)
            self.session.commit()  # Commit transaction
            return {"status": "success"}
        except Exception as e:
            self.session.rollback()  # Ensure rollback on error
            print(f"Upsert error: {e}")
            return {"status": "error", "error": str(e)}

    def delete(self, _id: Any) -> int:
        """Xóa bản ghi theo ID."""
        try:
            result = self.session.query(self.table).filter_by(_id=_id).delete()
            self.session.commit()  # Commit transaction
            return result
        except Exception as e:
            self.session.rollback()  # Ensure rollback on error
            print(f"Delete error: {e}")
            return -1  # Handle error

    def chunk(
        self,
        query: Dict[str, Any] = {},
        chunk_size: int = 10000,
        on_data_ready: Callable[[List[Dict[str, Any]]], None] = lambda x: None,
    ):
        """Lấy dữ liệu theo từng khối."""
        total_documents = self.session.query(self.table).filter_by(**query).count()
        for offset in range(0, total_documents, chunk_size):
            data_chunk = self.session.query(self.table).filter_by(**query).offset(offset).limit(chunk_size).all()
            on_data_ready(data_chunk)

    def clean(self) -> int:
        """Xóa tất cả bản ghi trong bảng."""
        try:
            result = self.session.query(self.table).delete()
            self.session.commit()  # Commit transaction
            return result
        except Exception as e:
            self.session.rollback()  # Ensure rollback on error
            print(f"Clean error: {e}")
            return -1  # Handle error

    # Cache methods
    def get_cache_manager(self):
        return self._cache

    def find_by_dict(self, dict: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tìm kiếm bản ghi theo từ điển."""
        try:
            return self.session.query(self.table).filter_by(**dict).all()
        except Exception as e:
            self.session.rollback()  # Ensure rollback on error
            print(f"Error in find_by_dict: {e}")
            return []

    def get_table_manager(self):
        """Lấy quản lý bảng (session hoặc table)."""
        return self.table

    def set_cache(self, key: str, values: List[Dict], expire: int = 0, cache_db: int = 0, chunk_size: int = 10000):
        pass

    def get_cache(self, key: str) -> List[Dict]:
        pass

    def find_cache_keys(self, key_pattern: str) -> List[str]:
        pass

    def delete_cache(self, key_pattern: str):
        pass

    def clean_cache(self):
        pass

    def get_session_manager(self):
        return self.session

