#tests for insert/delete/update permissions
use MYCO;

SELECT first_name, last_name, email, phone_number, job_id, department_id FROM employees;


INSERT INTO employees (first_name, last_name, email, phone_number, hire_date, job_id, salary, manager_id, department_id)
VALUES ('Mike','Tyson','mike.tyson@sqltutorial.org','515.464.5555','2020-08-05',3,6000.00,101,1);

SELECT * FROM employees WHERE phone_number = '515.464.5555';

UPDATE employees SET email = 'IronMike@MYCO.org' WHERE phone_number = '515.464.5555';

SELECT email FROM employees WHERE phone_number = '515.464.5555';

UPDATE employees SET email = 'mike.tyson@sqltutorial.org' WHERE phone_number = '515.464.5555';

DELETE FROM employees WHERE email = 'mike.tyson@sqltutorial.org';

SELECT min_salary FROM jobs WHERE job_id = 01;
SELECT max_salary FROM jobs WHERE job_id = 01;

USE mysql;
SHOW TABLES;
USE performance_schema;
SHOW TABLES;
USE sys;
SHOW TABLES;
