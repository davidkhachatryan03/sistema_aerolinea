USE aerolinea;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE estados_aviones;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO estados_aviones (descripcion) VALUES 
("Activo"),
("Dado de baja"),
("Mantenimiento")