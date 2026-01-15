USE aerolinea;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE estados_vuelos;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO estados_vuelos (descripcion) VALUES 
("Programado"),
("En vuelo"),
("Aterrizado"),
("Cancelado")