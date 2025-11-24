from application.services import CompraService, EnvioService, ProductoService, UsuarioService
from infraestructure.repositories import CompraRepository, ProductoRepository, UsuarioRepository
from core.config import settings
from py_eureka_client.eureka_client import EurekaClient

_singleton_compra_repo = None
_singleton_compra_service = None
_singleton_usuario_service = None
_singleton_usuario_repo = None
_singleton_producto_service = None
_singleton_producto_repo = None
_singleton_envio_service = None
_singleton_envio_repo = None
def get_producto_repo():
    global _singleton_producto_repo
    if not _singleton_producto_repo:        
        _singleton_producto_repo = ProductoRepository()
    return _singleton_producto_repo
def get_compra_repo():
    global _singleton_compra_repo
    if not _singleton_compra_repo:
        _singleton_compra_repo = CompraRepository()
    return _singleton_compra_repo
def get_usuario_repo():
    global _singleton_usuario_repo
    if not _singleton_usuario_repo:        
        _singleton_usuario_repo = UsuarioRepository()
    return _singleton_usuario_repo
def get_envio_repo():
    global _singleton_envio_repo
    if not _singleton_envio_repo:
        from infraestructure.repositories import EnvioRepository
        _singleton_envio_repo = EnvioRepository()
    return _singleton_envio_repo
def get_envio_service():
    global _singleton_envio_service
    if not _singleton_envio_service:
        envio_repo = get_envio_repo()
        producto_repo = get_producto_repo()
        _singleton_envio_service = EnvioService(envio_repo, producto_repo)
    return _singleton_envio_service
def get_compra_service():
    global _singleton_compra_service
    if not _singleton_compra_service:
        compra_repo = get_compra_repo()
        usuario_repo = get_usuario_repo()
        producto_repo = get_producto_repo()
        _singleton_compra_service = CompraService(compra_repo, usuario_repo, producto_repo)
    return _singleton_compra_service
def get_usuario_service():
    global _singleton_usuario_service
    if not _singleton_usuario_service:
        usuario_repo = get_usuario_repo()
        _singleton_usuario_service = UsuarioService(usuario_repo)
    return _singleton_usuario_service
def get_producto_service():
    global _singleton_producto_service
    if not _singleton_producto_service:
        producto_repo = get_producto_repo()
        _singleton_producto_service = ProductoService(producto_repo)
    return _singleton_producto_service
eureka_client = EurekaClient(
    eureka_server=settings.EUREKA_SERVER_URL,
    app_name=settings.EUREKA_APP_NAME,
    instance_port=settings.EUREKA_INSTANCE_PORT,
    instance_host=settings.EUREKA_INSTANCE_HOST,
)