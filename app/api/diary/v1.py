from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated
from app.schemas.apis.requests.diary import UpdateDiaryRequestBody
from app.repositories.diary import DiaryRepository
from app.services.jwt import JwtService
from app.utils.jwt_bearer import get_access_token

router = APIRouter()

@router.patch(
    "/",
    response_model=None,
)
async def update_diary(
    access_token: Annotated[str, Depends(get_access_token)],
    request_body: UpdateDiaryRequestBody,
    diary_repository: DiaryRepository = Depends(DiaryRepository.build),
) -> None:
    JwtService().validate_access_token(access_token)
    await diary_repository.update(request_body.to_diary_update_request_dto())