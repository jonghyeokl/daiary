from typing import Annotated
from typing import List
from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Body
from fastapi import HTTPException

from app.schemas.model_dtos.chat import ChatModelDTO
from app.schemas.model_dtos.message import MessageModelDTO
from app.schemas.apis.responses.chat import MessagesDiaryResponse
from app.services.jwt import JwtService
from app.services.chat import ChatService
from app.repositories.chat import ChatRepository
from app.repositories.message import MessageRepository
from app.repositories.diary import DiaryRepository
from app.utils.jwt_bearer import get_access_token

router = APIRouter()

@router.post(
    "/",
    response_model=MessageModelDTO,
)
async def create_chat_and_initial_message(
    access_token: Annotated[str, Depends(get_access_token)],
    chat_date: str = Body(..., embed=True),
    chat_service: ChatService = Depends(ChatService.build),
) -> MessageModelDTO:
    user_id = JwtService().validate_access_token(access_token)

    return await chat_service.create_chat_and_initial_message(user_id=user_id, chat_date=chat_date)

@router.get(
    "/",
    response_model=List[ChatModelDTO],
)
async def get_all_chats(
    access_token: Annotated[str, Depends(get_access_token)],
    chat_repository: ChatRepository = Depends(ChatRepository.build),
) -> List[ChatModelDTO]:
    user_id = JwtService().validate_access_token(access_token)
    return await chat_repository.get_all_chats_by_user_id(user_id)

@router.get(
    "/get-all-messages-and-diary",
    response_model=MessagesDiaryResponse,
)
async def get_all_messages_and_diary(
    access_token: Annotated[str, Depends(get_access_token)],
    chat_id: str,
    message_repository: MessageRepository = Depends(MessageRepository.build),
    diary_repository: DiaryRepository = Depends(DiaryRepository.build),
) -> MessagesDiaryResponse:
    JwtService().validate_access_token(access_token)
    messages = await message_repository.get_all_messages_by_chat_id(UUID(chat_id))
    diary = await diary_repository.find_diary_by_chat_id(UUID(chat_id))
    return MessagesDiaryResponse(messages=messages, diary=diary)

@router.patch(
    "/",
    response_model=None,
)
async def rating(
    access_token: Annotated[str, Depends(get_access_token)],
    chat_id: str,
    rating: int = Body(..., embed=True, ge=1, le=10),
    chat_repository: ChatRepository = Depends(ChatRepository.build),
) -> None:
    JwtService().validate_access_token(access_token)
    await chat_repository.rating(chat_id=UUID(chat_id), rating=rating)