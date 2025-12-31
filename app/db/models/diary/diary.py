import datetime
import uuid

from app.db.base import Base

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey

class Diary(Base):
    __tablename__ = "diaries"
    
    diary_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(
        ForeignKey("chats.chat_id"), nullable=False
    )
    
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)

    created_dt = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_dt = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )