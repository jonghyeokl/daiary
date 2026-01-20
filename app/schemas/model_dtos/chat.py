from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.db.models.chat.chat import Chat

class ChatModelDTO(BaseModel):
    chat_id: str
    user_id: str
    root_message_id: str
    chat_date: str
    rating: Optional[int] = None
    created_dt: datetime
    updated_dt: datetime

    @classmethod
    def from_model(cls, model: Chat) -> "ChatModelDTO":
        return cls(
            chat_id=str(model.chat_id),
            user_id=str(model.user_id),
            root_message_id=str(model.root_message_id),
            chat_date=model.chat_date,
            rating=model.rating,
            created_dt=model.created_dt,
            updated_dt=model.updated_dt,
        )