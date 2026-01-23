from fastapi import Depends
from datetime import datetime
from uuid import uuid4, UUID
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models.setting.setting import Setting
from app.schemas.model_dtos.setting import SettingModelDTO

class SettingRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    @classmethod
    def build(
        cls,
        db: AsyncSession = Depends(get_db),
    ) -> "SettingRepository":
        return cls(db=db)
    
    async def create(self, user_id: UUID) -> Setting:
        now = datetime.utcnow()
        setting_id = uuid4()
        new_setting = Setting(
            setting_id=setting_id,
            user_id=user_id,
            chat_manner=1,
            diary_font=1,
            created_dt=now,
            updated_dt=now,
        )
        self.db.add(new_setting)
        return new_setting
    
    async def upsert(self, user_id: UUID, chat_manner: int, diary_font: int) -> SettingModelDTO:
        query = await self.db.execute(select(Setting).where(Setting.user_id == user_id))
        setting = query.scalars().first()
        if not setting:
            setting = await self.create(user_id)
        
        setting.chat_manner = chat_manner
        setting.diary_font = diary_font
        setting.updated_dt = datetime.utcnow()

        await self.db.commit()
        
        return SettingModelDTO.from_model(setting)

    async def find_by_user_id(self, user_id: UUID) -> Optional[SettingModelDTO]:
        query = await self.db.execute(select(Setting).where(Setting.user_id == user_id))
        setting = query.scalars().first()
        
        return SettingModelDTO.from_model(setting) if setting else None