USE aerolinea;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE staff;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO staff (nombre_completo, id_cargo_actual, id_estado_actual) VALUES 
('Carlos Gómez', 1, 1),
('Lucía Benitez', 1, 1), 
('Ricardo Darín', 1, 2),
('Valeria Lynch', 1, 1),
('Mariana López', 2, 1),
('Esteban Quito', 2, 1),
('Julián Álvarez', 2, 3),
('Lionel Messi', 2, 1),
('Lali Espósito', 3, 1),
('Tini Stoessel', 3, 1),
('Fito Páez', 3, 2),
('Charly García', 3, 1),
('Alejandro Ruiz', 3, 1),
('Mirtha Legrand', 3, 1),
('Roberto Fernández', 4, 2),  
('Gustavo Cerati', 4, 1),     
('Norberto Pappo', 4, 1),
('Sofía Martínez', 5, 1),    
('Diego Maradona', 5, 4),    
('Susana Giménez', 5, 1);