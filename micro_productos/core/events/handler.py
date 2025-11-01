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
            prod_nombre_gremio=productor_data["prod_nombre_gremio"]
        )

        # Crear producto en MongoDB
        MongoProducto(
            p_id=event_data["p_id"],
            p_nombre=event_data["p_nombre"],
            p_tipo=event_data["p_tipo"],
            p_unidad=event_data["p_unidad"],
            p_precio=event_data["p_precio"],
            productor=mongo_productor
        ).save()

        print(f"[Observer] Producto {event_data['p_nombre']} creado en MongoDB ✅")
    except Exception as e:
        print(f"[Observer] Error al crear producto en MongoDB: {e}")
