import os
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

def get_database_url() -> str:
    return os.environ["DATABASE_URL"]
