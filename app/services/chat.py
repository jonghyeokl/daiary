from uuid import UUID
from typing import List
from fastapi import Depends
from fastapi import HTTPException
import os
import requests

from app.repositories.message import MessageRepository
from app.repositories.chat import ChatRepository
from app.repositories.setting import SettingRepository
from app.schemas.dtos.message import MessageCreateRequestDTO
from app.schemas.dtos.chat import ChatCreateRequestDTO
from app.schemas.model_dtos.message import MessageModelDTO
from app.schemas.model_dtos.chat import ChatModelDTO
from app.schemas.codes.message import Role
from app.utils.chatting_prompts import get_initial_message

INITIAL_MESSAGE = "안녕!👋 오늘 재미있는 일 없었어?"

class ChatService:
    def __init__(
        self,
        message_repository: MessageRepository,
        chat_repository: ChatRepository,
        setting_repository: SettingRepository,
    ) -> None:
        self.message_repository = message_repository
        self.chat_repository = chat_repository
        self.setting_repository = setting_repository
    
    @classmethod
    def build(cls, message_repository: MessageRepository = Depends(MessageRepository.build), chat_repository: ChatRepository = Depends(ChatRepository.build), setting_repository: SettingRepository = Depends(SettingRepository.build)) -> "ChatService":
        return cls(message_repository=message_repository, chat_repository=chat_repository, setting_repository=setting_repository)

    async def create_chat_and_initial_message(self, user_id: UUID, chat_date: str) -> MessageModelDTO:
        chat = await self.chat_repository.create(ChatCreateRequestDTO(user_id=user_id, chat_date=chat_date))
        
        setting = await self.setting_repository.find_by_user_id(user_id)

        current_manner = setting.chat_manner if setting else 1
        dynamic_initial_message = get_initial_message(current_manner)
        return await self.message_repository.create(MessageCreateRequestDTO(chat_id=UUID(chat.chat_id), content=dynamic_initial_message, role=Role.MODEL, message_id=UUID(chat.root_message_id)))
        