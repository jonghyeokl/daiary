from dataclasses import dataclass

@dataclass
class UserCreateRequestDTO:
    name: str
    email: str
    hashed_password: str
    phone_number: str