from fastapi import Depends
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from uuid import uuid4
from typing import Optional

from app.db.session import get_db
from app.schemas.dtos.diary import DiaryUpdateRequestDTO
from app.schemas.dtos.diary import DiaryCreateRequestDTO
from app.schemas.model_dtos.diary import DiaryModelDTO
from app.db.models.diary.diary import Diary

class DiaryRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    @classmethod
    def build(cls, db: AsyncSession = Depends(get_db)) -> "DiaryRepository":
        return cls(db=db)
    
    async def find_diary_by_chat_id(self, chat_id: UUID) -> Optional[DiaryModelDTO]:
        query = await self.db.execute(select(Diary).where(Diary.chat_id == chat_id))
        diary = query.scalars().one_or_none()
        return DiaryModelDTO.from_model(diary) if diary else None
    
    async def update(self, diary_update_request_dto: DiaryUpdateRequestDTO) -> None:
        query = await self.db.execute(select(Diary).where(Diary.diary_id == diary_update_request_dto.diary_id))
        diary = query.scalars().one()
        diary.title = diary_update_request_dto.title
        diary.body = diary_update_request_dto.body

        await self.db.commit()
    
    async def create(self, diary_create_request_dto: DiaryCreateRequestDTO) -> DiaryModelDTO:
        now = datetime.utcnow()
        diary = Diary(
            diary_id=uuid4(),
            chat_id=diary_create_request_dto.chat_id,
            title=diary_create_request_dto.title,
            body=diary_create_request_dto.body,
            created_dt=now,
            updated_dt=now,
        )
        self.db.add(diary)
        await self.db.commit()
        return DiaryModelDTO.from_model(diary)