
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
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)
    email = Column(String(length=255), unique=True, nullable=False)
    phone = Column(String(length=255), nullable=False)
    image_id = Column(String(length=36),
                    #    ForeignKey('Image._id'),
                        nullable=True)
    created_at = Column(DateTime(), nullable=False)
    roles = relationship("Role", back_populates=__back_populates__)
    # images = relationship("Image", back_populates=__back_populates__)
    def __init__(
        self, 
        _id: str,
        name: str,
        username: str,
        password: str,
        address: str,
        description: str,
        role_id: str,
        lat: float,
        long: float,
        email: str,
        phone: str,
        image_id: str = None,
        created_at: datetime.datetime = None,
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
        self.image_id = image_id if image_id else None
        self.created_at = created_at if isinstance(created_at, datetime.datetime) else datetime.datetime.fromisoformat(created_at) 