
from sqlalchemy import Column, ForeignKey, String
from src.domain.entities.entity import Entity
from src.domain.entities.utils import Base

class Category(Entity):
    __tablename__ = 'category'
    _id = Column(String(length=36),ForeignKey('entities._id') ,primary_key=True)
    name = Column(String(length=255))
    def __init__(
        self,
        _id: str,
        name: str):
        super().__init__(_id)
        self.name = name
    
