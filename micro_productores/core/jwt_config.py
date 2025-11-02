import jwt
from jwt.exceptions import InvalidTokenError
from config import settings


class JWTManager:    
    @staticmethod
    def verify_token(token: str) -> dict[str, any] | None:
        """Verifica y decodifica un token JWT"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,
                                 algorithms=[settings.ALGORITHM])
        except jwt.ExpiredSignatureError:
            return None
        except InvalidTokenError:
            return None
        return payload
