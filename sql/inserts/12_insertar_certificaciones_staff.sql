USE aerolinea;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE certificaciones_staff;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO certificaciones_staff (id_staff, descripcion, licencia_hasta) VALUES 
(1, 'Licencia de Capitán', '2028-12-31 23:59:59'),
(2, 'Licencia de Capitán', '2027-06-15 23:59:59'),
(3, 'Licencia de Capitán', '2026-11-30 23:59:59'),
(4, 'Licencia de Capitán', '2029-03-01 23:59:59'),
(5, 'Licencia de Primer Oficial', '2028-05-20 23:59:59'),
(6, 'Licencia de Primer Oficial', '2027-08-10 23:59:59'),
(7, 'Licencia de Primer Oficial', '2026-10-15 23:59:59'),
(8, 'Licencia de Primer Oficial', '2030-01-01 23:59:59'),
(9, 'Licencia de Tripulante de Cabina', '2027-12-31 23:59:59'),
(10, 'Licencia de Agente de Tierra', '2027-03-15 23:59:59'),
(11, 'Licencia de Agente de Tierra', '2026-08-30 23:59:59'),
(12, 'Licencia de Agente de Tierra', '2028-01-01 23:59:59'),
(13, 'Licencia de Agente de Tierra', '2027-05-20 23:59:59'),
(14, 'Licencia de Agente de Tierra', '2026-12-10 23:59:59'),
(15, 'Licencia de Jefe de Tierra', '2029-10-31 23:59:59'),
(16, 'Licencia de Jefe de Tierra', '2028-02-28 23:59:59'),
(17, 'Licencia de Jefe de Cabina', '2028-06-30 23:59:59'),
(18, 'Licencia de Jefe de Cabina', '2027-04-15 23:59:59'),
(19, 'Licencia de Jefe de Cabina', '2026-09-20 23:59:59'),
(20, 'Licencia de Mantenimiento', '2031-12-31 23:59:59'),
(21, 'Licencia de Mantenimiento', '2029-07-10 23:59:59'),
(22, 'Licencia de Ingeniería Aeronáutica', '2035-12-31 23:59:59'),
(23, 'Licencia de Ingeniería Aeronáutica', '2030-11-01 23:59:59'),
(24, 'Licencia de Ingeniería Aeronáutica', '2035-12-31 23:59:59'),
(25, 'Licencia de Tester', '2032-01-01 23:59:59');