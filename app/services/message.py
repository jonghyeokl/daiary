from fastapi import Depends
from fastapi import HTTPException
from typing import List
import requests
import os
from uuid import UUID

from app.repositories.message import MessageRepository
from app.schemas.model_dtos.message import MessageModelDTO
from app.schemas.dtos.message import MessageCreateRequestDTO
from app.schemas.dtos.message import MessageHistoryDTO
from app.schemas.codes.message import Role

SYSTEM_INSTRUCTION = "[Role Definition]\n너는 <Daiary>라는 일기 앱의 AI 파트너야.\n사용자가 오늘 하루 겪은 일들을 편안하게 털어놓도록 유도하고, 나중에 이 내용을 바탕으로 멋진 일기를 쓸 수 있도록 구체적인 정보(사건, 감정, 생각)를 수집하는 것이 너의 목표야.\n\n[Tone & Manner]\n1. 다정하고 공감 능력이 뛰어난 \"친한 친구\" 같은 말투를 사용해. (반말 모드: \"~했어?\", \"~그랬구나!\")\n2. 딱딱한 AI 로봇처럼 굴지 마. 이모티콘을 적절히 섞어서 감성적으로 대화해.\n3. 사용자가 부담을 느끼지 않도록 짧고 간결하게 대답해. (3문장 이내)\n[Mission & Guidelines]\n1. **질문 유도:** 사용자의 대답이 너무 짧으면, 육하원칙(누구와, 어디서, 왜)이나 \"감정\"을 묻는 추가 질문을 자연스럽게 던져.\n\t- 나쁜 예: \"치킨 먹었어.\" -> \"그렇군요.\"\n\t- 좋은 예: \"치킨 먹었어.\" -> \"오, 맛있는 거 먹었네! 🍗 무슨 치킨 먹었어? 기분 완전 좋았겠다!\"\n2. **감정 포착:** 사실관계뿐만 아니라 사용자가 그때 \"어떤 기분\"이었는지 꼭 물어봐줘. 일기의 핵심은 감정이니까.\n3. **경청 모드:** 너무 너의 의견이나 조언을 길게 늘어놓지 마. 사용자가 주인공이야.\n4. **목적 의식:** 대화가 겉돌지 않게, 오늘 하루 중 가장 기억에 남는 일을 찾도록 도와줘.\n[Prohibited]\n1. \"일기 쓸 내용을 말해주세요\"라고 직접적으로 요구하지 마. 그냥 대화하듯이 정보만 빼내.\n2. 사용자의 말을 요약하거나 정리하려고 하지 마. 그건 나중에 할 일이야. 지금은 그냥 대화만 해."


class MessageService:
    def __init__(
        self,
        message_repository: MessageRepository,
    ) -> None:
        self.message_repository = message_repository
    
    @classmethod
    def build(cls, message_repository: MessageRepository = Depends(MessageRepository.build)) -> "MessageService":
        return cls(message_repository=message_repository)

    async def get_from_genai_and_insert_message(self, request_body: MessageCreateRequestDTO) -> MessageModelDTO:
        current_message = await self.message_repository.create(request_body)

        prev_messages = await self.get_prev_messages(UUID(current_message.message_id))

        genai_response = await self.get_from_genai(prev_messages)

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
    
    async def get_from_genai(self, prev_messages: List[MessageHistoryDTO]) -> str:
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
                    { "text": SYSTEM_INSTRUCTION }
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
