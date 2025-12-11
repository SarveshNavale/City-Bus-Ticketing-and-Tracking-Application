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
ALTER TABLE cust_info
  ADD COLUMN latitude DECIMAL(10,7) DEFAULT NULL,
  ADD COLUMN longitude DECIMAL(10,7) DEFAULT NULL,
  ADD COLUMN last_seen DATETIME DEFAULT NULL;
  
  
ALTER TABLE cust_info
ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;

INSERT INTO cust_info (cust_name, cust_number, cust_age, cust_email)
VALUES 
('Sarvesh Navale', '9763772464', 18, 'sarveshnavale18@gmail.com');


CREATE TABLE stops_info (
    Stop_name VARCHAR(100),         
    track_no   INT,           
    latitude DECIMAL(10,7) DEFAULT NULL,
    longitude DECIMAL(10,7) DEFAULT NULL           
);
ALTER TABLE stops_info
ADD COLUMN stop_no int;

CREATE TABLE tickets_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    start_dest VARCHAR(150) NOT NULL,
    final_dest VARCHAR(150) NOT NULL,
    no_of_tickets INT NOT NULL,
    ticket_holder VARCHAR(150) NOT NULL,
    mobile_no VARCHAR(15) NOT NULL,
    ticket_number VARCHAR(30) UNIQUE NOT NULL,
    amount_paid DECIMAL(10,2) NOT NULL,
    issue_date DATE NOT NULL,
    issue_time TIME NOT NULL
);

create table current_login (
	mobo_no int NOT NULL
);

CREATE TABLE passes_info (
    id INT AUTO_INCREMENT PRIMARY KEY,

    pass_holder VARCHAR(150) NOT NULL,

    pass_number VARCHAR(50) UNIQUE NOT NULL,

    amount_paid DECIMAL(10,2) NOT NULL,

    mobile_no VARCHAR(15) NOT NULL,

    issue_date DATE NOT NULL,
    issue_time TIME NOT NULL
);
-- Create table (safe columns)
CREATE TABLE IF NOT EXISTS bus_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bus_no INT NOT NULL,
    no_plate VARCHAR(16) NOT NULL,
    route INT NOT NULL,                -- 1 = kokan, 2 = highway, 3 = nachane, 4 = railway
    latitude DOUBLE DEFAULT NULL,
    longitude DOUBLE DEFAULT NULL,
    last_seen DATETIME DEFAULT NULL
);

-- Insert exactly 12 buses (initial lat/lon = City Bus Stand)
-- City Bus Stand coordinates used as spawn initial position
INSERT INTO bus_info (bus_no, no_plate, route, latitude, longitude) VALUES
 (101, 'MH08-101-A', 1, 16.991452, 73.295039),
 (101, 'MH08-101-B', 1, 16.991452, 73.295039),
 (101, 'MH08-101-C', 1, 16.991452, 73.295039),

 (102, 'MH08-102-A', 2, 16.991452, 73.295039),
 (102, 'MH08-102-B', 2, 16.991452, 73.295039),
 (102, 'MH08-102-C', 2, 16.991452, 73.295039),

 (103, 'MH08-103-A', 3, 16.991452, 73.295039),
 (103, 'MH08-103-B', 3, 16.991452, 73.295039),
 (103, 'MH08-103-C', 3, 16.991452, 73.295039),

 (98,  'MH08-098-A', 4, 16.991452, 73.295039),
 (98,  'MH08-098-B', 4, 16.991452, 73.295039),
 (98,  'MH08-098-C', 4, 16.991452, 73.295039);
 
 
 create table current_login (
	 mobile_no VARCHAR(15) NOT NULL
 );




