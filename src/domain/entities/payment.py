
import datetime
from sqlalchemy import DECIMAL, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from src.domain.entities.utils import Base

class Payment(Base):
    __tablename__ = 'Payment'
    __back_populates__ = 'payments'
    _id = Column(String(length=36) ,primary_key=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime(), nullable=False)
    payment_method_id = Column(String(length=36), ForeignKey('PaymentMethod._id'), nullable=False)
    payment_methods = relationship("PaymentMethod", back_populates=__back_populates__)
    orders = relationship("Order", back_populates=__back_populates__)
    def __init__(
        self, 
        _id: str,
        amount: float, 
        payment_method_id: str,
        created_at: datetime.datetime = None):
        self._id = _id
        self.amount = amount
        self.created_at = created_at if isinstance(created_at, datetime.datetime) else datetime.datetime.fromisoformat(created_at)
        self.payment_method_id = payment_method_id
    
