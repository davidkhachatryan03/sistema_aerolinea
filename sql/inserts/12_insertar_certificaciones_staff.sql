USE aerolinea;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE certificaciones_staff;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO certificaciones_staff (id_staff, descripcion, licencia_hasta) VALUES 
(1, 'Licencia de Piloto', '2030-01-01 00:00:00'),
(2, 'Licencia de Piloto', '2029-05-15 00:00:00'),
(3, 'Licencia de Piloto', '2028-12-20 00:00:00'),
(4, 'Licencia de Piloto', '2030-06-10 00:00:00'),
(5, 'Licencia de Copiloto', '2027-08-01 00:00:00'),
(6, 'Licencia de Copiloto', '2028-02-14 00:00:00'),
(7, 'Licencia de Copiloto', '2026-11-30 00:00:00'),
(8, 'Licencia de Copiloto', '2029-07-22 00:00:00'),
(9, 'Licencia de Servicio', '2027-03-10 00:00:00'),
(10, 'Licencia de Servicio', '2028-09-05 00:00:00'),
(11, 'Licencia de Servicio', '2026-12-25 00:00:00'),
(12, 'Licencia de Servicio', '2027-04-18 00:00:00'),
(13, 'Licencia de Servicio', '2029-01-30 00:00:00'),
(14, 'Licencia de Servicio', '2030-10-12 00:00:00'),
(15, 'Licencia de Jefe', '2028-11-11 00:00:00'),
(16, 'Licencia de Jefe', '2027-06-06 00:00:00'),
(17, 'Licencia de Jefe', '2029-08-20 00:00:00'),
(18, 'Licencia de Mecánico', '2030-05-05 00:00:00'),
(19, 'Licencia de Mecánico', '2026-09-15 00:00:00'),
(20, 'Licencia de Mecánico', '2028-03-22 00:00:00');