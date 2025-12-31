from datetime import datetime

from pydantic import BaseModel

from app.db.models.diary.diary import Diary

class DiaryModelDTO(BaseModel):
    diary_id: str
    chat_id: str
    title: str
    body: str
    created_dt: datetime
    updated_dt: datetime

    @classmethod
    def from_model(cls, model: Diary) -> "DiaryModelDTO":
        return cls(
            diary_id=str(model.diary_id),
            chat_id=str(model.chat_id),
            title=model.title,
            body=model.body,
            created_dt=model.created_dt,
            updated_dt=model.updated_dt,
        )