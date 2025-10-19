
from infra.repositories import GremioRepositorySQL, ProductorRepositorySQL
#from app.infra.messaging import RabbitPublisher
from application.services import GremioService, ProductorService
from config import Settings
from infra.messaging import RabbitConsumer

_singleton_publisher = None
_singleton_gremio_repo = None
_singleton_productor_repo = None
_singleton_service = None

def get_publisher():
    global _singleton_publisher
    if not _singleton_publisher:
        _singleton_publisher = RabbitConsumer(Settings.RABBIT_URL,queue_name="micro_productores_queue",prefetch=10)
    return _singleton_publisher

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
