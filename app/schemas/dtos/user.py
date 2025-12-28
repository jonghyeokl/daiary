from dataclasses import dataclass

@dataclass
class UserCreateRequestDTO:
    name: str
    email: str
    hashed_password: str
    phone_number: str

@dataclass
class UserUpdatePasswordRequestDTO:
    current_password: str
    hashed_new_password: str