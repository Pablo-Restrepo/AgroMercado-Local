from domain.models import Gremio, Productor
from domain.repository import IGremioRepository, IProductorRepository

class ProductorService:
    def __init__(self, gremio_repo: IGremioRepository, productor_repo: IProductorRepository):
        self.gremio_repo = gremio_repo
        self.productor_repo = productor_repo
    # Métodos del servicio
    # TO DO