import base64
from bson import Binary
from infrastructure.mongo_collections import Producto as MongoProducto, Productor as MongoProductor

async def on_producto_creado(event_data: dict):
    """
    Observador que se ejecuta cuando se crea un producto en MySQL.
    Crea el producto y su productor en MongoDB.
    """
    try:
        print(f"[Observer] Evento recibido: {event_data}")

        productor_data = event_data["productor"]

        # Crear productor en MongoDB
        mongo_productor = MongoProductor(
            prod_id=productor_data["prod_id"],
            prod_nombre=productor_data["prod_nombre"],
            prod_cod_gremio =productor_data["prod_cod_gremio"],
            prod_nombre_gremio=productor_data["prod_nombre_gremio"]
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
            p_tipo=event_data["p_tipo"],
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
