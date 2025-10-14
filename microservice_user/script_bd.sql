--- Crear base de datos
DROP DATABASE microservice_user_bd;
CREATE DATABASE microservice_user_bd;

--- Usar la base de datos
USE microservice_user_bd;

--- Crear tabla de personas
CREATE TABLE persona (
    p_id INT AUTO_INCREMENT PRIMARY KEY,
    P_cedula VARCHAR(20) NOT NULL UNIQUE,
    p_nombre VARCHAR(100) NOT NULL,
    p_apellido VARCHAR(100) NOT NULL,
    p_telefono VARCHAR(15),
    p_direccion VARCHAR(255),
    p_fecha_nacimiento DATE
);

--- Crear tabla de usuarios
CREATE TABLE usuario (
    u_id INT AUTO_INCREMENT PRIMARY KEY,
    u_nombre_usuario VARCHAR(100) NOT NULL,
    u_contrasenia VARCHAR(100) NOT NULL,
    u_email VARCHAR(100) NOT NULL,
    u_fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    u_es_activo BOOLEAN DEFAULT TRUE,
    p_id INT,
    FOREIGN KEY (p_id) REFERENCES persona(p_id)
);

