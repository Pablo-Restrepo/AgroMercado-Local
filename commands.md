# Crear venv (desde la raíz del proyecto)
py -3 -m venv venv

### Activar el venv
venv\Scripts\activate.bat

### Instalar FastAPI y uvicorn
pip install fastapi uvicorn

### Ejecutar app
python -m uvicorn api.main:app --reload --port 8001

### Entrar a la consola de la BD
mysql -u root -p

# Pip freeze guardar en requirements.txt
pip freeze > requirements.txt
