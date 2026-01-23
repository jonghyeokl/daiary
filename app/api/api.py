from fastapi import APIRouter

from app.api.user import router as user_router
from app.api.message import router as message_router
from app.api.chat import router as chat_router
from app.api.diary import router as diary_router
from app.api.setting import router as setting_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(message_router, prefix="/message", tags=["message"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(diary_router, prefix="/diary", tags=["diary"])
api_router.include_router(setting_router, prefix="/setting", tags=["setting"])