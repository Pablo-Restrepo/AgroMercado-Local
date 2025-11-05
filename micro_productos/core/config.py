from pydantic_settings import BaseSettings
from pydantic import ConfigDict



class Settings(BaseSettings):
    # Datos de la aplicación
    BASE_URL: str = "http://localhost:8000"
    PROJECT_NAME: str = "AgroMercado-Local"
    VERSION: str = "1.0.0"

    # Configuración de MySQL
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_DB: str

    # Configuración de MongoDB
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_DB: str
    
    # RabbitMQ
    RABBIT_USER: str
    RABBIT_PASS: str
    RABBIT_HOST: str
    RABBIT_PORT: int
    PRODUCTORS_QUEUE: str

    # eureka
    EUREKA_APP_NAME: str
    EUREKA_INSTANCE_PORT: int
    EUREKA_INSTANCE_HOST: str
    EUREKA_HOST: str
    # Propiedades derivadas
    @property
    def MYSQL_DATABASE_URL(self) -> str:
        return (
            f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
        )

    @property
    def EUREKA_SERVER_URL(self) -> str:
        return (f"http://{self.EUREKA_HOST}:8761/eureka")
    
    @property
    def MONGO_DATABASE_URL(self) -> str:
        return (
            f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}"
            f"@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}"
        )
    @property
    def RABBIT_URL(self) -> str:
        return (
            f"amqp://{self.RABBIT_USER}:{self.RABBIT_PASS}"
            f"@{self.RABBIT_HOST}:{self.RABBIT_PORT}/"
        )
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
