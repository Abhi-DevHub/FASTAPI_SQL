from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.utils.utils import generate_uuid
from sqlalchemy.sql import func

from src.models.base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(String(512), primary_key=True, index=True, default=lambda: generate_uuid())
    email = Column(String(128), unique=True, index=True)
    username = Column(String(56), unique=True, index=True)
    hash_password = Column(String(512))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
