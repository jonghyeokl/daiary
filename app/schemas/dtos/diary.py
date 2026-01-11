from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class DiaryCreateRequestDTO:
    chat_id: UUID
    title: str
    body: str
    
@dataclass
class DiaryUpdateRequestDTO:
    diary_id: UUID
    title: str
    body: str