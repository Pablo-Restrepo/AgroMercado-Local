from application.dtos import CrearProductorDTO
from domain.models import Productor


def productorDTO_a_productor(dto: CrearProductorDTO) -> Productor:
    return Productor(
        id=None,
        codigo=dto.codigo,
        nombres=dto.nombres,
        apellidos=dto.apellidos,
        id_gremio=dto.id_gremio,
        rol=dto.rol
    )
