from datetime import datetime

from pydantic import BaseModel
from typing import Optional

from app.db.models.message.message import Message
from app.schemas.codes.message import Role

class MessageModelDTO(BaseModel):
    message_id: str
    chat_id: str
    parent_message_id: Optional[str] = None
    content: str
    role: Role
    created_dt: datetime
    updated_dt: datetime

    @classmethod
    def from_model(cls, model: Message) -> "MessageModelDTO":
        return cls(
            message_id=str(model.message_id),
            chat_id=str(model.chat_id),
            parent_message_id=str(model.parent_message_id) if model.parent_message_id else None,
            content=model.content,
            role=Role.from_int(model.role),
            created_dt=model.created_dt,
            updated_dt=model.updated_dt,
        )