from fastapi import APIRouter
from fastapi import Depends
from fastapi import Body

from app.exceptions.user import EmailAlreadyExistsException
from app.exceptions.user import EmailNotFoundException
from app.exceptions.user import InvalidCredentialsException
from app.repositories.user import UserRepository
from app.schemas.apis.requests.user import SignUpRequestBody, UpdatePasswordRequestBody
from app.schemas.apis.responses.custom_error import CustomErrorExample
from app.schemas.apis.responses.custom_error import CustomErrorResponse

from app.core.security import create_access_token
from app.core.dependencies import get_current_user
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
):
    user = await user_repository.find_by_email(email)
    if not user:
        raise EmailNotFoundException()

    if not verify_password(password, user.hashed_password):
        raise InvalidCredentialsException()

    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

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
    request_body: UpdatePasswordRequestBody,
    user_repository: UserRepository = Depends(UserRepository.build),
    token_payload: dict = Depends(get_current_user),
) -> None:

    user_id = token_payload.get("sub")
    user = await user_repository.find_by_id(user_id)
    if not user:
        raise InvalidCredentialsException()
    
    update_password_request_dto = request_body.to_update_password_request_dto()

    if not verify_password(update_password_request_dto.current_password, user.hashed_password):
        raise InvalidCredentialsException()
    
    new_hashed_password = hash_password(update_password_request_dto.new_password)
    user.hashed_password = new_hashed_password
    await user_repository.update(user)
    return None