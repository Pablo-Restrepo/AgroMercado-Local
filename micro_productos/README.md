## Ejecutar desde micro_productos
python -m uvicorn core.main:app --reload

## Test
Para ejecutarlos se debe tener un .env como:

SECRET_KEY=test_secret_key_for_testing_purposes_only_12345
ALGORITHM=HS256


MYSQL_USER=test_user
MYSQL_PASSWORD=test_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=agromercado_test

MONGO_USER=test_user
MONGO_PASSWORD=test_password
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=agromercado_test


RABBIT_USER=guest
RABBIT_PASS=guest
RABBIT_HOST=localhost
RABBIT_PORT=5672
PRODUCTORES_QUEUE=productores_queue
PRODUCTOS_CREADOS_QUEUE=productos_creados_queue
PRODUCTOS_ACTUALIZADOS_QUEUE=productos_actualizados_queue
PRODUCTOS_STOCK_ACTUALIZADO_QUEUE=productos_stock_actualizado_queue

EUREKA_APP_NAME=micro-productos
EUREKA_INSTANCE_PORT=8001
EUREKA_INSTANCE_HOST=localhost
EUREKA_HOST=localhost

Para despues hacer 
```sh
pytest
```

