from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    BASE_URL: str = 'http://localhost:8000'
    DATABASE_URL: str
    PROJECT_NAME: str = 'AgroMercado-Local'
    VERSION: str = '1.0.0'
    RABBIT_URL: str
    QUEUE_NAME: str
    PRODUCTORS_QUEUE: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256" 
    EUREKA_APP_NAME: str = 'productors-microservice'
    EUREKA_INSTANCE_PORT: int = 8000
    EUREKA_SERVER_URL: str = 'http://localhost:8761/eureka'
    model_config = ConfigDict(
        env_file='.env',
        extra='ignore'
    )


settings = Settings()
