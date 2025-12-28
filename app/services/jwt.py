from datetime import timedelta

class JWTService:
    ACCESS_TOKEN_EXPIRATION = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRATION = timedelta(days=30)

    