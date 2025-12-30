from pydantic import BaseModel
from pydantic import Field

from uuid import UUID

from app.schemas.dtos.message import MessageCreateRequestDTO
from app.schemas.codes.message import Role

class InsertMessageRequestBody(BaseModel):
    chat_id: str = Field(..., description="Chat ID")
    parent_message_id: str = Field(..., description="Parent message ID")
    content: str = Field(..., description="Content")

    def to_message_create_request_dto(self) -> MessageCreateRequestDTO:
        return MessageCreateRequestDTO(
            chat_id=UUID(self.chat_id),
            parent_message_id=UUID(self.parent_message_id),
            content=self.content,
            role=Role.USER,
        )