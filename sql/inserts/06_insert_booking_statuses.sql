USE airline;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE booking_statuses;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO booking_statuses (description) VALUES
("Paid"),
("Refunded"),
("Booked"),
("Fraud Detected")