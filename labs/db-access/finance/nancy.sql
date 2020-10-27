USE MYCO;

SELECT employee_id,first_name,last_name FROM employees WHERE employee_id = 109;

SELECT * FROM jobs WHERE job_id = 12;

SELECT * FROM dependents WHERE employee_id = 110;

UPDATE employees SET phone_number = '515.354.4568' WHERE employee_id = 111;

SELECT phone_number FROM employees WHERE employee_id = 111; 

UPDATE employees SET phone_number = '515.124.4369' WHERE employee_id = 111;

USE mysql;
SHOW TABLES;
USE performance_schema;
SHOW TABLES;
USE sys;
SHOW TABLES;
