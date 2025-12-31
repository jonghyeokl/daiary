from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Body

from app.exceptions.user import EmailAlreadyExistsException
from app.exceptions.user import EmailNotFoundException
from app.exceptions.user import InvalidCredentialsException
from app.exceptions.user import UserNotFoundException
from app.repositories.user import UserRepository
from app.schemas.apis.requests.user import SignUpRequestBody, UpdatePasswordRequestBody
from app.schemas.apis.responses.custom_error import CustomErrorExample
from app.schemas.apis.responses.custom_error import CustomErrorResponse

from app.services.jwt import JwtService
from app.utils.jwt_bearer import get_access_token
from app.utils.hash import verify_password, hash_password

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
    response_model=str,
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
    jwt_service: JwtService = Depends(JwtService.build),
) -> str:
    user = await user_repository.find_by_email(email)
    if not user:
        raise EmailNotFoundException()

    if not verify_password(password, user.hashed_password):
        raise InvalidCredentialsException()

    return jwt_service.create_access_token(user.user_id)

@router.patch(
    "/update-password",
    response_model=None,
    responses = {
        403: CustomErrorResponse(
            examples=[
                CustomErrorExample(
                    exception=InvalidCredentialsException(),
                )
            ]
        ).to_openapi(),
    }
)
async def update_password(
    access_token: Annotated[str, Depends(get_access_token)],
    request_body: UpdatePasswordRequestBody,
    user_repository: UserRepository = Depends(UserRepository.build),
) -> None:
    user_id = JwtService().validate_access_token(access_token)
    user = await user_repository.find_by_user_id(user_id)

    if not user:
        raise UserNotFoundException()

    if not verify_password(request_body.current_password, user.hashed_password):
        raise InvalidCredentialsException()

    new_hashed_password = hash_password(request_body.new_password)

    await user_repository.update_by_user_id(user_id=user_id, hashed_password=new_hashed_password)