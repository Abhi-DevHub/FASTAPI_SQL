import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm  import declarative_base
from sqlalchemy.sql import func
from src.models.base import Base
from src.utils.utils import generate_uuid

class Bookmark(Base):
    __tablename__ = 'bookmarks'
    id = Column(String(512), primary_key=True, index=True, default=lambda: generate_uuid())
    original_url = Column(Text)
    short_code = Column(String(10), unique=True, index=True)
    visits = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(String(512), ForeignKey('users.id'), nullable=True)

    __table_args__ = (
        Index('ix_bookmarks_short_code', 'short_code'),
        Index('ix_bookmarks_user_id', 'user_id', 'created_at')
    )