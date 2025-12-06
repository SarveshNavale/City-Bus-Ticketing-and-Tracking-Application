create database RotaryClub_Database;

CREATE TABLE cust_info (
    cust_name   VARCHAR(100),
    cust_number VARCHAR(15),
    cust_age    INT,
    cust_email  VARCHAR(100)
);
CREATE TABLE notification_info (
    notif_date        DATE,
    notif_time        TIME,
    notif_heading     VARCHAR(250),
    notif_description TEXT
);
CREATE TABLE Admin_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Admin_id VARCHAR(10),
    OTP INT
);
INSERT INTO Admin_info (Admin_id, OTP)
VALUES ('TC918710', 4085);       -- for TC
INSERT INTO Admin_info (Admin_id, OTP)     -- for complaint checkerr
VALUES ('ADM918710', 4085);


CREATE TABLE complaints (
    idc INT AUTO_INCREMENT PRIMARY KEY,   
    comp_time     TIME,                  
    comp_generator VARCHAR(100),         
    comp_gen_no   VARCHAR(20),           
    comp_status   VARCHAR(50)            
);


