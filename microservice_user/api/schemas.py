from pydantic import BaseModel

class UsuarioRegistro(BaseModel):
    u_nombre_usuario: str
    u_contrasenia: str
    u_email: str
    p_id: int