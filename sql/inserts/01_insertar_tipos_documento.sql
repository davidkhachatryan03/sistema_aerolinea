USE aerolinea;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE tipos_documento;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO tipos_documento (tipo_documento) VALUES
("Documento Nacional de Identidad (DNI)"),
("Pasaporte"),
("VISA")