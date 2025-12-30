from fastapi import APIRouter
from fastapi import Depends

from app.api.user import router as user_router
from app.api.message import router as message_router
from app.api.chat import router as chat_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(message_router, prefix="/message", tags=["message"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])