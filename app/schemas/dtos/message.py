from dataclasses import dataclass
from typing import Optional

from uuid import UUID

from app.schemas.codes.message import Role

@dataclass
class MessageCreateRequestDTO:
    chat_id: UUID
    content: str
    role: Role
    message_id: Optional[UUID] = None
    parent_message_id: Optional[UUID] = None

@dataclass
class MessageHistoryDTO:
    role: str
    content: str
