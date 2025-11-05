from py_eureka_client.eureka_client import EurekaClient
from core.config import settings


eureka_client = EurekaClient(
    eureka_server=settings.EUREKA_SERVER_URL,
    app_name=settings.EUREKA_APP_NAME,
    instance_port=settings.EUREKA_INSTANCE_PORT,
    instance_host=settings.EUREKA_INSTANCE_HOST,
)