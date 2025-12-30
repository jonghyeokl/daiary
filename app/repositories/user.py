from fastapi import Depends
from datetime import datetime
from typing import Optional
from uuid import uuid4, UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models.user.user import User

from app.schemas.model_dtos.user import UserModelDTO
from app.schemas.dtos.user import UserCreateRequestDTO

class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    @classmethod
    def build(
        cls,
        db: AsyncSession = Depends(get_db),
    ) -> "UserRepository":
        return cls(db=db)

    async def find_by_email(self, email: str) -> Optional[UserModelDTO]:
        query = await self.db.execute(select(User).where(User.email == email))

        user = query.scalars().one_or_none()

        return UserModelDTO.from_model(user) if user else None
    
    async def find_by_user_id(self, user_id: UUID) -> Optional[UserModelDTO]:
        query = await self.db.execute(select(User).where(User.user_id == user_id))
        user = query.scalars().one_or_none()
        return UserModelDTO.from_model(user) if user else None
    
    async def create(self, user: UserCreateRequestDTO) -> UserModelDTO:
        now = datetime.utcnow()
        user_id = uuid4()
        new_user = User(
            user_id=user_id,
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password,
            phone_number=user.phone_number,
            created_dt=now,
            updated_dt=now,
        )
        self.db.add(new_user)
        
        await self.db.commit()

        return UserModelDTO.from_model(new_user)
    
    async def update_by_user_id(self, user_id: UUID, hashed_password: str):
        query = await self.db.execute(select(User).where(User.user_id == user_id))

        user = query.scalars().first()
        user.hashed_password = hashed_password

        await self.db.commit()