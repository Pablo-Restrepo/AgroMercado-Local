import base64
from typing import List, Optional
from api.esquemas import ProductoConsulta
from infrastructure.int_query_repository import IProductoQueryRepository
from infrastructure.mongo_collections import Categoria, Producto  # Documento MongoEngine

class MongoQueryRepository(IProductoQueryRepository):

    def list_productos_por_gremio(self, prod_cod_gremio: int) -> List[ProductoConsulta]:
        """
        Devuelve una lista de productos cuyo productor pertenece al gremio dado.
        """
        try:
            productos = Producto.objects(productor__prod_cod_gremio=prod_cod_gremio)
            return [
                ProductoConsulta(
                    p_id = p.p_id,
                    p_nombre=p.p_nombre,
                    cat_id=p.categoria.cat_id,
                    p_unidad=p.p_unidad,
                    p_medicinal = p.p_medicinal,
                    gre_nombre=p.productor.prod_nombre_gremio,
                    p_stock = p.p_stock,
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
                    p_id = p.p_id,
                    p_nombre=p.p_nombre,
                    cat_id=p.categoria.cat_id,
                    p_unidad=p.p_unidad,
                    p_medicinal = p.p_medicinal,
                    p_stock = p.p_stock,
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
                    p_id = p.p_id,
                    p_nombre=p.p_nombre,
                    cat_id=p.categoria.cat_id,
                    p_unidad=p.p_unidad,
                    p_stock = p.p_stock,
                    p_medicinal = p.p_medicinal,
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
                    p_id = p.p_id,
                    p_nombre=p.p_nombre,
                    cat_id=p.categoria.cat_id,
                    p_unidad=p.p_unidad,
                    p_stock = p.p_stock,
                    p_medicinal = p.p_medicinal,
                    gre_nombre=p.productor.prod_nombre_gremio,
                    img= base64.b64encode(p.imagen).decode("utf-8"),
                    p_precio=p.p_precio
                )
                for p in productos
            ]
        except Exception as e:
            print(f"Error al listar todos los productos: {e}")
            return []
    
    def list_all_productos_por_categoria(self,cat_id:int) -> List[ProductoConsulta]:
        """
        Devuelve una lista de productos de la categoria dada
        """
        try:
            productos = Producto.objects(categoria__cat_id=cat_id)
            return [
                ProductoConsulta(
                    p_id = p.p_id,
                    p_nombre=p.p_nombre,
                    cat_id=p.categoria.cat_id,
                    p_unidad=p.p_unidad,
                    p_medicinal = p.p_medicinal,
                    gre_nombre=p.productor.prod_nombre_gremio,
                    p_stock = p.p_stock,
                    img= base64.b64encode(p.imagen).decode("utf-8"),
                    p_precio=p.p_precio
                )
                for p in productos
            ]
        except Exception as e:
            print(f"Error al listar productos por categoria ({cat_id}): {e}")
            return []
    
    def list_all_productos_medicinales(self) -> List[ProductoConsulta]:
        """
        Devuelve una lista de productos medicinales
        """
        try:
            productos = Producto.objects(p_medicinal=True)
            return [
                ProductoConsulta(
                    p_id = p.p_id,
                    p_nombre=p.p_nombre,
                    cat_id=p.categoria.cat_id,
                    p_unidad=p.p_unidad,
                    p_medicinal = p.p_medicinal,
                    gre_nombre=p.productor.prod_nombre_gremio,
                    p_stock = p.p_stock,
                    img= base64.b64encode(p.imagen).decode("utf-8"),
                    p_precio=p.p_precio
                )
                for p in productos
            ]
        except Exception as e:
            print(f"Error al listar productos por medicionales: {e}")
            return []


        
    def list_all_productos_por_categoria(self,cat_id:int) -> List[ProductoConsulta]:
        try:
            productos = Producto.objects(categoria__cat_id=cat_id)
            return [
                ProductoConsulta(
                    p_id = p.p_id,
                    p_nombre=p.p_nombre,
                    cat_id=p.categoria.cat_id,
                    p_unidad=p.p_unidad,
                    p_medicinal = p.p_medicinal,
                    gre_nombre=p.productor.prod_nombre_gremio,
                    p_stock = p.p_stock,
                    img= base64.b64encode(p.imagen).decode("utf-8"),
                    p_precio=p.p_precio
                )
                for p in productos
            ]
        except Exception as e:
            print(f"Error al listar productos por categoria: {e}")
            return []

    
    def list_productos_por_categoria_gremio(self,gre_id:int,cat_id:int) -> List[ProductoConsulta]:
        try:
            productos = Producto.objects(categoria__cat_id=cat_id,productor__prod_cod_gremio=gre_id)
            return [
                ProductoConsulta(
                    p_id = p.p_id,
                    p_nombre=p.p_nombre,
                    cat_id=p.categoria.cat_id,
                    p_unidad=p.p_unidad,
                    p_medicinal = p.p_medicinal,
                    gre_nombre=p.productor.prod_nombre_gremio,
                    p_stock = p.p_stock,
                    img= base64.b64encode(p.imagen).decode("utf-8"),
                    p_precio=p.p_precio
                )
                for p in productos
            ]
        except Exception as e:
            print(f"Error al listar productos de la categoria {cat_id} en el gremio {gre_id}: {e}")
            return []
   
    
    def list_productos_por_categoria_productor(self,prod_id:int,cat_id:int) -> List[ProductoConsulta]:
        try:
            productos = Producto.objects(categoria__cat_id=cat_id,productor__prod_id=prod_id)
            return [
                ProductoConsulta(
                    p_id = p.p_id,
                    p_nombre=p.p_nombre,
                    cat_id=p.categoria.cat_id,
                    p_unidad=p.p_unidad,
                    p_medicinal = p.p_medicinal,
                    gre_nombre=p.productor.prod_nombre_gremio,
                    p_stock = p.p_stock,
                    img= base64.b64encode(p.imagen).decode("utf-8"),
                    p_precio=p.p_precio
                )
                for p in productos
            ]
        except Exception as e:
            print(f"Error al listar productos de la categoria {cat_id} del productor {prod_id}: {e}")
            return []
    
    

    def list_productos_medicinales_gremio(self, gre_id:int)  -> List[ProductoConsulta]:
        try:
            productos = Producto.objects(productor__prod_cod_gremio=gre_id, p_medicinal=True)
            return [
                ProductoConsulta(
                    p_id = p.p_id,
                    p_nombre=p.p_nombre,
                    cat_id=p.categoria.cat_id,
                    p_unidad=p.p_unidad,
                    p_medicinal = p.p_medicinal,
                    gre_nombre=p.productor.prod_nombre_gremio,
                    p_stock = p.p_stock,
                    img= base64.b64encode(p.imagen).decode("utf-8"),
                    p_precio=p.p_precio
                )
                for p in productos
            ]
        except Exception as e:
            print(f"Error al listar productos medicinales del gremio {gre_id}: {e}")
            return []
    
    
    def list_productos_medicinales_productor(self, prod_id:int)  -> List[ProductoConsulta]:
        try:
            productos = Producto.objects(productor__prod_id=prod_id, p_medicinal=True)
            return [
                ProductoConsulta(
                    p_id = p.p_id,
                    p_nombre=p.p_nombre,
                    cat_id=p.categoria.cat_id,
                    p_unidad=p.p_unidad,
                    p_medicinal = p.p_medicinal,
                    gre_nombre=p.productor.prod_nombre_gremio,
                    p_stock = p.p_stock,
                    img= base64.b64encode(p.imagen).decode("utf-8"),
                    p_precio=p.p_precio
                )
                for p in productos
            ]
        except Exception as e:
            print(f"Error al listar productos medicinales del productor {prod_id}: {e}")
            return []

