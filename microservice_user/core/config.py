import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    BASE_URL: str = 'http://localhost:8001'
    PROJECT_NAME: str = 'AgroMercado-Local'
    VERSION: str = '1.0.0'
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    EUREKA_APP_NAME: str = 'users-microservice'
    EUREKA_INSTANCE_PORT: int = 8001
    EUREKA_INSTANCE_HOST: str = 'localhost'
    EUREKA_SERVER_URL: str = 'http://localhost:8761/eureka'
    model_config = ConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'),
        extra='ignore'
    )


settings = Settings()
