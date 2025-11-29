# Microservicio de usuarios

## Para ejecutar este microservicio

´´´bash
python -m uvicorn api.main:app --reload --port 8001
´´´

Puerto 8001

Para ejecutar test:
1. Crear un archivo .env con este contenido:
SECRET_KEY=your_secret_key_here

```sh
PYTHONPATH=. pytest
```