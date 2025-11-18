from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    RABBIT_URL: str = 'amqp://guest:guest@localhost:5672/'       
    DATABASE_URL: str = 'mysql+aiomysql://root:root@localhost/microservice_compras_bd'
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    EUREKA_APP_NAME: str = 'micro_compras'
    EUREKA_INSTANCE_PORT: int = 8003
    EUREKA_INSTANCE_HOST: str = 'localhost'
    EUREKA_SERVER_URL: str = 'http://localhost:8761/eureka'
    model_config = ConfigDict(
        env_file='.env',
        extra='ignore'
    )


settings = Settings()
