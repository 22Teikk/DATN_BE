
import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from src.domain.entities.utils import Base

class UserProfile(Base):
    __tablename__ = 'User'
    __back_populates__ = 'users'
    _id = Column(String(length=36) ,primary_key=True)
    name = Column(String(length=255), nullable=False)
    username = Column(String(length=255), unique=True, nullable=False)
    password = Column(String(length=255), nullable=False)
    address = Column(String(length=255), nullable=False)
    description = Column(String(length=255), nullable=False)
    role_id = Column(String(length=36), ForeignKey('Role._id'), nullable=False)
    lat = Column(Float, nullable=True)
    long = Column(Float, nullable=True)
    email = Column(String(length=255), unique=True, nullable=False)
    phone = Column(String(length=255), nullable=False)
    image_url = Column(String(length=100),
                        nullable=True)
    created_at = Column(DateTime(), nullable=False)
    store_id = Column(String(length=36), ForeignKey('Store._id'), nullable=True)
    roles = relationship("Role", back_populates=__back_populates__)
    stores = relationship("Store", back_populates=__back_populates__)
    wishlists = relationship("Wishlist", back_populates=__back_populates__)
    carts = relationship("Cart", back_populates=__back_populates__)
    orders = relationship("Order", back_populates=__back_populates__)
    feedbacks = relationship("Feedback", back_populates='users')
    def __init__(
        self, 
        _id: str,
        name: str,
        username: str,
        password: str,
        address: str,
        description: str,
        role_id: str,
        email: str,
        phone: str,
        long: float = None,
        lat: float = None,
        image_url: str = None,
        created_at: datetime.datetime = None,
        store_id: str = None,
        ):
        self._id = _id
        self.name = name
        self.username = username
        self.password = password
        self.address = address
        self.description = description
        self.role_id = role_id
        self.lat = lat
        self.long = long
        self.email = email
        self.phone = phone
        self.image_url = image_url if image_url else None
        self.created_at = created_at if isinstance(created_at, datetime.datetime) else datetime.datetime.fromisoformat(created_at) 
        self.store_id = store_id if store_id else None