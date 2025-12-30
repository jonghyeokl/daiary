from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Body

from app.schemas.apis.requests.message import InsertMessageRequestBody
from app.schemas.model_dtos.message import MessageModelDTO
from app.services.message import MessageService
from app.services.jwt import JwtService
from app.utils.jwt_bearer import get_access_token

router = APIRouter()

@router.post(
    "/",
    response_model=MessageModelDTO,
)
async def get_from_genai_and_insert_message(
    access_token: Annotated[str, Depends(get_access_token)],
    request_body: InsertMessageRequestBody,
    message_service: MessageService = Depends(MessageService.build),
) -> MessageModelDTO:
    JwtService().validate_access_token(access_token)
    
    return await message_service.get_from_genai_and_insert_message(request_body.to_message_create_request_dto())