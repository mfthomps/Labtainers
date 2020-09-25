USE MYCO;

SELECT * FROM jobs;
SELECT * FROM dependents;
SELECT * FROM departments;

# check for update and insert permissions
INSERT INTO employees (first_name, last_name, email, phone_number, hire_date, job_id, salary, manager_id, department_id)
VALUES ('Barry','Sanders','barry.sanders@sqltutorial.org','515.464.7777','2020-08-04',10,9000.00,201,2);

SELECT * FROM employees WHERE phone_number = '515.464.7777';

UPDATE employees SET email = 'detroitlion20@MYCO.org' WHERE phone_number = '515.464.7777';

SELECT email FROM employees WHERE phone_number = '515.464.7777';

UPDATE employees SET email = 'barry.sanders@sqltutorial.org' WHERE phone_number = '515.464.7777';

DELETE FROM employees WHERE email = 'barry.sanders@sqltutorial.org';

SELECT manager_id, COUNT(DISTINCT(manager_id)) AS 'Total Managers' FROM employees GROUP BY manager_id;

CREATE TABLE IF NOT EXISTS tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    start_date DATE,
    due_date DATE,
    status TINYINT NOT NULL,
    priority TINYINT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)  ENGINE=INNODB;

SHOW TABLES;

DROP TABLE tasks;

USE mysql;
SHOW TABLES;
USE performance_schema;
SHOW TABLES;
USE sys;
SHOW TABLES;
