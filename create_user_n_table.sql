CREATE TABLE pushdb.T_PUSH (
id int NOT NULL AUTO_INCREMENT ,
ovenno int NOT NULL,
pushtime DATETIME,
PRIMARY KEY (id)
);

CREATE TABLE pushdb.T_CHARGE (
id int NOT NULL AUTO_INCREMENT,
ovenno int NOT NULL,
chargetime DATETIME,
PRIMARY KEY (id)
);

CREATE TABLE pushdb.T_SCHED (
id int NOT NULL AUTO_INCREMENT,
ovenno int NOT NULL,
pushtime DATETIME,
chargetime DATETIME,
PRIMARY KEY (id)
);

CREATE USER 'php_user'@'localhost' IDENTIFIED BY 'random_pass';
GRANT SELECT ON pushdb.* TO 'php_user'@'localhost';
GRANT INSERT ON pushdb.T_SCHED TO 'php_user'@'localhost';

CREATE USER 'plc_logger'@'localhost' IDENTIFIED BY 'logger123';
GRANT SELECT, INSERT ON pushdb.T_PUSH TO 'plc_logger'@'localhost';
GRANT SELECT, INSERT ON pushdb.T_CHARGE TO 'plc_logger'@'localhost';