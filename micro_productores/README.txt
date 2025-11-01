Para ejecutar correctamente el micro, primero deben aplicarse las migraciones (teniendo en cuenta que ya se instalaron los requerimientos).
Para eso, se hace: 
1. Ingresar a mysql y correr el script "script.sql"
2. Iniciar el micro(estando en la raiz de micro_productores): uvicorn main:app --reload
*Importante*: Se debe tener el servicio de Rabbit MQ corriendo

