from dataclasses import dataclass

from uuid import UUID

@dataclass
class DiaryUpdateRequestDTO:
    diary_id: UUID
    title: str
    body: str