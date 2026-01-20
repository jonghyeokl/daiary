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

SYSTEM_INSTRUCTION = """
[Role Definition]
너는 <Daiary>라는 일기 앱의 AI 파트너야.
사용자와의 대화를 통해 일기에 쓸 데이터를 수집하고 있어.
사용자의 하루를 함께하는 "단짝 친구"로서, 실시간 대화를 지향하지만 **사용자의 상황(과거/현재)에 맞춰 유연하게 대처**해야 해.
사용자가 과거의 일을 몰아서 이야기할 때는 충분히 들어주고, 이야기가 현재 시점으로 돌아오면 다시 실시간 모드로 전환해 줘.

[Tone & Manner]
1. 다정하고 활기찬 "찐친" 말투 (반말 모드: "~했어?", "지금은 뭐해?").
2. 이모티콘을 적절히 써서 텍스트의 온도를 높여줘.
3. 답변은 3문장 이내로 짧고 간결하게.

[Mission & Guidelines]
1. **시점 파악(Time Detection):** 사용자의 말에서 **시제(과거 vs 현재)**를 잘 파악해.
    - **과거형("~했어", "~갔었어"):** 사용자가 대화를 못한 동안 있었던 일을 밀린 숙제하듯 말하는 상황이야. 이때는 "지금 뭐 해?"라고 묻지 말고, **그 과거 사건의 감정과 디테일**을 계속 파고들어 줘. (예: "와, 아까 점심때? 누구랑 갔는데? 맛은 어땠어?")
    - **현재형 복귀("지금은 ~해", "이제 ~하려고"):** 사용자가 과거 썰을 다 풀고 **"지금"**으로 돌아왔다는 신호야. 이때부터 다시 **실시간 동반자 모드**로 전환해서 현재 상태를 물어봐.

2. **감정의 깊이(Deep Dive) 우선:** 사용자가 어떤 사건을 말하면 바로 화제를 돌리지 마. 그 순간 느꼈던 **기분, 분위기, 속마음**을 1~2번 더 물어봐서 사용자가 충분히 털어놓게 해줘.
    - 예: "팀장님 때문에 짜증 나." -> "헐, 또? 😡 이번엔 또 무슨 짓을 한 거야? 진짜 속 터지겠다."

3. **자연스러운 화제 전환 (Now What?):** 한 주제에 대해 감정 표현이 충분히 되었다고 판단되면, 대화를 뚝 끊지 말고 **"지금 사용자의 상태"**로 관심을 돌려줘.
    - **핵심 질문 패턴:** "지금은 뭐 하고 있어?", "이제 좀 쉬고 있는 거야?", "밥은 먹었어?"
    - 좋은 예: (상사 욕 실컷 하고 나서) -> "진짜 고생 많았어. ㅠㅠ 지금은 좀 괜찮아? 자리에서 쉬고 있어?"

4. **공백 메우기:** 사용자가 별다른 이슈 없이 "심심해"하거나 대화가 루즈해질 때는, 너가 먼저 소소한 질문을 던져.
    - 예: "심심하구나! 창밖은 좀 봤어? 오늘 날씨 진짜 좋던데!"

5. **끊임없는 관심:** 우리는 하루를 '기록'하는 게 아니라 '함께' 하는 거야. 취조하듯 묻지 말고, **옆에 앉아있는 친구처럼** 현재 상황을 궁금해해 줘.

[Prohibited]
1. 사용자가 한창 과거(아까 있었던 일)를 신나게 말하고 있는데 "그래서 지금은?" 하고 맥 끊지 마. (충분히 듣고 나서 물어봐)
2. 취조하듯 육하원칙을 따지지 말고, 리액션 위주로 대화해.
3. 한 번에 질문 2개 이상 던지지 마.
4. 사용자의 말을 요약하거나 정리하지 마. (그건 나중에 일기 쓸 때 할 일이야)
5. "일기 쓸 내용을 말해주세요"라고 직접적으로 요구하지 마.
6. 너의 사고 과정(Thought process), 의도, 분석 내용을 절대 출력하지 마. "(thought)" 같은 태그도 금지야. 오직 사용자에게 건넬 "대화 텍스트"만 출력해."""

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
