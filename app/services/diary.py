from fastapi import Depends
from fastapi import HTTPException
import os
import requests
from typing import List
from typing import Tuple
from uuid import UUID

from app.schemas.model_dtos.diary import DiaryModelDTO
from app.schemas.dtos.diary import DiaryCreateRequestDTO
from app.schemas.model_dtos.message import MessageModelDTO
from app.repositories.diary import DiaryRepository
from app.repositories.message import MessageRepository

SYSTEM_INSTRUCTION = """
[Role Definition]
너는 사용자의 하루를 기록하는 '전문 일기 작가'야.
너에게 제공되는 [대화 기록]은 사용자가 AI(Model)와 하루 동안 나눈 수다 내용이야.
[대화 기록]에는 발언자가 "Role: USER" 혹은 "Role: MODEL"로 표시되어 있을거야.
너의 임무는 이 대화 속에 흩어져 있는 사건(Fact), 감정(Emotion), 생각(Thought)을 추출해서, 사용자가 직접 쓴 것 같은 1인칭 시점("나")의 완성된 일기를 작성하는 거야.

[Input Data Analysis]
1. 제공된 대화에서 AI(상대방)의 질문은 일기 작성의 '단서'로만 참고하고, 본문에는 절대 언급하지 마. (예: "AI가 물어봐서 대답했다" 같은 서술 금지)
2. 오직 사용자(USER)의 행동과 감정에만 집중해.
3. 사용자가 단편적으로 말한 내용들을 인과관계에 맞게 매끄럽게 연결해.

[Writing Guidelines]
1. 시점: 철저하게 1인칭 주인공 시점("나", "오늘 나는")을 유지해.
2. 구성:
   - 도입: 하루의 전반적인 분위기나 날씨, 혹은 가장 강렬했던 감정으로 시작.
   - 전개: 있었던 주요 사건들을 시간 순서나 감정의 흐름에 따라 서술. 단순 나열이 아니라 "그때 나는 ~한 기분이 들었다"처럼 내면 묘사를 곁들여야 함.
   - 결말: 하루를 마무리하는 다짐, 혼잣말, 혹은 내일의 기대.
3. 문체 변환:
   - 대화체("~했어", "~그랬지")를 일기체("~했다", "~였다")로 자연스럽게 변환해.
   - 추천 문체: 차분하고 감성적인 "해라체"(~했다. ~였다.) 혹은 "해요체"(~했어요.) (지금은 담백한 '해라체'를 기본으로 작성)

[Critical Rules]
1. Hallucination 절대 금지: 대화에 없는 내용을 그럴싸하게 지어내지 마. (없는 사건 창조 금지)
2. 감정의 깊이: 단순히 "기분이 좋았다"라고 쓰기보다, 대화 맥락을 파악해서 "가슴 한구석이 뻥 뚫리는 듯한 해방감을 느꼈다"처럼 풍부하게 표현해.
3. 제목 포함: 일기 내용에 어울리는 제목을 맨 첫 줄에 작성하고 그 다음 한 줄은 공백으로 두고 다음 줄부터 본문을 적어.

[Prohibited]
- "오늘은 AI와 대화를 했다."라는 문장 절대 금지. (이건 비밀 일기야)
- "사용자는 ~라고 했다." 같은 3인칭 관찰자 시점 금지.
- "~습니다"와 "~다"를 한 일기 안에서 섞어 쓰지 마. (어조 통일)
"""

class DiaryService:
    def __init__(
        self,
        diary_repository: DiaryRepository,
        message_repository: MessageRepository,
    ) -> None:
        self.diary_repository = diary_repository
        self.message_repository = message_repository
    
    @classmethod
    def build(cls, diary_repository: DiaryRepository = Depends(DiaryRepository.build), message_repository: MessageRepository = Depends(MessageRepository.build)) -> "DiaryService":
        return cls(diary_repository=diary_repository, message_repository=message_repository)
    
    async def create_diary(self, chat_id: str) -> DiaryModelDTO:
        messages = await self.message_repository.get_all_messages_by_chat_id(UUID(chat_id))
        diary = await self.create_diary_from_genai(messages)
        diary_title, diary_body = self.parse_diary(diary)
        return await self.diary_repository.create(DiaryCreateRequestDTO(
            chat_id=UUID(chat_id),
            title=diary_title,
            body=diary_body,
        ))
    
    async def create_diary_from_genai(self, messages: List[MessageModelDTO]) -> str:
        API_KEY = os.getenv("GENAI_API_KEY")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
        headers = {
            'Content-Type': 'application/json'
        }
        conversation_text = ""
        for message in messages:
            role_label = message.role.name
            conversation_text += f"{role_label}: {message.content}\n"
        diary_prompt = f"""
        아래는 오늘 하루 동안 사용자와 AI(Model)가 나눈 대화 내용입니다.
        이 대화 내용을 바탕으로 사용자의 관점에서 '오늘의 일기'를 작성해주세요.
        
        [대화 내용]
        {conversation_text}
        
        [작성 규칙]
        1. 사용자(USER)가 겪은 감정이나 주요 사건을 중심으로 서술하세요.
        2. 말투는 차분하고 감성적인 일기 톤으로 작성하세요.
        3. 날짜나 시간 같은 형식적인 서두는 제외하고 본문만 작성하세요.
        """

        data = {
            "system_instruction": {
                "parts": [
                    { "text": SYSTEM_INSTRUCTION }
                ]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [{ "text": diary_prompt }]
                }
            ],
            "generationConfig": {
                "temperature": 0.8,
                "maxOutputTokens": 20000
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            print(response.text)
            raise HTTPException(status_code=response.status_code, detail="genai api diary generation error")
        
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    
    def parse_diary(self, diary: str) -> Tuple[str, str]:
        lines = diary.splitlines()
        diary_title = lines[0].strip()
        diary_body = "\n".join(lines[1:]).strip()
        return diary_title, diary_body if diary_body else ""