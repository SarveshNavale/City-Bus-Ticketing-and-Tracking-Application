INSERT INTO stops_info (stop_name, track_no, latitude, longitude,stop_no) VALUES ('City Bus Stand', 0, 16.9914520, 73.2950390, 1);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Malnaka', 0, 16.9906412, 73.3059455, 2);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Maruti Mandir', 0, 16.9914520, 73.2950390, 3);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Godbole', 1, 16.9950168, 73.3190417, 4);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Charmalay', 1, 16.9964154, 73.3208352 , 5);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Kokan Nagar', 1, 17.0016121, 73.3245508, 6);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Radha Krishna Nagar', 1, 17.0035718, 73.3269559, 7);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Aadishti', 1, 17.0099843, 73.3301266 , 8);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Finolex', 1, 17.0116948, 73.3353763 ,9 );
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Jambhul Phata', 1, 17.0173015, 73.3356863, 10);

INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Shivaji Nagar', 2, 16.9913144, 73.3213231,4 );
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Salvi', 2, 16.9940142, 73.3273839, 5);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('JK Files', 2, 16.9955833, 73.3309237, 6);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Railway Station', 2, 16.9980804, 73.3578163, 7);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Mahalakshmi', 2, 17.0015264, 73.3720352, 8);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Khedshi', 2, 17.0139045, 73.3949133, 9 );
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Hatkhamba', 2, 17.0150127, 73.4054062, 10);

INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Jogalekar', 3, 16.9897621, 73.3145604, 4);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Power House', 3, 16.9885660, 73.3178680, 5);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('I.T.I', 3, 16.9867141, 73.3230856, 6);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Nachane', 3, 16.9853803, 73.3291087, 7);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Godown', 3, 16.9865191, 73.3334559, 8);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Shantinagar', 3, 16.9845721, 73.3396431, 9);
INSERT INTO stops_info (stop_name, track_no, latitude, longitude, stop_no) VALUES ('Kajarghati', 3, 16.9769149, 73.3674380, 10);


CREATE TABLE IF NOT EXISTS fuel_consumption (
    id INT AUTO_INCREMENT PRIMARY KEY,
    total_liter DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2) DEFAULT NULL
);
