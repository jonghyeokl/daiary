from app.schemas.codes.exception_code_base import Exception400CodeBase
from app.schemas.codes.exception_code_base import Exception403CodeBase
from app.schemas.codes.exception_code_base import Exception404CodeBase

class UserException403Code(Exception403CodeBase):
    EMAIL_ALREADY_EXISTS = -14040
    EMAIL_NOT_FOUND = -14041
    INVALID_CREDENTIALS = -14042

    def to_str(self) -> str:
        if self == UserException403Code.EMAIL_ALREADY_EXISTS:
            return "Email already exists"
        elif self == UserException403Code.EMAIL_NOT_FOUND:
            return "Email not found"
        elif self == UserException403Code.INVALID_CREDENTIALS:
            return "Invalid credentials"
        return self.name