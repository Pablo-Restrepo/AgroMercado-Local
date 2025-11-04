Para Dockerizar eureka, se deben seguir los siguientes pasos:
1. Compilar la aplicación de Java en un .jar
cd eureka
./mvnw clean package -DskipTests
cd ..
2. Construir la imagen de Docker
docker build -t eureka-server:latest eureka/
3. Correr imagen de Docker
docker run -p 8761:8761 --name eureka-server eureka-server:latest