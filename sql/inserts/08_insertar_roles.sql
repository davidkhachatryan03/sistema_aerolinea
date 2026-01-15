USE aerolinea;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE roles;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO roles (descripcion) VALUES
("Comandante"),
("Copiloto"),
("Jefe de cabina"),
("Tripulante de cabina"),
("Jefe de agentes"),
("Agente de mostrador"),
("Jefe de mantenimiento"),
("Técnico de mantenimiento")