import base64
from bson import Binary
from infrastructure.mongo_collections import Producto as MongoProducto, Productor as MongoProductor, Categoria as MongoCategoria

async def on_producto_creado(event_data: dict):
    """
    Observador que se ejecuta cuando se crea un producto en MySQL.
    Crea el producto y su productor en MongoDB.
    """
    try:
        print(f"[Observer] Evento recibido: {event_data}")

        productor_data = event_data["productor"]
        categoria_data = event_data["categoria"]
        # Crear productor en MongoDB
        mongo_productor = MongoProductor(
            prod_id=productor_data["prod_id"],
            prod_nombre=productor_data["prod_nombre"],
            prod_cod_gremio =productor_data["prod_cod_gremio"],
            prod_nombre_gremio=productor_data["prod_nombre_gremio"]
        )
        mongo_categoria = MongoCategoria(
            cat_id=categoria_data["cat_id"],
            cat_nombre = categoria_data["cat_nombre"]
        )
        print("Tipo de dato img antes:",type(event_data["imagen"]), len(event_data["imagen"]))
        imagen_bytes = base64.b64decode(event_data["imagen"])
        print("Tipo de dato img despues:",type(imagen_bytes))
        imagen_binary = Binary(imagen_bytes)
        print("Tipo de dato img binary:",type(imagen_binary))
        # Crear producto en MongoDB
        MongoProducto(
            p_id=event_data["p_id"],
            p_nombre=event_data["p_nombre"],
            categoria=mongo_categoria,
            p_medicinal = event_data["p_medicinal"],
            p_unidad=event_data["p_unidad"],
            p_precio=event_data["p_precio"],
            p_stock = event_data["p_stock"],
            productor=mongo_productor,
            imagen = imagen_binary
        ).save()

        print(f"[Observer] Producto {event_data['p_nombre']} creado en MongoDB ✅")
    except Exception as e:
        print(f"[Observer] Error al crear producto en MongoDB: {e}")


async def on_producto_eliminado(prod_id: int):
    """
    Observador que se ejecuta cuando se elimina un producto en MySQL.
    Elimina el producto correspondiente en MongoDB.
    """
    try:
        # Buscar el producto en MongoDB por su primary key p_id
        producto = MongoProducto.objects(p_id=prod_id).first()

        if producto:
            producto.delete()
            print(f"[Observer] Producto {prod_id} eliminado correctamente en MongoDB.")
        else:
            print(f"[Observer] Producto {prod_id} no existe en MongoDB (nada que eliminar).")

    except Exception as e:
        print(f"[Observer] Error al eliminar producto en MongoDB: {e}")

async def on_producto_actualizado(event_data: dict):
    """
    Observador que se ejecuta cuando se actualiza un producto en MySQL.
    actualiza el producto correspondiente en MongoDB.
    """
    try:
        # Buscar el producto en MongoDB por su primary key p_id
        prod_id = event_data["p_id"]
        categoria_data = event_data["categoria"]
        mongo_categoria = MongoCategoria(
            cat_id=categoria_data["cat_id"],
            cat_nombre = categoria_data["cat_nombre"]
            )
        producto: MongoProducto = MongoProducto.objects(p_id=prod_id).first()
        if producto:
            producto.p_nombre=event_data["p_nombre"]
            producto.categoria=event_data["categoria"]
            producto.p_unidad=event_data["p_unidad"]
            producto.p_precio=event_data["p_precio"]
            producto.p_medicinal = event_data["p_medicinal"]
            producto.p_stock = event_data["p_stock"]
            producto.categoria = mongo_categoria
            imagen_bytes = base64.b64decode(event_data["imagen"])
            imagen_binary = Binary(imagen_bytes)
            producto.imagen = imagen_binary

            producto.save()
            print(f"[Observer] Producto {prod_id} fue actualizado correctamente en MongoDB.")
        else:
            print(f"[Observer] Producto {prod_id} no existe en MongoDB.")

    except Exception as e:
        print(f"[Observer] Error al actualizar producto en MongoDB: {e}")


async def on_producto_stock_actualizado(event_data: dict):
    """
    Observador que se ejecuta cuando se actualiza un producto en MySQL.
    actualiza el producto correspondiente en MongoDB.
    """
    try:
        # Buscar el producto en MongoDB por su primary key p_id
        for p in event_data:
            p_id = p["p_id"]
            producto: MongoProducto = MongoProducto.objects(p_id=p_id).first()
            if producto:
                stock_actual = producto.p_stock 
                if stock_actual < p["cant"]:
                    raise ValueError("La compra tiene un valor superior al stock actual")

                nuevo_stock = stock_actual - p["cant"]
                producto.p_stock =  nuevo_stock

                producto.save()
                print(f"[Observer] el stock del Producto {p_id} fue actualizado correctamente en MongoDB.")
            else:
                print(f"[Observer] Producto {p_id} no existe en MongoDB.")

    except Exception as e:
        print(f"[Observer] Error al eliminar producto en MongoDB: {e}")
