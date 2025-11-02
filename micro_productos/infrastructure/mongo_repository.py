import base64
from typing import List, Optional
from api.esquemas import ProductoConsulta
from infrastructure.int_query_repository import IProductoQueryRepository
from infrastructure.mongo_collections import Producto  # Documento MongoEngine

class MongoQueryRepository(IProductoQueryRepository):

    def list_productos_por_gremio(self, prod_cod_gremio: int) -> List[ProductoConsulta]:
        """
        Devuelve una lista de productos cuyo productor pertenece al gremio dado.
        """
        try:
            productos = Producto.objects(productor__prod_cod_gremio=prod_cod_gremio)
            return [
                ProductoConsulta(
                    p_nombre=p.p_nombre,
                    p_tipo=p.p_tipo,
                    p_unidad=p.p_unidad,
                    gre_nombre=p.productor.prod_nombre_gremio,
                    img= base64.b64encode(p.imagen).decode("utf-8"),
                    p_precio=p.p_precio
                )
                for p in productos
            ]
        except Exception as e:
            print(f"Error al listar productos por gremio ({prod_cod_gremio}): {e}")
            return []

    def list_productos_por_productor(self, prod_id: int) -> List[ProductoConsulta]:
        try:
            productos = Producto.objects(productor__prod_id=prod_id)
            return [
                ProductoConsulta(
                    p_nombre=p.p_nombre,
                    p_tipo=p.p_tipo,
                    p_unidad=p.p_unidad,
                    gre_nombre=p.productor.prod_nombre_gremio,
                    img= base64.b64encode(p.imagen).decode("utf-8"),
                    p_precio=p.p_precio
                )
                for p in productos
            ]
        except Exception as e:
            print(f"Error al listar productos por productor ({prod_id}): {e}")
            return []

    def get_producto_por_id(self, p_id: int) -> Optional[ProductoConsulta]:
        try:
            p = Producto.objects(p_id=p_id).first()
            if not p:
                return None
            return ProductoConsulta(
                    p_nombre=p.p_nombre,
                    p_tipo=p.p_tipo,
                    p_unidad=p.p_unidad,
                    gre_nombre=p.productor.prod_nombre_gremio,
                    img= base64.b64encode(p.imagen).decode("utf-8"),
                    p_precio=p.p_precio
                )
        except Exception as e:
            print(f"Error al obtener producto por id={p_id}: {e}")
            return None

    def list_all_productos(self) -> List[ProductoConsulta]:
        try:
            productos = Producto.objects.all()
            return [
                ProductoConsulta(
                    p_nombre=p.p_nombre,
                    p_tipo=p.p_tipo,
                    p_unidad=p.p_unidad,
                    gre_nombre=p.productor.prod_nombre_gremio,
                    img= base64.b64encode(p.imagen).decode("utf-8"),
                    p_precio=p.p_precio
                )
                for p in productos
            ]
        except Exception as e:
            print(f"Error al listar todos los productos: {e}")
            return []
