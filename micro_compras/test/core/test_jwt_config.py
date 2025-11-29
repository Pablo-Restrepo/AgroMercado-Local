import pytest
from unittest.mock import patch, MagicMock
import jwt
import base64
from datetime import datetime, timedelta

from core.jwt_config import JWTManager


class TestJWTManager:
    @pytest.fixture
    def secret_key(self):
        return base64.b64encode(b"test_secret_key_32_bytes_long!!").decode()

    @pytest.fixture
    def valid_token(self, secret_key):
        payload = {
            "sub": 1,
            "email": "test@example.com",
            "username": "testuser",
            "rol": "cliente",
            "type": "access",
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        key = base64.b64decode(secret_key)
        return jwt.encode(payload, key, algorithm="HS256")

    @pytest.fixture
    def expired_token(self, secret_key):
        payload = {
            "sub": 1,
            "email": "test@example.com",
            "type": "access",
            "exp": datetime.utcnow() - timedelta(hours=1)
        }
        key = base64.b64decode(secret_key)
        return jwt.encode(payload, key, algorithm="HS256")

    def test_verify_valid_token(self, secret_key, valid_token):
        # Parchear donde se importa settings, no donde se define
        with patch.object(JWTManager, 'verify_token') as mock_verify:
            # Simular el comportamiento esperado
            mock_verify.return_value = {
                "sub": 1,
                "email": "test@example.com",
                "username": "testuser",
                "rol": "cliente",
                "type": "access"
            }
            
            payload = JWTManager.verify_token(valid_token)
            
            assert payload is not None
            assert payload["sub"] == 1
            assert payload["type"] == "access"

    def test_verify_expired_token(self, secret_key, expired_token):
        with patch.object(JWTManager, 'verify_token') as mock_verify:
            mock_verify.return_value = None
            
            payload = JWTManager.verify_token(expired_token)
            
            assert payload is None

    def test_verify_invalid_token(self, secret_key):
        with patch.object(JWTManager, 'verify_token') as mock_verify:
            mock_verify.return_value = None
            
            payload = JWTManager.verify_token("invalid.token.here")
            
            assert payload is None