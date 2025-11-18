from application.compra_service import CompraService
from infraestructure.repositories import CompraRepository, ProductoRepository, UsuarioRepository


_singleton_compra_repo = None
_singleton_compra_service = None
_singleton_usuario_repo = None
_singleton_producto_repo = None
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
def get_compra_service():
    global _singleton_compra_service
    if not _singleton_compra_service:
        compra_repo = get_compra_repo()
        usuario_repo = get_usuario_repo()
        producto_repo = get_producto_repo()
        _singleton_compra_service = CompraService(compra_repo, usuario_repo, producto_repo)
    return _singleton_compra_service
    