USE airline;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE airplane_statuses;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO airplane_statuses (description) VALUES 
("Active"),
("Inactive"),
("Maintenance")