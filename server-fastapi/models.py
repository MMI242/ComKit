from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum


class ItemType(str, enum.Enum):
    BORROW = "borrow"
    SHARE = "share"


class ItemStatus(str, enum.Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"


class RequestStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    RETURNED = "returned"
    CANCELLED = "cancelled"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    address = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("Item", back_populates="owner", cascade="all, delete-orphan")
    requests = relationship(
        "Request", back_populates="requester", cascade="all, delete-orphan"
    )


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    qty = Column(Integer, nullable=False)
    remaining_qty = Column(Integer, nullable=False)
    unit = Column(String(20), default="pcs")
    photo_url = Column(String(255), nullable=True)
    thumbnail_url = Column(String(255), nullable=True)
    type = Column(Enum(ItemType), nullable=False)
    status = Column(Enum(ItemStatus), default=ItemStatus.AVAILABLE)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="items")
    requests = relationship(
        "Request", back_populates="item", cascade="all, delete-orphan"
    )


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    requested_qty = Column(Integer, nullable=False)
    date_start = Column(String(10), nullable=False)
    date_end = Column(String(10), nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    item = relationship("Item", back_populates="requests")
    requester = relationship("User", back_populates="requests")
