import uuid
from src.domain.entities.utils import get_current_timestamp_str


class Entity:
    def __init__(self, _id: str):
        self._id = _id

    def get_updated(self):
        self.updated = get_current_timestamp_str()
        return self.updated

    def get_current_time(self):
        return get_current_timestamp_str()

    def get_new_uuid(self):
        return str(uuid.uuid4())
