import datetime
import uuid

from app.db.base import Base

from sqlalchemy import Column
from sqlalchemy import SmallInteger
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

class Message(Base):
    __tablename__ = "messages"
    
    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), nullable=False)

    parent_message_id = Column(UUID(as_uuid=True), nullable=True)
    content = Column(String, nullable=False)
    role = Column(SmallInteger, nullable=False)
    
    created_dt = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_dt = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )