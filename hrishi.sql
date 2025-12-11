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