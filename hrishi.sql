-- 1. add password column to cust_info table
ALTER TABLE cust_info ADD COLUMN password VARCHAR(255);

-- 2. update existing dummy user with password
UPDATE cust_info 
SET password = '123456' 
WHERE cust_number = '9763772464';

-- change from cust_number to mobile_no 
DROP TABLE IF EXISTS current_login;
CREATE TABLE current_login (
    mobile_no VARCHAR(15) NOT NULL
);

-- update existing user with password
UPDATE cust_info 
SET password = '123456' 
WHERE cust_number = '9763772464';

-- Add missing columns to notification_info table
ALTER TABLE notification_info 
ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST,
ADD COLUMN is_read BOOLEAN DEFAULT FALSE,
ADD COLUMN user_mobile VARCHAR(15),
ADD COLUMN notification_type VARCHAR(50) DEFAULT 'bus_proximity';

-- Add indexes for better performance
CREATE INDEX idx_notification_user ON notification_info(user_mobile, notif_date DESC);
CREATE INDEX idx_bus_location ON bus_info(latitude, longitude, last_seen);
CREATE INDEX idx_cust_location ON cust_info(latitude, longitude, last_seen);