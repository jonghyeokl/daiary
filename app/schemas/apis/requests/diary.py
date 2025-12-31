from pydantic import BaseModel
from pydantic import Field
from uuid import UUID

from app.schemas.dtos.diary import DiaryUpdateRequestDTO

class UpdateDiaryRequestBody(BaseModel):
    diary_id: str = Field(..., description="Diary ID")
    title: str = Field(..., description="Title")
    body: str = Field(..., description="Body")

    def to_diary_update_request_dto(self) -> DiaryUpdateRequestDTO:
        return DiaryUpdateRequestDTO(
            diary_id=UUID(self.diary_id),
            title=self.title,
            body=self.body,
        )