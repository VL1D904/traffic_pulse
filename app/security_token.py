from datetime import datetime, timezone, timedelta
from token_settings import settings
from jose import jwt, JWTError


class SecurityToken:
    def __init__(self):
        pass

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = int(expire.timestamp())
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    def decode_access_token(self, token: str) -> dict:
        try: 
            payload = jwt.decode(
                token=token,
                key=settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            return payload
        except JWTError:
            return None