USE aerolinea;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE estados_ventas;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO estados_ventas (descripcion) VALUES
("Pagado"),
("Reembolsado"),
("Reservado"),
("Fraude detectado")