USE airline;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE flight_statuses;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO flight_statuses (description) VALUES 
("Scheduled"),
("In Flight"),
("Landed"),
("Canelled")