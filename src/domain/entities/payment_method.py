
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from src.domain.entities.utils import Base

class PaymentMethod(Base):
    __tablename__ = 'PaymentMethod'
    __back_populates__ = 'payment_methods'
    _id = Column(String(length=36) ,primary_key=True)
    name = Column(String(length=255), nullable=False)
    def __init__(self, _id: str, name: str):
        self._id = _id
        self.name = name