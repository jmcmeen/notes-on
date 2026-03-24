# Introduction to Oracle Database

## Table of Contents

1. [What is Oracle Database](#what-is-oracle-database)
2. [Installation and Setup](#installation-and-setup)
3. [Database Architecture](#database-architecture)
4. [Data Types](#data-types)
5. [Creating Tables](#creating-tables)
6. [CRUD Operations](#crud-operations)
7. [Querying Data](#querying-data)
8. [PL/SQL Basics](#plsql-basics)
9. [Indexes and Performance](#indexes-and-performance)
10. [Views and Materialized Views](#views-and-materialized-views)
11. [Transactions](#transactions)
12. [Python Integration](#python-integration)
13. [Practice Exercises](#practice-exercises)
14. [Summary](#summary)

---

## What is Oracle Database

### Overview

Oracle Database is a multi-model, enterprise-grade relational database management system (RDBMS) developed by Oracle Corporation. Key features:

- **Enterprise-ready**: Built for high availability, scalability, and security
- **ACID compliant**: Full transactional integrity with robust concurrency control
- **PL/SQL**: Powerful procedural extension to SQL for server-side logic
- **Multi-model**: Supports relational, JSON, XML, spatial, and graph data
- **Cross-platform**: Runs on Linux, Windows, Solaris, and cloud environments (OCI)
- **Industry standard**: Widely used in banking, telecommunications, and government

### Oracle Editions

| Edition | Use Case |
| ------- | -------- |
| **Enterprise Edition (EE)** | Large-scale production with advanced features (partitioning, RAC, Data Guard) |
| **Standard Edition 2 (SE2)** | Small to mid-size applications, up to 2 sockets |
| **Express Edition (XE)** | Free, lightweight edition for development and learning (limited to 2 CPU threads, 2 GB RAM, 12 GB user data) |
| **Oracle Cloud (Autonomous)** | Fully managed cloud database with self-tuning capabilities |

---

## Installation and Setup

### Installing Oracle XE (Express Edition)

Oracle XE is the best starting point for learning. Download from the official Oracle website.

```bash
# On Oracle Linux / RHEL / CentOS (RPM-based)
sudo yum install oracle-database-xe-21c-1.0-1.ol8.x86_64.rpm
sudo /etc/init.d/oracle-xe-21c configure   # sets SYS and SYSTEM passwords
```

### Connecting with SQL*Plus

```bash
sqlplus system/your_password@localhost:1521/XEPDB1  # connect as SYSTEM
sqlplus / as sysdba                                  # connect with admin privileges
```

```sql
SELECT banner FROM v$version;  -- check Oracle version
SHOW USER;                     -- current user
SHOW CON_NAME;                 -- current container
```

### SQL Developer

Oracle SQL Developer is a free GUI tool for database development:

- **Download**: Available from oracle.com (requires JDK)
- **Connection setup**: Host = localhost, Port = 1521, Service = XEPDB1
- **Features**: SQL worksheet, data modeler, export/import, debugging PL/SQL

### Creating a Practice User

```sql
ALTER SESSION SET CONTAINER = XEPDB1;  -- switch to pluggable database

CREATE USER dev_user IDENTIFIED BY dev_password
    DEFAULT TABLESPACE users TEMPORARY TABLESPACE temp QUOTA UNLIMITED ON users;

GRANT CONNECT, RESOURCE TO dev_user;
GRANT CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE TO dev_user;
```

---

## Database Architecture

### Instances and Databases

Oracle separates the **instance** (memory + processes) from the **database** (physical files):

- **Instance**: SGA (shared memory for buffer cache, shared pool, redo log buffer) + background processes (DBWR, LGWR, SMON, PMON)
- **PGA (Program Global Area)**: Private memory allocated for each server process
- **Database files**: Data files (.dbf), redo log files (.log), and control files

### Tablespaces and Data Files

A **tablespace** is a logical storage container that maps to one or more physical data files.

```sql
SELECT tablespace_name, status, contents FROM dba_tablespaces;  -- view tablespaces

-- Create a custom tablespace
CREATE TABLESPACE app_data
    DATAFILE '/opt/oracle/oradata/app_data01.dbf' SIZE 100M
    AUTOEXTEND ON NEXT 50M MAXSIZE 2G;
```

### Schemas and Users

In Oracle, a **schema** is directly tied to a **user** — creating a user automatically creates a schema of the same name.

```sql
-- List non-system users
SELECT username, account_status, created FROM dba_users
WHERE oracle_maintained = 'N' ORDER BY created DESC;

-- Objects in a schema
SELECT object_type, COUNT(*) FROM all_objects
WHERE owner = 'DEV_USER' GROUP BY object_type;
```

---

## Data Types

### Numeric Types

```sql
column_name NUMBER          -- arbitrary precision
column_name NUMBER(10)      -- integer up to 10 digits
column_name NUMBER(10, 2)   -- decimal with 2 fractional digits (e.g., 99999999.99)
column_name BINARY_FLOAT    -- 32-bit IEEE float (fast math)
column_name BINARY_DOUBLE   -- 64-bit IEEE double (fast math)
```

### Character Types

```sql
column_name VARCHAR2(100)   -- variable-length, up to 4000 bytes (32767 with MAX_STRING_SIZE=EXTENDED)
column_name CHAR(10)        -- fixed-length, padded with spaces
column_name NVARCHAR2(100)  -- Unicode variable-length string
column_name CLOB            -- character large object, up to 4 GB
```

### Date, Time, and Binary Types

```sql
column_name DATE                            -- date and time to the second (no fractional seconds)
column_name TIMESTAMP                       -- date/time with fractional seconds (default 6 digits)
column_name TIMESTAMP WITH TIME ZONE        -- includes time zone offset
column_name TIMESTAMP WITH LOCAL TIME ZONE  -- converts to session time zone
column_name INTERVAL DAY TO SECOND          -- duration in days, hours, minutes, seconds
column_name RAW(200)                        -- raw binary data, up to 2000 bytes
column_name BLOB                            -- binary large object, up to 4 GB
column_name JSON                            -- native JSON type (Oracle 21c+)
```

---

## Creating Tables

### Basic Table Creation

```sql
CREATE TABLE departments (
    department_id   NUMBER(4)    GENERATED ALWAYS AS IDENTITY,  -- auto-increment (12c+)
    department_name VARCHAR2(50) NOT NULL,
    location        VARCHAR2(100),
    created_at      TIMESTAMP    DEFAULT SYSTIMESTAMP,
    CONSTRAINT pk_departments PRIMARY KEY (department_id)
);

CREATE TABLE employees (
    employee_id   NUMBER(6)     GENERATED ALWAYS AS IDENTITY,
    first_name    VARCHAR2(50)  NOT NULL,
    last_name     VARCHAR2(50)  NOT NULL,
    email         VARCHAR2(100) CONSTRAINT uq_emp_email UNIQUE,
    hire_date     DATE          DEFAULT SYSDATE,
    salary        NUMBER(10,2)  CONSTRAINT chk_salary CHECK (salary > 0),
    department_id NUMBER(4),
    CONSTRAINT pk_employees PRIMARY KEY (employee_id),
    CONSTRAINT fk_emp_dept FOREIGN KEY (department_id)
        REFERENCES departments(department_id) ON DELETE SET NULL
);
```

### Sequences (Pre-12c Auto-Increment)

```sql
CREATE SEQUENCE emp_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

-- Use the sequence during insert
INSERT INTO employees (employee_id, first_name, last_name, email)
VALUES (emp_seq.NEXTVAL, 'John', 'Doe', 'john.doe@example.com');

SELECT emp_seq.CURRVAL FROM dual;  -- current value (only after NEXTVAL in session)
```

### Table Modifications

```sql
ALTER TABLE employees ADD phone VARCHAR2(20);           -- add a column
ALTER TABLE employees MODIFY phone VARCHAR2(30);        -- change type or size
ALTER TABLE employees RENAME COLUMN phone TO phone_num; -- rename a column
ALTER TABLE employees DROP COLUMN phone_num;            -- drop a column

-- Add a constraint after table creation
ALTER TABLE employees ADD CONSTRAINT chk_email CHECK (email LIKE '%@%.%');
```

---

## CRUD Operations

### INSERT

```sql
-- Single row insert
INSERT INTO departments (department_name, location)
VALUES ('Engineering', 'Building A');

-- Multiple rows using INSERT ALL (requires dummy SELECT at the end)
INSERT ALL
    INTO departments (department_name, location) VALUES ('Sales', 'Building B')
    INTO departments (department_name, location) VALUES ('Marketing', 'Building C')
SELECT 1 FROM dual;

-- Insert from a subquery
INSERT INTO archived_employees (employee_id, first_name, last_name)
SELECT employee_id, first_name, last_name FROM employees WHERE hire_date < DATE '2020-01-01';
```

### SELECT

```sql
-- Basic select with filtering and expressions
SELECT
    first_name || ' ' || last_name AS full_name,  -- string concatenation with ||
    salary * 12 AS annual_salary,
    NVL(department_id, 0) AS dept_id              -- NVL replaces NULL with a default
FROM employees
WHERE department_id = 1 AND salary > 50000
ORDER BY salary DESC;
```

### UPDATE

```sql
-- Update specific rows
UPDATE employees
SET salary = salary * 1.10,       -- 10% raise
    hire_date = SYSDATE
WHERE department_id = 1;

-- Update with a subquery
UPDATE employees e
SET salary = (SELECT AVG(salary) * 1.05 FROM employees
              WHERE department_id = e.department_id)
WHERE employee_id = 101;
```

### DELETE and MERGE

```sql
-- Delete specific rows
DELETE FROM employees
WHERE employee_id = 105;

-- MERGE (upsert: insert or update in one statement)
MERGE INTO employees tgt USING new_hires src ON (tgt.email = src.email)
WHEN MATCHED THEN
    UPDATE SET tgt.salary = src.salary, tgt.department_id = src.department_id
WHEN NOT MATCHED THEN
    INSERT (first_name, last_name, email, salary, department_id)
    VALUES (src.first_name, src.last_name, src.email, src.salary, src.department_id);
```

---

## Querying Data

### JOINs

```sql
-- Inner join
SELECT e.first_name, d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id;

-- Left outer join (includes employees with no department)
SELECT e.first_name, d.department_name
FROM employees e
LEFT JOIN departments d ON e.department_id = d.department_id;

-- Self-join: employees and their managers
SELECT e.first_name AS employee, m.first_name AS manager
FROM employees e LEFT JOIN employees m ON e.manager_id = m.employee_id;
```

### Subqueries

```sql
-- Subquery in WHERE (employees earning above average)
SELECT first_name, salary FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Correlated subquery (departments with more than 5 employees)
SELECT d.department_name FROM departments d
WHERE (SELECT COUNT(*) FROM employees e WHERE e.department_id = d.department_id) > 5;

-- EXISTS check (departments that have at least one employee)
SELECT d.department_name FROM departments d
WHERE EXISTS (SELECT 1 FROM employees e WHERE e.department_id = d.department_id);
```

### Common Table Expressions (CTEs)

```sql
-- CTE for readability and reuse
WITH dept_stats AS (
    SELECT department_id, COUNT(*) AS emp_count,
           AVG(salary) AS avg_salary, MAX(salary) AS max_salary
    FROM employees GROUP BY department_id
)
SELECT d.department_name, ds.emp_count, ds.avg_salary
FROM dept_stats ds JOIN departments d ON ds.department_id = d.department_id
WHERE ds.emp_count > 3
ORDER BY ds.avg_salary DESC;

-- Recursive CTE (organizational hierarchy)
WITH org_chart (employee_id, first_name, manager_id, lvl) AS (
    SELECT employee_id, first_name, manager_id, 1  -- anchor: top-level managers
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.first_name, e.manager_id, oc.lvl + 1  -- recursive member
    FROM employees e JOIN org_chart oc ON e.manager_id = oc.employee_id
)
SELECT LPAD(' ', (lvl - 1) * 4) || first_name AS org_tree, lvl
FROM org_chart ORDER BY lvl, first_name;
```

### Analytic / Window Functions

```sql
-- ROW_NUMBER, RANK, DENSE_RANK: ranking within partitions
SELECT first_name, department_id, salary,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS row_num,
    RANK()       OVER (ORDER BY salary DESC) AS rank_gaps,    -- gaps after ties
    DENSE_RANK() OVER (ORDER BY salary DESC) AS rank_no_gaps  -- no gaps
FROM employees;

-- LAG and LEAD: access previous/next rows
SELECT first_name, hire_date,
    LAG(hire_date, 1)  OVER (ORDER BY hire_date) AS prev_hire,
    LEAD(hire_date, 1) OVER (ORDER BY hire_date) AS next_hire
FROM employees;

-- Running total with SUM window function
SELECT first_name, salary,
    SUM(salary) OVER (ORDER BY hire_date ROWS UNBOUNDED PRECEDING) AS running_total
FROM employees;
```

### GROUP BY, HAVING, and Row Limiting

```sql
-- GROUP BY with HAVING filter
SELECT department_id, COUNT(*) AS emp_count, ROUND(AVG(salary), 2) AS avg_salary
FROM employees GROUP BY department_id
HAVING COUNT(*) >= 3 ORDER BY avg_salary DESC;

-- ROWNUM (legacy — applied before ORDER BY, so wrap in subquery)
SELECT * FROM (
    SELECT first_name, salary FROM employees ORDER BY salary DESC
) WHERE ROWNUM <= 5;

-- FETCH FIRST (Oracle 12c+, preferred and ANSI-compliant)
SELECT first_name, salary FROM employees
ORDER BY salary DESC
FETCH FIRST 5 ROWS ONLY;

-- Pagination with OFFSET (page 2, 10 rows per page)
SELECT first_name, salary FROM employees
ORDER BY salary DESC
OFFSET 10 ROWS FETCH NEXT 10 ROWS ONLY;
```

---

## PL/SQL Basics

### Anonymous Blocks and Variables

```plsql
-- PL/SQL anonymous block
DECLARE
    v_name     VARCHAR2(100);          -- variable declaration
    v_salary   NUMBER(10,2) := 0;     -- initialize with default
    v_bonus    CONSTANT NUMBER := 500; -- constant
    c_tax_rate CONSTANT NUMBER := 0.25;
BEGIN
    SELECT first_name || ' ' || last_name, salary
    INTO v_name, v_salary               -- SELECT INTO assigns query results to variables
    FROM employees
    WHERE employee_id = 101;

    v_salary := v_salary + v_bonus;     -- assignment operator is :=

    DBMS_OUTPUT.PUT_LINE('Employee: ' || v_name);
    DBMS_OUTPUT.PUT_LINE('Adjusted salary: ' || v_salary);
    DBMS_OUTPUT.PUT_LINE('After tax: ' || v_salary * (1 - c_tax_rate));
END;
/
```

### Conditional Logic and Loops

```plsql
DECLARE
    v_grade CHAR(1);
    v_score NUMBER := 85;
BEGIN
    -- IF / ELSIF / ELSE
    IF v_score >= 90 THEN
        v_grade := 'A';
    ELSIF v_score >= 80 THEN
        v_grade := 'B';
    ELSIF v_score >= 70 THEN
        v_grade := 'C';
    ELSE
        v_grade := 'F';
    END IF;

    -- CASE expression
    DBMS_OUTPUT.PUT_LINE('Result: ' ||
        CASE v_grade
            WHEN 'A' THEN 'Excellent'
            WHEN 'B' THEN 'Good'
            ELSE 'Needs Improvement'
        END
    );

    -- FOR loop (iterator is implicitly declared)
    FOR i IN 1..5 LOOP
        DBMS_OUTPUT.PUT_LINE('Iteration: ' || i);
    END LOOP;

    FOR i IN REVERSE 1..5 LOOP                -- reverse FOR loop
        DBMS_OUTPUT.PUT_LINE('Countdown: ' || i);
    END LOOP;

    -- WHILE loop
    DECLARE v_num NUMBER := 1;
    BEGIN
        WHILE v_num <= 5 LOOP
            v_num := v_num + 1;
        END LOOP;
    END;

    -- Basic LOOP with EXIT WHEN
    DECLARE v_counter NUMBER := 1;
    BEGIN
        LOOP
            EXIT WHEN v_counter > 5;
            v_counter := v_counter + 1;
        END LOOP;
    END;
END;
/
```

### Cursors

```plsql
DECLARE
    CURSOR c_employees IS
        SELECT employee_id, first_name, salary FROM employees WHERE department_id = 1;
    v_emp c_employees%ROWTYPE;  -- record variable matching cursor columns
BEGIN
    OPEN c_employees;
    LOOP
        FETCH c_employees INTO v_emp;
        EXIT WHEN c_employees%NOTFOUND;
        DBMS_OUTPUT.PUT_LINE(v_emp.first_name || ': ' || v_emp.salary);
    END LOOP;
    CLOSE c_employees;

    -- Simpler: cursor FOR loop (auto open/fetch/close)
    FOR rec IN (SELECT first_name, salary FROM employees WHERE department_id = 2) LOOP
        DBMS_OUTPUT.PUT_LINE(rec.first_name || ': ' || rec.salary);
    END LOOP;
END;
/
```

### Stored Procedures and Functions

```plsql
-- Stored procedure: performs an action, uses IN/OUT parameters
CREATE OR REPLACE PROCEDURE give_raise (
    p_employee_id IN  NUMBER,
    p_percentage  IN  NUMBER,
    p_new_salary  OUT NUMBER
) AS
BEGIN
    UPDATE employees SET salary = salary * (1 + p_percentage / 100)
    WHERE employee_id = p_employee_id
    RETURNING salary INTO p_new_salary;
    COMMIT;
END give_raise;
/

-- Call a procedure
DECLARE
    v_new_sal NUMBER;
BEGIN
    give_raise(101, 10, v_new_sal);  -- 10% raise for employee 101
    DBMS_OUTPUT.PUT_LINE('New salary: ' || v_new_sal);
END;
/

-- Function: returns a value, can be used in SQL
CREATE OR REPLACE FUNCTION get_annual_salary (
    p_employee_id IN NUMBER
) RETURN NUMBER AS
    v_salary NUMBER;
BEGIN
    SELECT salary * 12 INTO v_salary FROM employees WHERE employee_id = p_employee_id;
    RETURN v_salary;
EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN NULL;
END get_annual_salary;
/

SELECT first_name, get_annual_salary(employee_id) AS annual_pay FROM employees;
```

### Packages

```plsql
-- Package specification (public interface)
CREATE OR REPLACE PACKAGE emp_pkg AS
    PROCEDURE hire_employee(p_first_name VARCHAR2, p_last_name VARCHAR2, p_dept_id NUMBER);
    FUNCTION  get_headcount(p_dept_id NUMBER) RETURN NUMBER;
END emp_pkg;
/

-- Package body (implementation)
CREATE OR REPLACE PACKAGE BODY emp_pkg AS
    PROCEDURE hire_employee(p_first_name VARCHAR2, p_last_name VARCHAR2, p_dept_id NUMBER) IS
    BEGIN
        INSERT INTO employees (first_name, last_name, department_id)
        VALUES (p_first_name, p_last_name, p_dept_id);
        COMMIT;
    END hire_employee;

    FUNCTION get_headcount(p_dept_id NUMBER) RETURN NUMBER IS
        v_count NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM employees WHERE department_id = p_dept_id;
        RETURN v_count;
    END get_headcount;
END emp_pkg;
/

-- Call package members with dot notation
BEGIN
    emp_pkg.hire_employee('Jane', 'Smith', 1);
    DBMS_OUTPUT.PUT_LINE('Headcount: ' || emp_pkg.get_headcount(1));
END;
/
```

### Triggers

```plsql
-- Row-level trigger: runs once per affected row (:OLD/:NEW access before/after values)
CREATE OR REPLACE TRIGGER trg_emp_audit
    BEFORE UPDATE OF salary ON employees FOR EACH ROW
BEGIN
    INSERT INTO salary_audit (employee_id, old_salary, new_salary, changed_at)
    VALUES (:OLD.employee_id, :OLD.salary, :NEW.salary, SYSTIMESTAMP);
END;
/

-- Statement-level trigger: runs once per DML statement (no FOR EACH ROW)
CREATE OR REPLACE TRIGGER trg_no_weekend_changes
    BEFORE INSERT OR UPDATE OR DELETE ON employees
BEGIN
    IF TO_CHAR(SYSDATE, 'DY', 'NLS_DATE_LANGUAGE=ENGLISH') IN ('SAT', 'SUN') THEN
        RAISE_APPLICATION_ERROR(-20001, 'No changes allowed on weekends');
    END IF;
END;
/
```

### Exception Handling

```plsql
DECLARE
    v_salary NUMBER;
BEGIN
    SELECT salary INTO v_salary FROM employees WHERE employee_id = 99999;
    DBMS_OUTPUT.PUT_LINE('Salary: ' || v_salary);
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('Employee not found');
    WHEN TOO_MANY_ROWS THEN
        DBMS_OUTPUT.PUT_LINE('Query returned multiple rows');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error ' || SQLCODE || ': ' || SQLERRM);  -- log error
        RAISE;  -- re-raise after logging
END;
/

-- User-defined exception with RAISE_APPLICATION_ERROR
DECLARE
    v_salary NUMBER := -500;
BEGIN
    IF v_salary < 0 THEN
        RAISE_APPLICATION_ERROR(-20002, 'Salary cannot be negative');
    END IF;
END;
/
```

---

## Indexes and Performance

### B-Tree Indexes

```sql
-- B-tree index: default type, good for high-cardinality columns
CREATE INDEX idx_emp_last_name ON employees(last_name);
CREATE INDEX idx_emp_dept_salary ON employees(department_id, salary);  -- composite
CREATE UNIQUE INDEX idx_emp_email ON employees(email);                 -- unique

-- Function-based index (for case-insensitive searches)
CREATE INDEX idx_emp_upper_name ON employees(UPPER(last_name));
SELECT * FROM employees WHERE UPPER(last_name) = 'SMITH';  -- uses the index
```

### Bitmap Indexes

```sql
-- Bitmap index: efficient for low-cardinality columns (e.g., status, gender)
-- Best for read-heavy data warehousing; avoid in OLTP with frequent DML
CREATE BITMAP INDEX idx_emp_status ON employees(employment_status);
```

### EXPLAIN PLAN and Optimizer Hints

```sql
-- Generate and view an execution plan
EXPLAIN PLAN FOR
SELECT e.first_name, d.department_name FROM employees e
JOIN departments d ON e.department_id = d.department_id WHERE e.salary > 70000;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);  -- view the plan

-- Common optimizer hints (use sparingly)
SELECT /*+ INDEX(e idx_emp_dept_salary) */ first_name, salary  -- force index use
FROM employees e WHERE department_id = 1;

SELECT /*+ FULL(e) */ first_name, salary   -- force full table scan
FROM employees e WHERE department_id = 1;

SELECT /*+ PARALLEL(e, 4) */ COUNT(*) FROM employees e;  -- 4 parallel workers

-- Gather statistics (important after bulk data loads)
BEGIN
    DBMS_STATS.GATHER_TABLE_STATS('DEV_USER', 'EMPLOYEES',
        estimate_percent => DBMS_STATS.AUTO_SAMPLE_SIZE);
END;
/
```

---

## Views and Materialized Views

### Standard Views

```sql
-- A view is a saved query — no data stored, it runs the query each time
CREATE OR REPLACE VIEW v_employee_details AS
SELECT e.employee_id, e.first_name || ' ' || e.last_name AS full_name,
       e.salary, d.department_name, e.hire_date
FROM employees e LEFT JOIN departments d ON e.department_id = d.department_id;

-- Query the view like a regular table
SELECT full_name, department_name FROM v_employee_details WHERE salary > 60000;

-- Updatable view (simple views without joins/aggregates can be updated)
CREATE OR REPLACE VIEW v_engineering AS
SELECT employee_id, first_name, last_name, salary, department_id
FROM employees WHERE department_id = 1
WITH CHECK OPTION;  -- prevents rows that violate the WHERE clause
```

### Materialized Views

```sql
-- A materialized view stores query results physically for faster reads
CREATE MATERIALIZED VIEW mv_dept_summary
    BUILD IMMEDIATE         -- populate now
    REFRESH FAST ON COMMIT  -- auto-refresh when base tables change (requires MV logs)
    ENABLE QUERY REWRITE    -- let the optimizer substitute this MV in queries
AS
SELECT d.department_id, d.department_name,
       COUNT(*) AS emp_count, SUM(e.salary) AS total_salary
FROM employees e
JOIN departments d ON e.department_id = d.department_id
GROUP BY d.department_id, d.department_name;

-- Materialized view log (required for FAST refresh)
CREATE MATERIALIZED VIEW LOG ON employees
    WITH ROWID, SEQUENCE (department_id, salary) INCLUDING NEW VALUES;

-- Manual refresh: 'C' = complete, 'F' = fast
BEGIN
    DBMS_MVIEW.REFRESH('MV_DEPT_SUMMARY', 'C');
END;
/
```

---

## Transactions

### COMMIT, ROLLBACK, and SAVEPOINT

```sql
-- Oracle does NOT auto-commit by default (unlike MySQL)
INSERT INTO departments (department_name, location) VALUES ('Legal', 'Building D');
SAVEPOINT sp_after_legal;

INSERT INTO departments (department_name, location) VALUES ('Finance', 'Building E');
ROLLBACK TO sp_after_legal;  -- undo Finance insert, keep Legal
COMMIT;                      -- commit only the Legal insert

-- ROLLBACK undoes all uncommitted changes
INSERT INTO departments (department_name, location) VALUES ('Temp', 'Building Z');
ROLLBACK;  -- the Temp row is discarded
```

### Transaction Isolation Levels

Oracle supports two isolation levels:

```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;   -- default: each query sees committed data
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;      -- all queries see data as of txn start
SET TRANSACTION READ ONLY;                         -- no DML allowed, consistent snapshot
```

- **READ COMMITTED** (default): no dirty reads; non-repeatable and phantom reads possible
- **SERIALIZABLE**: no dirty, non-repeatable, or phantom reads

---

## Python Integration

### Connecting with python-oracledb

```python
# python-oracledb is the modern driver (successor to cx_Oracle): pip install oracledb
import oracledb

# Thin mode — no Oracle Client needed
connection = oracledb.connect(
    user="dev_user", password="dev_password", dsn="localhost:1521/XEPDB1")

cursor = connection.cursor()
cursor.execute("SELECT first_name, salary FROM employees WHERE department_id = :dept_id",
               {"dept_id": 1})  # bind variables use colon prefix

for first_name, salary in cursor:
    print(f"{first_name}: ${salary:,.2f}")

cursor.close()
connection.close()
```

### CRUD with Bind Variables

```python
import oracledb

with oracledb.connect(user="dev_user", password="dev_password",
                       dsn="localhost:1521/XEPDB1") as conn:
    with conn.cursor() as cur:

        # INSERT with bind variables (prevents SQL injection)
        cur.execute(
            "INSERT INTO employees (first_name, last_name, email, salary, department_id) "
            "VALUES (:fname, :lname, :email, :sal, :dept)",
            {"fname": "Alice", "lname": "Wong", "email": "awong@example.com",
             "sal": 75000, "dept": 1}
        )

        # Batch insert with executemany (list of dicts)
        cur.executemany(
            "INSERT INTO employees (first_name, last_name, email, salary, department_id) "
            "VALUES (:fname, :lname, :email, :sal, :dept)",
            [{"fname": "Bob", "lname": "Lee", "email": "blee@example.com", "sal": 68000, "dept": 2},
             {"fname": "Carol", "lname": "Davis", "email": "cd@example.com", "sal": 72000, "dept": 1}]
        )

        conn.commit()  # explicitly commit the transaction
```

### Calling PL/SQL from Python

```python
import oracledb

with oracledb.connect(user="dev_user", password="dev_password",
                       dsn="localhost:1521/XEPDB1") as conn:
    with conn.cursor() as cur:
        # Call a stored procedure with an OUT parameter
        new_salary = cur.var(oracledb.NUMBER)
        cur.callproc("give_raise", [101, 10, new_salary])
        print(f"New salary: {new_salary.getvalue()}")

        # Call a function directly
        annual = cur.callfunc("get_annual_salary", oracledb.NUMBER, [101])
        print(f"Annual salary: {annual}")
```

---

## Practice Exercises

### Exercise 1: Table Design

Create a `products` table with columns for `product_id` (auto-increment), `product_name`, `category`, `price`, `stock_quantity`, and `created_at`. Add appropriate constraints.

### Exercise 2: Data Manipulation

Insert 5 products, update the price of one category by 15%, and delete products with zero stock.

### Exercise 3: Analytical Query

Write a query that ranks products by price within each category using `DENSE_RANK()`, and shows the price difference from the next cheapest product using `LAG()`.

### Exercise 4: PL/SQL Procedure

Create a stored procedure `restock_product` that takes a product ID and quantity, updates the stock, and raises an exception if the product does not exist.

### Exercise 5: View and Performance

Create a view showing product summaries by category (count, avg price, total stock). Then create a materialized view for the same query and compare execution plans.

### Exercise 6: Python Script

Write a Python script using `oracledb` that connects to the database, inserts a new product with bind variables, and retrieves all products in a given category.

---

## Summary

These notes cover the core concepts of Oracle Database:

1. **Architecture**: Instances, SGA/PGA, tablespaces, schemas, and the user-schema relationship
2. **Data Types**: NUMBER, VARCHAR2, CLOB, DATE, TIMESTAMP, RAW, and large object types
3. **Table Design**: CREATE TABLE with identity columns, sequences, constraints, and foreign keys
4. **CRUD**: INSERT (single, bulk, INSERT ALL), UPDATE, DELETE, and MERGE for upserts
5. **Querying**: JOINs, subqueries, CTEs (including recursive), analytic functions (ROW_NUMBER, RANK, LAG, LEAD), GROUP BY/HAVING, and FETCH FIRST pagination
6. **PL/SQL**: Variables, control flow, cursors, procedures, functions, packages, triggers, and exception handling
7. **Performance**: B-tree and bitmap indexes, EXPLAIN PLAN, optimizer hints, and statistics gathering
8. **Views**: Standard views with CHECK OPTION and materialized views with refresh strategies
9. **Transactions**: COMMIT/ROLLBACK/SAVEPOINT and isolation levels (READ COMMITTED, SERIALIZABLE)
10. **Python**: Connecting with python-oracledb, bind variables, batch operations, and calling PL/SQL

### Next Steps

1. Practice the exercises using Oracle XE on your local machine
2. Explore Oracle's multi-tenant architecture (CDB/PDB) for containerized databases
3. Study Oracle Data Guard for high availability and disaster recovery
4. Learn about partitioning strategies for large tables (range, list, hash)
5. Investigate Oracle APEX for low-code application development on the database

### Additional Resources

- **Oracle Documentation**: <https://docs.oracle.com/en/database/>
- **Oracle Live SQL**: <https://livesql.oracle.com/> (free browser-based SQL environment)
- **Ask TOM**: <https://asktom.oracle.com/> (expert Q&A from Oracle engineers)
- **python-oracledb**: <https://python-oracledb.readthedocs.io/>
- **Oracle XE Downloads**: <https://www.oracle.com/database/technologies/xe-downloads.html>
