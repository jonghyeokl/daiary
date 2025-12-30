from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # 개발자만 아는 Secret Key
    # 배포 시 길고 복잡한 문자열로 바꿀 것
    ACCESS_TOKEN_SECRET_KEY: str = "welcome to jonghyeok and hanjae's d'ai'ary project!"

    # 암호화 알고리즘 (HS256)
    ALGORITHM: str = "HS256"


conf = Settings()