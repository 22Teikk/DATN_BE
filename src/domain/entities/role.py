
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from src.domain.entities.utils import Base

class Role(Base):
    __tablename__ = 'Role'
    __back_populates__ = 'roles'
    _id = Column(String(length=36) ,primary_key=True)
    name = Column(String(length=255), nullable=False)
    # users = relationship("User", back_populates=__back_populates__)
    def __init__(
        self, 
        _id: str,
        name: str):
        self._id = _id
        self.name = name
