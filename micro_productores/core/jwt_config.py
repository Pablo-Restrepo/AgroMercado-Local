import jwt
from jwt.exceptions import InvalidTokenError
from config import settings
import base64

class JWTManager:
    @staticmethod
    def _get_signing_key() -> bytes:
        """Decodifica la SECRET_KEY desde base64 (recomendado para HS256)."""
        try:
            return base64.b64decode(settings.SECRET_KEY.strip())
        except Exception:
            # fallback: usar UTF-8 si no es base64 (dev/legacy)
            return settings.SECRET_KEY.encode('utf-8')

    @staticmethod
    def verify_token(token: str) -> dict[str, any] | None:
        try:
            payload = jwt.decode(token, JWTManager._get_signing_key(), algorithms=[settings.ALGORITHM])
        except jwt.ExpiredSignatureError:
            return None
        except InvalidTokenError:
            return None
        return payload