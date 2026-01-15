USE aerolinea;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE certificaciones_staff;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO certificaciones_staff (id_staff, descripcion, licencia_hasta) VALUES 
(1, 'Licencia de Piloto de Transporte de Línea Aérea (TLA)', '2026-05-20 00:00:00'),
(2, 'Habilitación de Vuelo por Instrumentos (IFR)', '2025-11-15 00:00:00'),
(3, 'Certificado Médico Aeronáutico Clase 1', '2025-08-10 00:00:00'),
(4, 'Habilitación Multimotor Terrestre (MEP)', '2027-03-30 00:00:00'),
(5, 'Licencia de Piloto Comercial de Avión (PCA)', '2026-09-12 00:00:00'),
(6, 'Certificación de Competencia Lingüística OACI Nivel 5', '2028-01-20 00:00:00'),
(7, 'Habilitación Tipo (Type Rating) Jet Privado', '2026-07-09 00:00:00'),
(8, 'Curso de Prevención de Accidentes y Seguridad (SMS)', '2029-06-24 00:00:00'),
(9, 'Certificado de Tripulante de Cabina de Pasajeros (TCP)', '2026-12-01 00:00:00'),
(10, 'Curso de Primeros Auxilios y RCP Avanzado', '2025-10-30 00:00:00'),
(11, 'Gestión de Recursos de la Tripulación (CRM)', '2026-02-14 00:00:00'),
(12, 'Procedimientos de Emergencia y Evacuación', '2025-11-20 00:00:00'),
(13, 'Manejo de Mercancías Peligrosas (DGR)', '2027-04-05 00:00:00'),
(14, 'Protocolo de Servicio VIP y Atención a Pasajeros', '2030-01-01 00:00:00'),
(15, 'Licencia de Mecánico de Mantenimiento de Aeronaves (MMA)', '2026-08-17 00:00:00'),
(16, 'Especialización en Aviónica y Sistemas Eléctricos', '2027-11-04 00:00:00'),
(17, 'Habilitación en Motores a Reacción y Turbinas', '2026-03-10 00:00:00'),
(18, 'Certificación en Sistemas Globales de Distribución (GDS)', '2026-05-25 00:00:00'),
(19, 'Seguridad de la Aviación Civil (AVSEC)', '2025-09-30 00:00:00'),
(20, 'Atención al Cliente y Resolución de Conflictos', '2027-12-15 00:00:00');