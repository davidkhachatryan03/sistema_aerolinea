USE aerolinea;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE estados_tarjetas_embarque;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO estados_tarjetas_embarque (descripcion) VALUES
("Emitida"),
("No show"),
("Denegada"),
("Embarcado")