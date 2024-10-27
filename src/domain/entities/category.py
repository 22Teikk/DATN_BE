
from sqlalchemy import Column, ForeignKey, String
from src.domain.entities.entity import Entity
from sqlalchemy.orm import relationship
from src.domain.entities.utils import Base

class Category(Base):
    __tablename__ = 'category'
    _id = Column(String(length=36) ,primary_key=True)
    name = Column(String(length=255))
    # entity = relationship("Entity", backref="category")

    def __init__(
        self,
        _id: str,
        name: str):
        # super().__init__(_id)
        self._id = _id
        self.name = name
    
