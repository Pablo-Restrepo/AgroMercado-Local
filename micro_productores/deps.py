
from infra.repositories import GremioRepositorySQL, ProductorRepositorySQL
#from app.infra.messaging import RabbitPublisher
from application.productor_service import ProductoresService
from config import Settings

_singleton_publisher = None
_singleton_repo = None
_singleton_service = None

"""def get_publisher():
    global _singleton_publisher
    if not _singleton_publisher:
        _singleton_publisher = RabbitPublisher(settings.RABBIT_URL)
    return _singleton_publisher
"""
def get_gremio_repo():
    global _singleton_repo
    if not _singleton_repo:
        _singleton_repo = GremioRepositorySQL()
    return _singleton_repo
def get_productor_repo():
    global _singleton_repo
    if not _singleton_repo:
        _singleton_repo = ProductorRepositorySQL()
    return _singleton_repo

def get_productores_service():
    #pub = get_publisher()
    productor_repo = get_productor_repo()
    gremio_repo = get_gremio_repo()
    return ProductoresService(productor_repo, gremio_repo)
