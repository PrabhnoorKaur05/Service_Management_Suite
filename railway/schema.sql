CREATE DATABASE IF NOT EXISTS railway_management_system;
USE railway_management_system;

CREATE TABLE IF NOT EXISTS pdata (
    custno INT PRIMARY KEY,
    custname VARCHAR(50),
    addr VARCHAR(150),
    jrdate DATE,
    source VARCHAR(50),
    destination VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS tkt (
    custno INT,
    tkt_tot INT,
    lug_tot INT,
    g_tot INT,
    FOREIGN KEY (custno) REFERENCES pdata(custno)
);
