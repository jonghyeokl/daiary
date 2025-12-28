from pydantic import BaseModel
from pydantic import Field

from app.schemas.dtos.user import UserCreateRequestDTO
from app.utils.hash import hash_password

class SignUpRequestBody(BaseModel):
    name: str = Field(..., description="User name")
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")
    phone_number: str = Field(..., description="User phone number")

    def to_sign_up_request_dto(self) -> UserCreateRequestDTO:
        return UserCreateRequestDTO(
            name=self.name,
            email=self.email,
            hashed_password=hash_password(self.password),
            phone_number=self.phone_number,
        )

class UpdatePasswordRequestBody(BaseModel):
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., description="New password")