# Etapa 1: Compilación (build)
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /build

# Copiar archivos de configuración de Maven
COPY pom.xml .
COPY .mvn .mvn
COPY mvnw .

# Descargar dependencias (se cachea si pom.xml no cambia)
RUN ./mvnw dependency:go-offline -B

# Copiar código fuente
COPY src ./src

# Compilar el proyecto (skip tests para build más rápido)
RUN ./mvnw clean package -DskipTests

# Etapa 2: Imagen final (runtime)
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# Copiar el JAR compilado desde la etapa de build
COPY --from=builder /build/target/*.jar app.jar

EXPOSE 8090

ENTRYPOINT ["java", "-jar", "app.jar"]