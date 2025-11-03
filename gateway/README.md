## Ejecución local
*Nota* Para correr el gateway tuve que exportar una variable de entorno de la secret key, para eso hice: export SECRET_KEY="clave_secreta" en la terminal que iba a ejecutar este proyecto.
## Información general
Métodos publicos de la gateway (no requieren autorización)
Microservicio de usuarios:
- login
- registro
Microservicio de productos:
- obtener productos
Microserivicio de productores:
- operaciones con GET
## Dockerización
Para Dockerizar, se deben seguir los siguientes pasos:
1. Compilar la aplicación de Java en un .jar
cd gateway
./mvnw clean package -DskipTests
cd ..
2. Construir la imagen de Docker
docker build -t gateway:latest gateway/
3. Correr imagen de Docker
docker run -d \
  --env-file ./gateway/.env \
  -p 8090:8090 \
  --name gateway \
  gateway:latest
*Nota:* Si se desea correr solo este contenedor, necesita hacer uso del servicio de eureka, el cual debe estar corriendo en su host (pc propio), para eso, se debe agregar "--network host \" de esta manera, el contenedor puede acceder a eureka corriendo en nuestra maquina, el comando completo sería:
docker run -d --rm \
  --env-file ./gateway/.env \
  --network host \
  -p 8090:8090 \
  --name gateway \
  gateway:latest