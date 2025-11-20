DROP DATABASE IF EXISTS `microservice_productos_bd`;
-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS `microservice_productos_bd`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Crear usuario (si no existe) y establecer contraseña
CREATE USER IF NOT EXISTS 'root'@'mysql' IDENTIFIED BY 'root';

-- Conceder permisos sobre la base de datos
GRANT ALL PRIVILEGES ON `microservice_productos_bd`.* TO 'root'@'mysql';

FLUSH PRIVILEGES;