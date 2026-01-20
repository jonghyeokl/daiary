from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime
from uuid import uuid4
from uuid import UUID

from app.db.session import get_db
from app.schemas.dtos.chat import ChatCreateRequestDTO
from app.schemas.model_dtos.chat import ChatModelDTO
from app.db.models.chat.chat import Chat

class ChatRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    @classmethod
    def build(cls, db: AsyncSession = Depends(get_db)) -> "ChatRepository":
        return cls(db=db)
    
    async def create(self, chat: ChatCreateRequestDTO) -> ChatModelDTO:
        now = datetime.utcnow()
        new_chat = Chat(
            chat_id=uuid4(),
            user_id=chat.user_id,
            root_message_id=uuid4(),
            chat_date=chat.chat_date,
            rating=None,
            created_dt=now,
            updated_dt=now,
        )
        self.db.add(new_chat)

        await self.db.commit()
        
        return ChatModelDTO.from_model(new_chat)
    
    async def get_by_chat_id(self, chat_id: UUID) -> ChatModelDTO:
        query = await self.db.execute(select(Chat).where(Chat.chat_id == chat_id))
        chat = query.scalars().first()
        return ChatModelDTO.from_model(chat)

    async def get_all_chats_by_user_id(self, user_id: UUID) -> List[ChatModelDTO]:
        query = await self.db.execute(select(Chat).where(Chat.user_id == user_id))
        chats = query.scalars().all()
        return [ChatModelDTO.from_model(chat) for chat in chats]
    
    async def rating(self, chat_id: UUID, rating: int) -> None:
        query = await self.db.execute(select(Chat).where(Chat.chat_id == chat_id))
        chat = query.scalars().first()
        chat.rating = rating
        chat.updated_dt = datetime.utcnow()
        await self.db.commit()