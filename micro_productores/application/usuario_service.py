from application.dtos import UsuarioRegistro
#import requests

def registrar_usuario(usuario:UsuarioRegistro):
    """Funcion que llama al microservicio de usuarios para registrar un nuevo usuario"""
    #TODO Tratar de incorporar el llamado al micro de usuarios por medio de Eureka
    """url = "http://microservice_user:8000/usuarios/registro"
    payload = usuario.model_dump()
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"Error al registrar usuario: {response.text}")
    return response.json()"""

    # Temporalmente se retorna una respuesta 200
    return {"status_code": 200, "data": {"message": "Usuario registrado exitosamente (simulado)"}}
def eliminar_usuario_por_email(email:str):
    """Funcion que llama al microservicio de usuarios para eliminar un usuario por su email"""
    #TODO Tratar de incorporar el llamado al micro de usuarios por medio de Eureka
    """url = f"http://microservice_user:8000/usuarios/eliminar/{email}"
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"Error al eliminar usuario: {response.text}")
    return response.json()"""

    # Temporalmente se retorna una respuesta 200
    return {"status_code": 200, "data": {"message": "Usuario eliminado exitosamente (simulado)"}}