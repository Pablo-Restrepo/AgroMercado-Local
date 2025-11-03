
from infra.repositories import GremioRepositorySQL, ProductorRepositorySQL
from application.services import GremioService, ProductorService
from config import settings
from py_eureka_client.eureka_client import EurekaClient


_singleton_gremio_repo = None
_singleton_productor_repo = None

eureka_client = EurekaClient(
    eureka_server=settings.EUREKA_SERVER_URL,
    app_name=settings.EUREKA_APP_NAME,
    instance_port=settings.EUREKA_INSTANCE_PORT,
    instance_host="localhost",
)

def get_gremio_repo():
    global _singleton_gremio_repo
    if not _singleton_gremio_repo:
        _singleton_gremio_repo = GremioRepositorySQL()
    return _singleton_gremio_repo
def get_productor_repo():
    global _singleton_productor_repo
    if not _singleton_productor_repo:
        _singleton_productor_repo = ProductorRepositorySQL()
    return _singleton_productor_repo

def get_productor_service():
    #pub = get_publisher()
    productor_repo = get_productor_repo()
    gremio_repo = get_gremio_repo()
    return ProductorService(productor_repo, gremio_repo)

def get_gremio_service():
    #pub = get_publisher()
    gremio_repo = get_gremio_repo()
    productor_repo = get_productor_repo()
    return GremioService(gremio_repo, productor_repo)
