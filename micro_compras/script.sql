DROP DATABASE IF EXISTS `microservice_compras_bd`;
-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS `microservice_compras_bd`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Crear usuario (si no existe) y establecer contraseña
CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY 'root';

-- Conceder permisos sobre la base de datos
GRANT ALL PRIVILEGES ON `microservice_compras_bd`.* TO 'root'@'localhost';

FLUSH PRIVILEGES;

--Datos de prueba, un usuario y dos productos
USE `microservice_compras_bd`;
INSERT INTO usuario (u_nombre, u_email, u_es_activo) VALUES ('Pablo Perez', 'pablo.perez@example.com', True);
INSERT INTO producto (p_nombre, p_id_gremio, p_precio, p_unidad, p_stock) VALUES ('Manzanas',1, 2.50, 'kg', 100);
INSERT INTO producto (p_nombre, p_id_gremio, p_precio, p_unidad, p_stock) VALUES ('Naranjas', 1, 3.00, 'kg', 150);