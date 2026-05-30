USE airline;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE ticket_statuses;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO ticket_statuses (description) VALUES
("Paid"),
("Refunded"),
("Booked"),
("Fraud Detected")