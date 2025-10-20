# ARCHIVO REGISTRO EUREKA

crear un archivo llamado eureka_registry.py

from py_eureka_client.eureka_client import EurekaClient

client = EurekaClient(
    eureka_server="http://localhost:8761/eureka",
    app_name="NOMBRE-DEL-SERVICIO",
    instance_port=PUERTO,
    instance_host="localhost"
)

# EN EL MAIN

llamar la funcion client.start() al levantar la aplicacion.
aqui esta implementado con @app.on_event("startup"), pero este metodo esta obsoleto, se debe utilizar lifespan. 
en caso de tener problemas con lifespan se puede emplear esta version. 
from infra.eureka_registry import client

@app.on_event("startup")
async def startup_event():
    await client.start()


# REQUERIMIENTOS

httpcore==1.0.9
httpx==0.28.1