CREATE TABLE IF NOT EXISTS productor (
  prod_id INT AUTO_INCREMENT PRIMARY KEY,
  prod_nombre VARCHAR(100),
  prod_apellido VARCHAR(100),
  prod_cod_gremio INT,
  prod_nombre_gremio VARCHAR(100)
);

INSERT INTO productor (prod_nombre, prod_apellido, prod_cod_gremio, prod_nombre_gremio)
VALUES 
  ('Juan', 'Perez', 101, 'Asociacion de Citricos'),
  ('Mary', 'Gonzalez', 102, 'Gremio de Cafeteros'),
  ('Carlos', 'Lopez', 103, 'Union de Agricultores');
