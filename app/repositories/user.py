from fastapi import Depends
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models.user.user import User

from app.schemas.model_dtos.user import UserModelDTO
from app.schemas.dtos.user import UserCreateRequestDTO, UserUpdatePasswordRequestDTO

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
    
    async def find_by_id(self, id: str) -> Optional[UserModelDTO]:
        query = await self.db.execute(select(User).where(User.id == id))
        user = query.scalars().one_or_none()
        return UserModelDTO.from_model(user) if user else None
    
    async def create(self, user: UserCreateRequestDTO) -> UserModelDTO:
        now = datetime.utcnow()
        id = uuid4()
        new_user = User(
            id=id,
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
    
    async def update_password(self, user: User, dto: UserUpdatePasswordRequestDTO) -> UserModelDTO:
        now = datetime.utcnow()
        user.hashed_password = dto.hashed_new_password
        user.updated_dt = now
        await self.db.commit()
        await self.db.refresh(user)
        return UserModelDTO.from_model(user)