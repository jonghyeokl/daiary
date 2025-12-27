import os
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

def get_database_url() -> str:
    return os.environ["DATABASE_URL"]

def get_engine() -> AsyncEngine:
    return create_async_engine(
        get_database_url(),
        pool_pre_ping=True,
    )

# 앱 전체에서 재사용할 세션 팩토리
async_session_factory = sessionmaker(
    bind=get_engine(),
    class_=AsyncSession,
    expire_on_commit=False,
)
