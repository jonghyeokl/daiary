from uuid import UUID
from typing import List
from fastapi import Depends
from fastapi import HTTPException
import os
import requests

from app.repositories.message import MessageRepository
from app.repositories.chat import ChatRepository
from app.schemas.dtos.message import MessageCreateRequestDTO
from app.schemas.dtos.chat import ChatCreateRequestDTO
from app.schemas.model_dtos.message import MessageModelDTO
from app.schemas.model_dtos.chat import ChatModelDTO
from app.schemas.codes.message import Role

INITIAL_MESSAGE = "안녕!👋 오늘 재미있는 일 없었어?"

class ChatService:
    def __init__(
        self,
        message_repository: MessageRepository,
        chat_repository: ChatRepository,
    ) -> None:
        self.message_repository = message_repository
        self.chat_repository = chat_repository
    
    @classmethod
    def build(cls, message_repository: MessageRepository = Depends(MessageRepository.build), chat_repository: ChatRepository = Depends(ChatRepository.build)) -> "ChatService":
        return cls(message_repository=message_repository, chat_repository=chat_repository)

    async def create_chat_and_initial_message(self, user_id: UUID, chat_date: str) -> MessageModelDTO:
        chat = await self.chat_repository.create(ChatCreateRequestDTO(user_id=user_id, chat_date=chat_date))
        return await self.message_repository.create(MessageCreateRequestDTO(chat_id=UUID(chat.chat_id), content=INITIAL_MESSAGE, role=Role.MODEL, message_id=UUID(chat.root_message_id)))
        