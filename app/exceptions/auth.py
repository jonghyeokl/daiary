from fastapi import HTTPException


class AuthorizationHeaderNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail="Authorization header not found")


class InvalidAuthorizationHeader(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail="Invalid Authorization header")