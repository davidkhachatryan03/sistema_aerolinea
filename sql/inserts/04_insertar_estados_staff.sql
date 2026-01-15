USE aerolinea;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE estados_staff;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO estados_staff (descripcion) VALUES
("Activo"),
("Licencia"),
("De baja"),
("Vacaciones")