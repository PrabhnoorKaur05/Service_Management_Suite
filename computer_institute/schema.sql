CREATE DATABASE IF NOT EXISTS cims;

USE cims;

CREATE TABLE IF NOT EXISTS candidate_details (
    adm_no INT PRIMARY KEY,
    candidate_name VARCHAR(50),
    course_select VARCHAR(20)
);
