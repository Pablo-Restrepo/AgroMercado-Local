from sqlalchemy.orm import Session
from ..models.pedido import Pedido
from ..models.cliente import Cliente
from ..models.producto import Producto
from ..models.producto_unitario import ProductoUnitario
from ..cruds.pedidoRepository import PedidoRepository
from ..schemas.pedido import PedidoCreate, PedidoRead
from ..schemas.producto_unitario import ProductoUnitario as ProductoUnitarioSchema
from .cliente_service import ClienteService
from .producto_service import ProductoService
from ..schemas.pedido import Pedido as PedidoSchema
class PedidoService:
    
    @classmethod
    def obtener_pedido(cls,db: Session, pedido_id: int):
        pedido_final= PedidoRepository.get_pedido(db, pedido_id)
        pedido_read = PedidoRead.model_validate(pedido_final, from_attributes=True)
        return pedido_read

    @classmethod
    def obtener_pedidos(cls, db: Session, skip: int = 0, limit: int = 100):
        pedidos = PedidoRepository.get_pedidos(db)
        # Validar cada pedido individualmente
        pedidos_read = [PedidoRead.model_validate(p, from_attributes=True) for p in pedidos]
        return pedidos_read


    @classmethod
    def crear_pedido(cls, db: Session, pedido: PedidoCreate, cliente_cedula: str):
        #Comprobar que el cliente existe
        cliente = ClienteService.obtener_cliente_por_cedula(db, cliente_cedula)
        if not cliente:
            raise ValueError(f"Cliente con cédula {cliente_cedula} no encontrado.")
        #Obtener la estancia de cliente sin el id
        dict_cliente = cliente.model_dump()
        dict_cliente.pop("id", None)
        cliente_model = Cliente(**dict_cliente)
        dic_productos = {}
        pro_id ={}
        #Comprobar que los productos existen
        for pro in pedido.productos.keys():
            producto = ProductoService.obtener_producto_por_nombre(db, pro)
            if not producto:
                raise ValueError(f"Producto con ID {pro} no encontrado.")
            #Agregar el producto y su cantidad al diccionario
            
            dict_producto = producto.model_dump()
            pro_id[pro] = producto.id
            dict_producto.pop("id", None)
            producto_modelo = Producto(**dict_producto)
            dic_productos[producto_modelo] = pedido.productos[pro]
        p = cliente_model.crear_pedido(dic_productos)
        pedido_schema = PedidoSchema.from_model(p)
        #Almacenar el pedido en la base de datos
        pedido_final = PedidoRepository.create_pedido(db, pedido_schema)
        #Almacenar los productos unitarios en la base de datos
        for pro,cant in dic_productos.items():
            producto_unitario = ProductoUnitarioSchema(producto_id=pro_id[pro.nombre], pedido_id=pedido_final.id, cantidad=cant)
            #agregar el producto unitario al pedido_read
            PedidoRepository.create_producto_unitario(db, producto_unitario)
        return PedidoService.obtener_pedido(db, pedido_final.id)
    
    @classmethod
    def eliminar_productos_unitarios_por_pedido(cls, db: Session, pedido_id: int):
        PedidoRepository.delete_productos_unitarios_por_pedido(db, pedido_id)

    @classmethod
    def actualizar_pedido(cls,db: Session, pedido_id: str, pedido_data, cedula_cli: str):
        cliente = ClienteService.obtener_cliente_por_cedula(db, cedula_cli)
        if not cliente:
            raise ValueError(f"Cliente con cédula {cedula_cli} no encontrado.")
        pedido = PedidoRepository.get_pedido(db, pedido_id)
        if not pedido:
            raise ValueError(f"Pedido con ID {pedido_id} no encontrado.")
        if pedido.cliente_cedula != cliente.cedula:
            raise ValueError(f"El pedido con ID {pedido_id} no pertenece al cliente con cédula {cedula_cli}.")
        if pedido.estado == "CANCELADO" or pedido.estado == "COMPLETADO":
            raise ValueError(f"El pedido con ID {pedido_id} no puede ser modificado porque está {pedido.estado}.")
        #Obtener la estancia de cliente sin el id
        dict_cliente = cliente.model_dump()
        dict_cliente.pop("id", None)
        cliente_model = Cliente(**dict_cliente)
        dic_productos = {}
        pro_id ={}
        #Comprobar que los productos existen
        for pro in pedido_data.get("productos", {}).keys():
            producto = ProductoService.obtener_producto_por_nombre(db, pro)
            if not producto:
                raise ValueError(f"Producto con ID {pro} no encontrado.")
            #Agregar el producto y su cantidad al diccionario
            dict_producto = producto.model_dump()
            pro_id[pro] = producto.id
            dict_producto.pop("id", None)
            producto_modelo = Producto(**dict_producto)
            dic_productos[producto_modelo] = pedido_data.get("productos", {})[pro]
        p = cliente_model.crear_pedido(dic_productos)
        pedido_schema = PedidoSchema.from_model(p)
        PedidoRepository.update_pedido(db, pedido_id, pedido_schema)
        PedidoService.eliminar_productos_unitarios_por_pedido(db, pedido_id)
        for pro,cant in dic_productos.items():
            producto_unitario = ProductoUnitarioSchema(producto_id=pro_id[pro.nombre], pedido_id=pedido_id, cantidad=cant)
            #agregar el producto unitario al pedido_read
            PedidoRepository.create_producto_unitario(db, producto_unitario)
        return PedidoService.obtener_pedido(db, pedido_id)

    @classmethod
    def eliminar_pedido(cls, db: Session, pedido_id: int):
        return PedidoRepository.delete_pedido(db, pedido_id)

    @classmethod
    def obtener_pedidos_por_cedula(cls, db: Session, cedula: str):
         pedido_final = PedidoRepository.get_pedidos_por_cedula(db, cedula)
         pedido_read = PedidoRead.model_validate(pedido_final, from_attributes=True)
         return pedido_read

    
    @staticmethod
    def crear_producto_unitario(db: Session, producto_unitario: ProductoUnitario):
        return PedidoRepository.create_producto_unitario(db, producto_unitario)

    @staticmethod
    def obtener_productos_unitarios_por_pedido(db: Session, pedido_id: int):
        return PedidoRepository.get_productos_unitarios_por_pedido(db, pedido_id)