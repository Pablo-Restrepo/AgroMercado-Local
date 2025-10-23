from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from microservice_user.core.jwt_config import JWTManager

security = HTTPBearer()
jwt_manager = JWTManager()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Obtiene el usuario actual desde el token JWT"""
    token = credentials.credentials
    payload = jwt_manager.verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload.get('type') != 'access':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        'user_id': payload.get('sub'),
        'email': payload.get('email'),
        'username': payload.get('username'),
        'rol': payload.get('rol')
    }
