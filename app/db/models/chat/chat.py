import datetime
import uuid

from app.db.base import Base

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import SmallInteger
from sqlalchemy import ForeignKey
from sqlalchemy import CheckConstraint
from sqlalchemy.dialects.postgresql import UUID

class Chat(Base):
    __tablename__ = "chats"

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 10', name='check_rating_range'),
    )
    
    chat_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.user_id"), nullable=False)

    root_message_id = Column(UUID(as_uuid=True), nullable=False)
    chat_date = Column(String, nullable=False)
    rating = Column(SmallInteger(), nullable=True)
    
    created_dt = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_dt = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )