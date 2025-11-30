"""Modulo de mapeadores entre entidades de dominio y modelos de base de datos SQLModel"""

from domain.entities.compra import Compra
from domain.entities.envio import Envio
from domain.entities.producto_unitario import ProductoUnitario
from infraestructure.db.modelsSQL import CompraModel, EnvioModel, ProductoUnitarioModel


def compra_entity_to_model(compra_entity: Compra)-> CompraModel:
    from infraestructure.db.modelsSQL import CompraModel
    compra_model = CompraModel(
        c_id=compra_entity.id,
        u_id=compra_entity.id_usuario,
        c_productos= [producto_unitario_entity_to_model(pu) for pu in compra_entity.productos],
        c_fecha=compra_entity.fecha,
        c_total=compra_entity.total,
        c_estado=compra_entity.estado.nombre
    )
    return compra_model
def compra_model_to_entity(compra_model: CompraModel) -> Compra:
    from domain.entities.estado_compra import (
        EstadoCompraEnum,
        EstadoCreada,
        EstadoConfirmada,
        EstadoEnviada,
        EstadoPagada,
        EstadoCancelada
    )
    estado_map = {
        EstadoCompraEnum.CREADA: EstadoCreada(),
        EstadoCompraEnum.CONFIRMADA: EstadoConfirmada(),
        EstadoCompraEnum.ENVIADA: EstadoEnviada(),
        EstadoCompraEnum.PAGADA: EstadoPagada(),
        EstadoCompraEnum.CANCELADA: EstadoCancelada()
    }
    estado_entity = estado_map.get(compra_model.c_estado, EstadoCreada())
    compra_entity = Compra(
        id=compra_model.c_id,
        id_usuario=compra_model.u_id,
        productos= [producto_unitario_model_to_entity(pu) for pu in compra_model.c_productos],
        fecha=compra_model.c_fecha,
        total=compra_model.c_total,
        estado=estado_entity
    )
    return compra_entity
def producto_unitario_model_to_entity(pu_model:ProductoUnitarioModel)-> ProductoUnitario:
    from domain.entities.producto_unitario import ProductoUnitario
    producto_unitario_entity = ProductoUnitario(
        id=pu_model.pu_id,
        id_producto=pu_model.p_id,
        cantidad=pu_model.pu_cantidad,
        precio_unitario=pu_model.pu_precio_unitario,
        unidad=pu_model.pu_unidad        
    )
    return producto_unitario_entity
def producto_unitario_entity_to_model(pu_entity:ProductoUnitario)-> ProductoUnitarioModel:
    from infraestructure.db.modelsSQL import ProductoUnitarioModel
    pu_model = ProductoUnitarioModel(
        pu_id=pu_entity.id,
        p_id=pu_entity.id_producto,
        pu_cantidad=pu_entity.cantidad,
        pu_precio_unitario=pu_entity.precio_unitario,
        pu_unidad=pu_entity.unidad,
        pu_subtotal=pu_entity.subtotal
    )
    return pu_model
def envio_entity_to_model(envio_entity:Envio)-> EnvioModel:
    from infraestructure.db.modelsSQL import EnvioModel
    envio_model = EnvioModel(
        e_id=envio_entity.id,
        e_id_gremio=envio_entity.id_gremio,
        e_destino=envio_entity.destino,        
        e_valor=envio_entity.valor,
        e_estado=envio_entity.estado.nombre,
        e_fecha_envio=envio_entity.fecha_envio,        
        e_c_id=envio_entity.compra.id
    )
    return envio_model
def envio_model_to_entity(envio_model:EnvioModel) -> Envio:
    from domain.entities.envio import Envio
    from domain.entities.estado_envio import (
        EstadoDespachado,
        EstadoPendiente,
        EstadoEnRuta,
        EstadoEntregado
    )
    estado_map = {
        "PENDIENTE": EstadoPendiente(),
        "DESPACHADO": EstadoDespachado(),
        "EN_RUTA": EstadoEnRuta(),
        "ENTREGADO": EstadoEntregado()
    }
    estado_entity = estado_map.get(envio_model.e_estado, EstadoPendiente())
    envio_entity = Envio(
        id=envio_model.e_id,
        id_gremio=envio_model.e_id_gremio,
        compra=compra_model_to_entity(envio_model.e_compra),
        destino=envio_model.e_destino,
        valor=envio_model.e_valor,        
        fecha_envio=envio_model.e_fecha_envio,
        estado=estado_entity
    )
    return envio_entity