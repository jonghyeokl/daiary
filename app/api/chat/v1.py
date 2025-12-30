from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Body

from app.schemas.dtos.message import MessageModelDTO
from app.services.jwt import JwtService
from app.services.chat import ChatService

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
) -> None:
    user_id = JwtService().validate_access_token(access_token)

    return await chat_service.create_chat_and_initial_message(user_id=user_id, chat_date=chat_date)
