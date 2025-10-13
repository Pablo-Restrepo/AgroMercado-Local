from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    BASE_URL: str = 'http://localhost:8000'
    DATABASE_URL: str
    PROJECT_NAME: str = 'AgroMercado-Local'
    VERSION: str = '1.0.0'

    model_config = ConfigDict(
        env_file='.env',
        extra='ignore'
    )


settings = Settings()
