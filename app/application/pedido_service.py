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
    

    def obtener_pedido(db: Session, pedido_id: int):
        pedido_final= PedidoRepository.get_pedido(db, pedido_id)
        pedido_read = PedidoRead.model_validate(pedido_final, from_attributes=True)
        return pedido_read

    def obtener_pedidos(db: Session, skip: int = 0, limit: int = 100):
        pedido_final = PedidoRepository.get_pedidos(db, skip, limit)
        pedido_read = PedidoRead.model_validate(pedido_final, from_attributes=True)
        return pedido_read

    def crear_pedido(db: Session, pedido: PedidoCreate, cliente_cedula: str):
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
        pedido_read = PedidoRead.model_validate(pedido_final, from_attributes=True)
        #Almacenar los productos unitarios en la base de datos
        for pro,cant in dic_productos.items():
            producto_unitario = ProductoUnitarioSchema(producto_id=pro_id[pro.nombre], pedido_id=pedido_final.id, cantidad=cant)
            #agregar el producto unitario al pedido_read
            #pedido_read.listado_productos.append(producto_unitario)
            PedidoRepository.create_producto_unitario(db, producto_unitario)
        return pedido_read

    def actualizar_pedido(db: Session, pedido_id: int, pedido_data):
        return PedidoRepository.update_pedido(db, pedido_id, pedido_data)

    def eliminar_pedido(db: Session, pedido_id: int):
        return PedidoRepository.delete_pedido(db, pedido_id)

    def obtener_pedidos_por_cedula(db: Session, cedula: str):
         pedido_final = PedidoRepository.get_pedidos_por_cedula(db, cedula)
         pedido_read = PedidoRead.model_validate(pedido_final, from_attributes=True)
         return pedido_read

    
    @staticmethod
    def crear_producto_unitario(db: Session, producto_unitario: ProductoUnitario):
        return PedidoRepository.create_producto_unitario(db, producto_unitario)

    @staticmethod
    def obtener_productos_unitarios_por_pedido(db: Session, pedido_id: int):
        return PedidoRepository.get_productos_unitarios_por_pedido(db, pedido_id)