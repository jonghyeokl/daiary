import os
from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

app = FastAPI()

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/db-health")
def db_health():
    if not DATABASE_URL:
        return {"ok": False, "error": "DATABASE_URL is not set"}

    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
