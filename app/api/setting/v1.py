from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Body

from app.repositories.setting import SettingRepository
from app.services.jwt import JwtService
from app.utils.jwt_bearer import get_access_token

router = APIRouter()

@router.patch(
    "/",
    response_model=None,
)
async def upsert_setting(
    access_token: Annotated[str, Depends(get_access_token)],
    chat_manner: int = Body(..., embed=True),
    diary_font: int = Body(..., embed=True),
    setting_repository: SettingRepository = Depends(SettingRepository.build),
) -> None:
    user_id = JwtService().validate_access_token(access_token)
    await setting_repository.upsert(user_id, chat_manner, diary_font)
