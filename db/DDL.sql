CREATE DATABASE IF NOT EXISTS f22_databases;
USE f22_databases;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS sections;
DROP TABLE IF EXISTS attendances;

CREATE TABLE courses(
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(128) UNIQUE,
    prof_name VARCHAR(128),
    time VARCHAR(128)
);

CREATE TABLE sections(
    section_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT REFERENCES courses(course_id),
    section_date DATE NOT NULL,
    UNIQUE(course_id, section_date)
);

CREATE TABLE attendances(
    section_id INT NOT NULL,
    student_id INT NOT NULL,
    PRIMARY KEY(section_id, student_id)
);
