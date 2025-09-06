# AgroMercado-Local

AgroMercado-Local es una API REST construida con FastAPI y SQLModel para la gestión de clientes, pedidos, productos y pagos en un mercado local.

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