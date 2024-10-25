from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List

from src.adapters.repositories.entity_cache import EntityCache


class EntityRepository(EntityCache):
    @abstractmethod
    def find_by_query(self, query: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        """Tìm kiếm bản ghi theo truy vấn."""
        pass

    @abstractmethod
    def find_by_id(self, _id: Any) -> Dict[str, Any]:
        """Tìm kiếm bản ghi theo ID."""
        pass

    @abstractmethod
    def insert(self, data: Dict[str, Any]) -> int:
        """Chèn một bản ghi mới vào bảng."""
        pass

    @abstractmethod
    def update(self, data: Dict[str, Any]) -> int:
        """Cập nhật bản ghi đã tồn tại."""
        pass

    @abstractmethod
    def upserts(self, datas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Chèn hoặc cập nhật nhiều bản ghi."""
        pass

    @abstractmethod
    def delete(self, _id: Any) -> int:
        """Xóa bản ghi theo ID."""
        pass

    @abstractmethod
    def chunk(
        self,
        query: Dict[str, Any] = {},
        chunk_size: int = 10000,
        on_data_ready: Callable[[List[Dict[str, Any]]], None] = lambda x: None,
    ):
        """Lấy dữ liệu theo từng khối."""
        pass

    @abstractmethod
    def clean(self) -> int:
        """Xóa tất cả bản ghi trong bảng."""
        pass

    @abstractmethod
    def get_table_manager(self):
        """Lấy quản lý bảng (session hoặc table)."""
        pass