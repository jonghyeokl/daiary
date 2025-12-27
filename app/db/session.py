import os

import orjson
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.utils.orjson_serializer import orjson_serializer

if os.getenv("DATABASE_URL") is None:
    load_dotenv(".env")

async_engine = create_async_engine(
    os.getenv("DATABASE_URL"),
    future=True,
    pool_pre_ping=True,
    json_serializer=orjson_serializer,
    json_deserializer=orjson.loads,
    pool_size=200,
    pool_timeout=30,
    pool_recycle=500,
    max_overflow=10,
)

session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_db() -> AsyncSession:
    db = session()
    try:
        yield db
    finally:
        await db.close()
