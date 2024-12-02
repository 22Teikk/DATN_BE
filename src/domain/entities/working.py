from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

class Working():
    def __init__(self, _id: str, user_id: str, order_id: str, type: str, date: str):
        self._id = _id
        self.user_id = user_id
        self.order_id = order_id
        self.type = type
        self.date = date