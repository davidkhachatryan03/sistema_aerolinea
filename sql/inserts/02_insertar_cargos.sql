USE aerolinea;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE cargos;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO cargos (descripcion) VALUES
("Capitán"),
("Primer oficial"),
("Tripulante de cabina"),
("Técnico de mantenimiento"),
("Agente de mostrador"),
("Gerente general")