-- Create the database
CREATE DATABASE IF NOT EXISTS dental_management_system;

-- Use the database
USE dental_management_system;

-- Create patient_record table
CREATE TABLE IF NOT EXISTS patient_record (
    Patient_Name VARCHAR(50),
    Age INT(3),
    Doctor_Conculted VARCHAR(50),
    Address VARCHAR(150),
    Phone_Number BIGINT(15)
);

-- Create salary_record table
CREATE TABLE IF NOT EXISTS salary_record (
    Employee_Name VARCHAR(50),
    Proffession VARCHAR(20),
    Salary_Amount VARCHAR(9),
    Address VARCHAR(150),
    Phone_Number BIGINT(15)
);

-- Create accounts table
CREATE TABLE IF NOT EXISTS accounts (
    User_Name VARCHAR(20) PRIMARY KEY,
    password VARCHAR(30) UNIQUE
);
