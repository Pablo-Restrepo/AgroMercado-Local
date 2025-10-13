Para ejecutar correctamente el micro, primero deben aplicarse las migraciones (teniendo en cuenta que ya se instalaron los requerimientos).
Para eso, se hace: 
alembic revision --autogenerate -m "mensaje"
alembic upgrade head
Posteriormente se inicia el servidor con:
uvicorn main:app --reload