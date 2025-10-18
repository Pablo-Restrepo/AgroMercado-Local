### Activar el venv
venv\Scripts\activate.bat

### Instalar FastAPI y uvicorn
pip install fastapi uvicorn

### Ejecutar app
python -m uvicorn microservice_user.api.main:app --reload --port 8001

### Entrar a la consola de la BD
mysql -u root -p

# Pip freeze guardar en requirements.txt
pip freeze > requirements.txt
