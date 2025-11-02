# Imagen base
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Exponer el puerto del servicio FastAPI
EXPOSE 8000

# Comando para ejecutar la app
CMD ["uvicorn", "core.main:app", "--host", "0.0.0.0", "--port", "8000"]
