from dataclasses import dataclass

@dataclass
class SignUpRequestDTO:
    name: str
    email: str
    hashed_password: str
    phone_number: str