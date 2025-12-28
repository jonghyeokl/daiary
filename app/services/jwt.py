from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict

import jwt
from fastapi import HTTPException

from app.resources.config import conf

class JwtService:
    ACCESS_TOKEN_EXPIRATION = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRATION = timedelta(days=30)

    @classmethod
    def build(cls) -> "JwtService":
        return cls()

    def _create_jwt_token(
        self,
        payload: Dict[str, Any],
        secret_key: str,
    ) -> str:
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return token
    
    def _decode_jwt_token(
        self,
        token: str,
        secret_key: str,
    ) -> Dict[str, Any]:
        jwt_token = token.encode("utf-8")
        payload = jwt.decode(jwt_token, secret_key, algorithms=["HS256"])
        return payload

    def create_access_token(self, user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + self.ACCESS_TOKEN_EXPIRATION,
        }

        return self._create_jwt_token(payload, conf.ACCESS_TOKEN_SECRET_KEY)

    def create_refresh_token(self, user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + self.REFRESH_TOKEN_EXPIRATION,
        }

        return self._create_jwt_token(payload, conf.REFRESH_TOKEN_SECRET_KEY)

    def validate_access_token(self, access_token: str) -> str:
        try:
            user_id = self._decode_jwt_token(
                access_token, conf.ACCESS_TOKEN_SECRET_KEY
            )["user_id"]
            if user_id is None:
                raise HTTPException(status_code=401, detail="Token invalid")
            return user_id
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token invalid")

    def validate_refresh_token(self, refresh_token: str) -> str:
        try:
            user_id = self._decode_jwt_token(
                refresh_token, conf.REFRESH_TOKEN_SECRET_KEY
            )["user_id"]
            if user_id is None:
                raise HTTPException(status_code=401, detail="Token invalid")
            return user_id
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token invalid")