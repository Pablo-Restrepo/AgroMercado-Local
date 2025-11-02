from application.dtos import CrearProductorDTO, RegistrarProductorEnGremioDTO
from domain.models import Productor, RolEnum


def productorDTO_a_productor(dto: RegistrarProductorEnGremioDTO) -> Productor:
    return Productor(
        id=None,
        codigo=dto.codigo,
        nombres=dto.usuario.persona.p_nombre,
        apellidos=dto.usuario.persona.p_apellido,
        id_gremio=dto.id_gremio,
        rol=RolEnum.PRODUCTOR_AFILIADO,        
    )
def productorDTO_a_productor_admin(dto: CrearProductorDTO) -> Productor:
    return Productor(
        id=None,
        codigo=None,
        nombres=dto.nombres,
        apellidos=dto.apellidos,
        id_gremio=None,
        rol=RolEnum.PRODUCTOR_ADMIN,
        u_id=dto.u_id
    )