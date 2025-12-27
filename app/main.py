import os
from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/health")
async def health():
    return {"ok": True}

@app.get("/db-health")
async def db_health():
    if not DATABASE_URL:
        return {"ok": False, "error": "DATABASE_URL is not set"}

    try:
        engine = create_async_engine(DATABASE_URL, poolclass=NullPool, pool_pre_ping=True)
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        await engine.dispose()
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
