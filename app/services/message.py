from fastapi import Depends
from fastapi import HTTPException
from typing import List
import requests
import os
from uuid import UUID

from app.repositories.message import MessageRepository
from app.repositories.setting import SettingRepository
from app.schemas.model_dtos.message import MessageModelDTO
from app.schemas.dtos.message import MessageCreateRequestDTO
from app.schemas.dtos.message import MessageHistoryDTO
from app.schemas.codes.message import Role
from app.schemas.codes.setting import ChatManner
from app.utils.chatting_prompts import get_system_instruction

class MessageService:
    def __init__(
        self,
        message_repository: MessageRepository,
        setting_repository: SettingRepository,
    ) -> None:
        self.message_repository = message_repository
        self.setting_repository = setting_repository
    
    @classmethod
    def build(cls, message_repository: MessageRepository = Depends(MessageRepository.build), setting_repository: SettingRepository = Depends(SettingRepository.build)) -> "MessageService":
        return cls(message_repository=message_repository, setting_repository=setting_repository)

    async def get_from_genai_and_insert_message(self, request_body: MessageCreateRequestDTO, user_id: UUID) -> MessageModelDTO:
        current_message = await self.message_repository.create(request_body)

        prev_messages = await self.get_prev_messages(UUID(current_message.message_id))

        genai_response = await self.get_from_genai(prev_messages, user_id)

        return await self.message_repository.create(MessageCreateRequestDTO(
            chat_id=current_message.chat_id,
            parent_message_id=current_message.message_id,
            content=genai_response,
            role=Role.MODEL,
        ))
    
    async def get_prev_messages(self, message_id: UUID) -> List[MessageHistoryDTO]:
        messages = []
        current_message = await self.message_repository.get_by_message_id(message_id)
        iterations = 0
        while current_message.parent_message_id is not None and iterations < 19:
            messages.append(MessageHistoryDTO(role=current_message.role.name, content=current_message.content))
            current_message = await self.message_repository.get_by_message_id(UUID(current_message.parent_message_id))
            iterations += 1
        messages.append(MessageHistoryDTO(role=current_message.role.name, content=current_message.content))
        return messages[::-1]
    
    async def get_from_genai(self, prev_messages: List[MessageHistoryDTO], user_id: UUID) -> str:
        
        setting = await self.setting_repository.find_by_user_id(user_id)

        current_manner = setting.chat_manner if setting else 1

        dynamic_system_instruction = get_system_instruction(current_manner)

        API_KEY = os.getenv("GENAI_API_KEY")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
        headers = {
            'Content-Type': 'application/json'
        }
        contents = []
        for message in prev_messages:
            contents.append({
                "role": message.role,
                "parts": [{ "text": message.content }]
            })
        data = {
            "system_instruction": {
                "parts": [
                    { "text": dynamic_system_instruction }
                ]
            },
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            print(response.text)
            raise HTTPException(status_code=response.status_code, detail="genai api error")
        
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
