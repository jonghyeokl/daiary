from pydantic import BaseModel
from pydantic import Field
from typing import List
from typing import Optional

from app.schemas.model_dtos.message import MessageModelDTO
from app.schemas.model_dtos.diary import DiaryModelDTO

class MessagesDiaryResponse(BaseModel):
    messages: List[MessageModelDTO] = Field(..., description="Messages")
    diary: Optional[DiaryModelDTO] = Field(None, description="Diary")