from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from src.domain.entities.utils import Base

class Category(Base):
    __tablename__ = 'Category'
    __back_populates__ = 'categories'
    _id = Column(String(length=36) ,primary_key=True, nullable=False)
    name = Column(String(length=255), nullable=False)
    products = relationship("Product", back_populates=__back_populates__)

    def __init__(
        self,
        _id: str, name: str):
        self._id = _id
        self.name = name
    
