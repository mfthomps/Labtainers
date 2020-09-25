USE MYCO;

INSERT INTO employees (first_name, last_name, email, phone_number, hire_date, job_id, salary, manager_id, department_id) 
VALUES ('James','McNair','james.mcnair@sqltutorial.org','515.123.4587','2001-08-25',6,7900.00,108,10);

SELECT email FROM employees WHERE last_name = 'McNair';

DELETE FROM employees WHERE phone_number = '515.123.4587';

SELECT * FROM employees WHERE first_name = 'James';

SELECT CONCAT(first_name, ' ', last_name) AS name FROM employees;

SELECT * FROM dependents WHERE employee_id = 206;

INSERT INTO departments (department_id, department_name, location_id) VALUES (12, 'Maintenance', 1500);

SELECT department_name FROM departments where department_name = 'Maintenance';

DELETE FROM departments WHERE department_name = 'Maintenance';

USE mysql;

SHOW TABLES; 

USE performance_schema;

SHOW TABLES;

USE sys;

SHOW TABLES;