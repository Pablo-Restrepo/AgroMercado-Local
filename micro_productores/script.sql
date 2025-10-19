-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS `micro_productores_db`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Crear usuario (si no existe) y establecer contraseña
CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY 'root';

-- Conceder permisos sobre la base de datos
GRANT ALL PRIVILEGES ON `micro_productores_db`.* TO 'root'@'localhost';

FLUSH PRIVILEGES;