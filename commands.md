# Comandos generales
## Crear venv (desde la raíz del proyecto)
py -3 -m venv venv

## Activar el venv
venv\Scripts\activate.bat

## Instalar FastAPI y uvicorn
pip install fastapi uvicorn

## Ejecutar app
python -m uvicorn api.main:app --reload --port 8001

## Entrar a la consola de la BD
mysql -u root -p

## Pip freeze guardar en requirements.txt
pip freeze > requirements.txt

# Docker compose
Para levantar el proyecto, debe ubicarse en la carpeta raiz ".../Agromercado-Local" y ejecutar:
- docker compose up
Si desea realizar un cambio en los micros después de haber hecho docker compose, asegurese de eliminar la imagen creada de ese micro y volver a ejecutar el comando anterior.