
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from src.domain.entities.utils import Base

class PaymentMethod(Base):
    __tablename__ = 'PaymentMethod'
    __back_populates__ = 'payment_methods'
    _id = Column(String(length=36) ,primary_key=True)
    name = Column(String(length=255), nullable=False)
    image_url = Column(String(length=255), nullable=False)
    payments = relationship("Payment", back_populates=__back_populates__)
    def __init__(self, _id: str, name: str, image_url: str):
        self._id = _id
        self.name = name
        self.image_url = image_url