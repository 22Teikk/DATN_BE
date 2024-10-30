
import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.domain.entities.utils import Base

class Order(Base):
    __tablename__ = 'Order'
    __back_populates__ = 'orders'
    _id = Column(String(length=36) ,primary_key=True)
    created_at = Column(DateTime(), nullable=False)
    status = Column(String(length=50), nullable=False)
    total = Column(Integer, nullable=False)
    lat = Column(Float, nullable=True)
    long = Column(Float, nullable=True)
    is_shipment = Column(Boolean, nullable=False)
    user_id = Column(String(length=36), ForeignKey('User._id'))
    payment_id = Column(String(length=36), ForeignKey('Payment._id'))
    users = relationship("UserProfile", back_populates=__back_populates__)
    payments = relationship("Payment", back_populates=__back_populates__)

    def __init__(
        self, 
        _id: str,
        status: str,
        total: int,
        user_id: str,
        payment_id: str,
        is_shipment: bool,
        created_at: datetime.datetime = None,
        lat: float = None,
        long: float = None,
        ):
        self._id = _id
        self.status = status
        self.total = total
        self.created_at = created_at if created_at else datetime.datetime.now()
        self.is_shipment = is_shipment
        self.user_id = user_id
        self.payment_id = payment_id
        self.lat = lat
        self.long = long