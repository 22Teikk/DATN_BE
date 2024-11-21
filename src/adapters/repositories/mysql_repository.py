from sqlalchemy import Table, create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import insert
from typing import Callable, Dict, List, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.adapters.repositories.entity_repository import EntityRepository

class MySQLRepository(EntityRepository):
    def __init__(self, session: Session, table: Table, cache, schema):
        self.session = session
        self.table = table
        self._cache = cache
        self.schema = schema

    def _handle_transaction_error(self, e):
        """Xử lý lỗi giao dịch."""
        print(f"Transaction error: {e}")
        if self.session.is_active:
            self.session.rollback()

    def find_by_query(self, query: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        """Tìm kiếm bản ghi theo truy vấn."""
        try:
            if query == {}:
                return self.session.query(self.table).all()
            return self.session.query(self.table).filter_by(**query).all()
        except SQLAlchemyError as e:
            print(f"Find by query error: {e}")
            return []

    def find_by_id(self, _id: Any) -> Dict[str, Any]:
        """Tìm kiếm bản ghi theo ID."""
        try:
            record = self.session.query(self.table).filter_by(_id=_id).first()
            return self.schema.dump(record) if record else {}
        except SQLAlchemyError as e:
            print(f"Find by ID error: {e}")
            return {}

    def insert(self, data: Dict[str, Any]) -> int:
        """Chèn một bản ghi mới vào bảng."""
        try:
            with self.session.begin():  # Tự động rollback nếu có lỗi
                stmt = insert(self.table).values(**data)
                result = self.session.execute(stmt)
                return result.inserted_primary_key[0]
        except IntegrityError:
            print(f"Integrity error during insert: {data}")
            return -1
        except SQLAlchemyError as e:
            print(f"Insert error: {e}")
            return -1

    def update(self, data: Dict[str, Any]) -> int:
        """Cập nhật bản ghi đã tồn tại."""
        try:
            data_update = {key: value for key, value in data.items() if key != '_sa_instance_state'}
            with self.session.begin():
                self.session.query(self.table).filter_by(_id=data['_id']).update(data_update)
            return data['_id']
        except SQLAlchemyError as e:
            print(f"Update error: {e}")
            return -1

    def upserts(self, datas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Chèn hoặc cập nhật nhiều bản ghi."""
        try:
            with self.session.begin():
                for data in datas:
                    stmt = insert(self.table).values(data).on_duplicate_key_update(**data)
                    self.session.execute(stmt)
            return {"status": "success"}
        except SQLAlchemyError as e:
            print(f"Upsert error: {e}")
            return {"status": "error", "error": str(e)}

    def delete(self, _id: Any) -> int:
        """Xóa bản ghi theo ID."""
        try:
            with self.session.begin():
                result = self.session.query(self.table).filter_by(_id=_id).delete()
            return result
        except SQLAlchemyError as e:
            print(f"Delete error: {e}")
            return -1

    def chunk(
        self,
        query: Dict[str, Any] = {},
        chunk_size: int = 10000,
        on_data_ready: Callable[[List[Dict[str, Any]]], None] = lambda x: None,
    ):
        """Lấy dữ liệu theo từng khối."""
        try:
            total_documents = self.session.query(self.table).filter_by(**query).count()
            for offset in range(0, total_documents, chunk_size):
                data_chunk = self.session.query(self.table).filter_by(**query).offset(offset).limit(chunk_size).all()
                on_data_ready(data_chunk)
        except SQLAlchemyError as e:
            print(f"Chunk error: {e}")

    def clean(self) -> int:
        """Xóa tất cả bản ghi trong bảng."""
        try:
            with self.session.begin():
                result = self.session.query(self.table).delete()
            return result
        except SQLAlchemyError as e:
            print(f"Clean error: {e}")
            return -1

    # Các phương thức liên quan đến cache không thay đổi.
    def get_cache_manager(self):
        return self._cache

    def find_by_dict(self, dict: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tìm kiếm bản ghi theo từ điển."""
        try:
            return self.session.query(self.table).filter_by(**dict).all()
        except SQLAlchemyError as e:
            print(f"Find by dict error: {e}")
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
        if not self.session.is_active:  # Session không hoạt động
            print("Session is not active. Resetting session state.")
            self.session.rollback()  # Đảm bảo mọi giao dịch lỗi trước đó được rollback
        if self.session.in_transaction():  # Đảm bảo không có giao dịch bị treo
            print("Session is in an invalid transaction state. Rolling back.")
            self.session.rollback()
        return self.session