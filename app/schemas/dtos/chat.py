from dataclasses import dataclass

from uuid import UUID

@dataclass
class ChatCreateRequestDTO:
    user_id: UUID
    chat_date: str