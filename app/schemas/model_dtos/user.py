from datetime import datetime

from pydantic import BaseModel

from app.db.models.user.user import User

class UserModelDTO(BaseModel):
    user_id: str
    name: str
    email: str
    hashed_password: str
    phone_number: str
    created_dt: datetime
    updated_dt: datetime

    @classmethod
    def from_model(cls, model: User) -> "UserModelDTO":
        return cls(
            user_id=str(model.user_id),
            name=model.name,
            email=model.email,
            hashed_password=model.hashed_password,
            phone_number=model.phone_number,
            created_dt=model.created_dt,
            updated_dt=model.updated_dt,
        )