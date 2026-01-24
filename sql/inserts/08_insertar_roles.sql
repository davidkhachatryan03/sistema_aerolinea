USE aerolinea;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE roles;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO roles (descripcion) VALUES
("PIC"),
("SIC"),
("Auxiliar de vuelo"),
("Supervisor de cabina"),
("Agente de check-in"),
("Agente de embarque"),
("Supervisor de agentes"),
("Mecánico de línea"),
("Mecánico de hangar"),
("Inspector de aviones")