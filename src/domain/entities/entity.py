import uuid

from sqlalchemy import Column, String
from src.domain.entities.utils import get_current_timestamp_str
from src.domain.entities.utils import Base

class Entity(Base):
    __tablename__ = 'entities'
    _id = Column(String(length=36), primary_key=True)
    def __init__(self, _id: str):
        self._id = _id

    def get_updated(self):
        self.updated = get_current_timestamp_str()
        return self.updated

    def get_current_time(self):
        return get_current_timestamp_str()

    def get_new_uuid(self):
        return str(uuid.uuid4())
