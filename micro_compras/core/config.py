from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    RABBIT_URL: str = 'amqp://guest:guest@localhost:5672/'       
    DATABASE_URL: str = 'mysql+aiomysql://root:root@localhost/microservice_compras_bd'
    USUARIO_QUEUE_NAME: str = 'usuario_queue' # Nombre de la cola para recibir usuarios desde el micro de usuarios
    PRODUCTO_QUEUE_NAME: str = 'producto_queue' # Nombre de la cola para recibir productos desde el micro de productos
    PRODUCTO_STOCK_QUEUE_NAME: str = 'updated_product_stock' # Nombre de la cola para actualizar stock en el micro de productos
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    EUREKA_APP_NAME: str = 'micro-compras'
    EUREKA_INSTANCE_PORT: int = 8003
    EUREKA_INSTANCE_HOST: str = 'localhost'
    EUREKA_SERVER_URL: str = 'http://localhost:8761/eureka'
    DEFAULT_ENVIO_COST: float = 10000.0
    model_config = ConfigDict(
        env_file='.env',
        extra='ignore'
    )


settings = Settings()
