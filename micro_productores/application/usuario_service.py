from application.dtos import UsuarioRegistro
import requests

def registrar_usuario(usuario:UsuarioRegistro):
    """Funcion que llama al microservicio de usuarios para registrar un nuevo usuario"""
    #TODO Tratar de incorporar el llamado al micro de usuarios por medio de Eureka
    url = "http://127.0.0.1:8001/usuarios/registro"
    payload = usuario.model_dump()
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
    except requests.RequestException as e:
        raise ValueError(f"Error al registrar usuario: {e}")
    if response.status_code != 200:
        raise ValueError(f"Error al registrar usuario: {response.text}")
    return response.json()

def eliminar_usuario_por_id(usuario_id: int):
    """Funcion que llama al microservicio de usuarios para eliminar un usuario por su ID"""
    #TODO Tratar de incorporar el llamado al micro de usuarios por medio de Eureka
    url = f"http://microservice_user:8000/usuarios/{usuario_id}"
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.delete(url, headers=headers)
    except requests.RequestException as e:
        raise ValueError(f"Error al eliminar usuario: {e}")
    if response.status_code != 200:
        raise ValueError(f"Error al eliminar usuario: {response.text}")
    return response.json()
    