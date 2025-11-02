# AgroMercado-Local

AgroMercado-Local es una API REST construida con FastAPI y SQLModel para la gestión de clientes, pedidos y productos en un mercado local.

En el sistema se implementaron los siguientes metodos:
   - Consultar productos
   - Consultar clientes
   - Crear pedido
   - Consultar pedidos por cedula de cliente
   - Consultar pedidos

Las reglas negocios estan relacionadas a la gestion de pedidos:
   1. Solo los clientes registrados puedes crear pedidos
   2. Solo los clientes pueden actualizar sus respectivos pedidos
   3. Al crear un pedido el cliente debe ingresar el nombre y cantidad que desea comprar, solo se aceptan productos que esten registrados
## Requisitos

- Python 3.12+
- pip

## Instalación

1. Clona el repositorio:
   ```sh
   git clone https://github.com/Pablo-Restrepo/AgroMercado-Local.git
   cd AgroMercado-Local
   ```

2. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## Ejecución
Inicia el servidor de desarrollo:

   ```sh
   python -m uvicorn app.main:app --reload
   ```
   
Accede a la documentación interactiva en:
http://localhost:8000/docs
