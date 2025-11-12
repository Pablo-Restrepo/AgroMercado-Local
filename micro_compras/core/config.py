from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    RABBIT_URL: str = 'amqp://guest:guest@localhost:5672/'
    QUEUE_NAME: str     
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
