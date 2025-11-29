Para ejecutar los test debe tenerse un .env de esta forma:
DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=your_secret_key_here
RABBIT_URL=amqp://guest:guest@localhost:5672/
QUEUE_NAME=task_queue
PRODUCTORS_QUEUE=productors_queue
ALGORITHM=HS256
EUREKA_APP_NAME=my_app
EUREKA_INSTANCE_PORT=8000
EUREKA_INSTANCE_HOST=localhost
EUREKA_SERVER_URL=http://localhost:8761/eureka/
GATEWAY_HOST=http://localhost:8090


