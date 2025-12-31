from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from uuid import uuid4
from uuid import UUID
from typing import List

from app.db.session import get_db
from app.schemas.dtos.message import MessageCreateRequestDTO
from app.schemas.model_dtos.message import MessageModelDTO
from app.db.models.message.message import Message

class MessageRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    @classmethod
    def build(cls, db: AsyncSession = Depends(get_db)) -> "MessageRepository":
        return cls(db=db)
    
    async def create(self, message: MessageCreateRequestDTO) -> MessageModelDTO:
        now = datetime.utcnow()
        new_message = Message(
            message_id=message.message_id if message.message_id else uuid4(),
            chat_id=message.chat_id,
            parent_message_id=message.parent_message_id,
            content=message.content,
            role=message.role.value,
            created_dt=now,
            updated_dt=now,
        )
        self.db.add(new_message)

        await self.db.commit()
        
        return MessageModelDTO.from_model(new_message)
    
    async def get_by_message_id(self, message_id: UUID) -> MessageModelDTO:
        query = await self.db.execute(select(Message).where(Message.message_id == message_id))
        message = query.scalars().first()
        return MessageModelDTO.from_model(message)
    
    async def get_all_messages_by_chat_id(self, chat_id: UUID) -> List[MessageModelDTO]:
        query = await self.db.execute(select(Message).where(Message.chat_id == chat_id).order_by(Message.created_dt.asc()))
        messages = query.scalars().all()
        return [MessageModelDTO.from_model(message) for message in messages]