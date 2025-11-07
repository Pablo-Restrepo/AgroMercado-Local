from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    BASE_URL: str
    DATABASE_URL: str 
    PROJECT_NAME: str
    VERSION: str
    RABBIT_URL: str 
    QUEUE_NAME: str 
    PRODUCTORS_QUEUE: str
    SECRET_KEY: str
    ALGORITHM: str 
    EUREKA_APP_NAME: str 
    EUREKA_INSTANCE_PORT: int 
    EUREKA_INSTANCE_HOST: str 
    EUREKA_SERVER_URL: str 
    model_config = ConfigDict(
        env_file='.env',
        extra='ignore'
    )


settings = Settings()
