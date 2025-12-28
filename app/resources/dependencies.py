from security import verify_token
from config import settings

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    API 요청이 들어올 때마다 실행되는 함수.
    1. 헤더에서 토큰을 추출 (OAuth2PasswordBearer가 해줌)
    2. verify_token()으로 유효성 검사
    3. 유효하면 payload(담긴 정보)를 반환, 아니면 401 에러 발생
    """
    payload = verify_token(token)
    
    if payload is None:
        # 토큰이 만료되었거나 위조된 경우 401 에러를 던져서 쫓아냄
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 인증 성공! 토큰을 dictionary 형태로 반환
    return payload