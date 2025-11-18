from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from core.config import settings
import base64

class JWTManager:
    @staticmethod
    def _get_signing_key() -> bytes:
        """Convierte SECRET_KEY a bytes usando UTF-8."""
        return settings.SECRET_KEY.encode('utf-8')

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, JWTManager._get_signing_key(), algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, JWTManager._get_signing_key(), algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> dict[str, any] | None:
        try:
            payload = jwt.decode(token, JWTManager._get_signing_key(), algorithms=[settings.ALGORITHM])
        except jwt.ExpiredSignatureError:
            return None
        except InvalidTokenError:
            return None
        return payload