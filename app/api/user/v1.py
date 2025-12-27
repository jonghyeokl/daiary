from fastapi import APIRouter
from fastapi import Depends
from fastapi import Body

from app.exceptions.user import EmailAlreadyExistsException
from app.exceptions.user import EmailNotFoundException
from app.exceptions.user import InvalidCredentialsException
from app.repositories.user import UserRepository
from app.schemas.apis.requests.user import SignUpRequestBody
from app.schemas.apis.responses.custom_error import CustomErrorExample
from app.schemas.apis.responses.custom_error import CustomErrorResponse
from app.utils.hash import verify_password

router = APIRouter()

@router.post(
    "/",
    response_model=None,
    responses = {
        403: CustomErrorResponse(
            examples=[
                CustomErrorExample(
                    exception=EmailAlreadyExistsException(),
                )
            ]
        ).to_openapi(),
    }
)
async def sign_up(
    request_body: SignUpRequestBody,
    user_repository: UserRepository = Depends(UserRepository.build),
) -> None:
    sign_up_request_dto = request_body.to_sign_up_request_dto()
    user = await user_repository.find_by_email(sign_up_request_dto.email)
    if user:
        raise EmailAlreadyExistsException()

    await user_repository.create(sign_up_request_dto)

@router.post(
    "/login",
    response_model=None,
    responses = {
        403: CustomErrorResponse(
            examples=[
                CustomErrorExample(
                    exception=EmailNotFoundException(),
                ),
                CustomErrorExample(
                    exception=InvalidCredentialsException(),
                )
            ]
        ).to_openapi(),
    }
)
async def login(
    email: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    user_repository: UserRepository = Depends(UserRepository.build),
) -> None:
    user = await user_repository.find_by_email(email)
    if not user:
        raise EmailNotFoundException()

    if not verify_password(password, user.hashed_password):
        raise InvalidCredentialsException()
