from datetime import datetime, timedelta
from typing import Optional, Any
import jwt  # PyJWT 사용
from config import settings  # config.py의 settings 객체 사용

def create_access_token(subject: Any, expires_delta: Optional[timedelta] = None) -> str:
    """
    Access Token 생성 (Sign)
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # settings에서 만료 시간 가져오기
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"sub": str(subject), "exp": expire}
    
    # PyJWT의 encode 사용
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Access Token 검증 (Verify)
    - PyJWT의 decode는 서명 검증과 exp(만료) 체크를 기본적으로 수행함
    """
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        return payload

    except jwt.ExpiredSignatureError:
        # 토큰 만료 시
        return None

    except jwt.InvalidTokenError:
        # 서명 불일치 또는 잘못된 토큰
        return None