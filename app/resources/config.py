from pydantic import BaseSettings

class Settings(BaseSettings):
    # 개발자만 아는 Secret Key
    # 배포 시 길고 복잡한 문자열로 바꿀 것
    SECRET_KEY: str = "welcome to jonghyeok and hanjae's d'ai'ary project!"

    # 암호화 알고리즘 (HS256)
    ALGORITHM: str = "HS256"


    class Config:
        env_file = ".env"

conf = Settings()