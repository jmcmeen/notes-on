# Introduction to PostgreSQL

## Table of Contents

1. [What is PostgreSQL](#what-is-postgresql)
2. [Installation and Setup](#installation-and-setup)
3. [Database Basics](#database-basics)
4. [Data Types](#data-types)
5. [Creating Tables](#creating-tables)
6. [CRUD Operations](#crud-operations)
7. [Querying Data](#querying-data)
8. [Indexes and Performance](#indexes-and-performance)
9. [Views and Functions](#views-and-functions)
10. [Transactions](#transactions)
11. [JSON Support](#json-support)
12. [Python Integration](#python-integration)
13. [Practice Exercises](#practice-exercises)
14. [Summary](#summary)

---

## What is PostgreSQL

### Overview

PostgreSQL is an advanced, open-source relational database management system known for its:
- **ACID compliance**: Guarantees reliable transaction processing
- **Extensibility**: Custom data types, functions, operators, and index methods
- **Standards compliance**: Closely follows the SQL standard
- **Concurrency**: MVCC (Multi-Version Concurrency Control) for high performance
- **JSON support**: First-class support for semi-structured data

### Key Features

- Full-text search built in
- Table inheritance and partitioning
- Window functions and CTEs (Common Table Expressions)
- Foreign data wrappers for querying external sources
- Rich ecosystem of extensions (PostGIS, pg_trgm, hstore)

---

## Installation and Setup

### Installing on Ubuntu/Debian

```sql
-- sudo apt update && sudo apt install postgresql postgresql-contrib
-- sudo systemctl status postgresql   -- verify the service is running
```

### Installing on macOS

```sql
-- brew install postgresql@16
-- brew services start postgresql@16
```

### Initial Configuration

```sql
-- Switch to the postgres system user and open psql
-- sudo -u postgres psql

-- Create a new database user with a password
CREATE USER myuser WITH PASSWORD 'securepassword';
ALTER USER myuser CREATEDB;  -- allow this user to create databases
```

### Connecting to PostgreSQL

```sql
-- psql -U myuser -d mydatabase -h localhost
-- psql "postgresql://myuser:securepassword@localhost:5432/mydatabase"
```

---

## Database Basics

### Creating and Managing Databases

```sql
-- Create a new database
CREATE DATABASE shop;

-- Create a database owned by a specific user
CREATE DATABASE shop OWNER myuser;

-- List all databases (psql command)
-- \l

-- Connect to a database (psql command)
-- \c shop

-- Drop a database (cannot drop while connected to it)
DROP DATABASE IF EXISTS shop;
```

### Essential psql Commands

```sql
-- \l             List all databases        \dt            List tables
-- \c dbname      Connect to a database     \d tablename   Describe a table
-- \dn            List schemas              \df            List functions
-- \di            List indexes              \dv            List views
-- \du            List users/roles          \x             Toggle expanded output
-- \timing        Toggle timing display     \i file.sql    Run a SQL file
-- \q             Quit psql
```

### Schemas

```sql
CREATE SCHEMA inventory;                     -- create a schema to organize tables
CREATE TABLE inventory.products (            -- create a table inside a schema
    id SERIAL PRIMARY KEY, name TEXT NOT NULL
);
SET search_path TO inventory, public;        -- avoid prefixing schema names
```

---

## Data Types

### Common Data Types

```sql
-- Integer types
SMALLINT              -- 2 bytes, -32768 to 32767
INTEGER               -- 4 bytes, standard integer
BIGINT                -- 8 bytes, large integers
SERIAL                -- auto-incrementing 4-byte integer
NUMERIC(10, 2)        -- exact precision, 10 digits total, 2 after decimal
REAL                  -- 4-byte floating point
DOUBLE PRECISION      -- 8-byte floating point

-- Text types
CHAR(10)              -- fixed-length, padded with spaces
VARCHAR(255)          -- variable-length with a limit
TEXT                  -- variable-length, unlimited (preferred in PostgreSQL)

-- Boolean: accepts TRUE, FALSE, NULL (also 't','f','yes','no','1','0')
BOOLEAN

-- Date and time types
DATE                  -- '2026-03-24'
TIME                  -- '14:30:00'
TIMESTAMP             -- '2026-03-24 14:30:00'
TIMESTAMPTZ           -- timestamp with time zone (recommended)
INTERVAL              -- '1 year 2 months 3 days'

-- JSON types
JSON                  -- stores as text, validates on input
JSONB                 -- binary format, faster queries, supports indexing (preferred)

-- Arrays: PostgreSQL supports arrays of any type
INTEGER[]             -- array of integers
TEXT[]                -- array of text values

-- UUID: 128-bit universally unique identifier
UUID                  -- e.g. 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'
-- Enable auto-generation with:
CREATE EXTENSION IF NOT EXISTS "pgcrypto";  -- then use gen_random_uuid()
```

---

## Creating Tables

### Basic Table Creation

```sql
-- Create a simple table with various column types
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,                    -- auto-incrementing primary key
    first_name VARCHAR(100) NOT NULL,         -- required field
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,       -- must be unique and non-null
    department TEXT DEFAULT 'Unassigned',     -- default value if not provided
    salary NUMERIC(10, 2) CHECK (salary > 0), -- check constraint
    hire_date DATE DEFAULT CURRENT_DATE,      -- defaults to today
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()      -- auto-set timestamp
);
```

### Constraints

```sql
-- Primary key constraint (unique + not null)
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_date DATE NOT NULL,
    total NUMERIC(10, 2) NOT NULL
);

-- Composite primary key and unique constraints
CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_id)  -- composite key spans two columns
);
```

### Foreign Keys

```sql
-- Create a parent table
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Create a child table with a foreign key reference
CREATE TABLE staff (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER REFERENCES departments(id)  -- foreign key
        ON DELETE SET NULL    -- set to NULL if the department is deleted
        ON UPDATE CASCADE     -- update if the department id changes
);

-- Other ON DELETE options: CASCADE, RESTRICT, SET DEFAULT
```

### Indexes

```sql
CREATE INDEX idx_employees_email ON employees(email);          -- single column
CREATE INDEX idx_emp_dept ON employees(department, is_active); -- composite
CREATE UNIQUE INDEX idx_emp_email ON employees(email);         -- unique index
CREATE INDEX idx_active_emp ON employees(last_name)            -- partial index
    WHERE is_active = TRUE;
```

### Altering Tables

```sql
ALTER TABLE employees ADD COLUMN phone VARCHAR(20);          -- add a column
ALTER TABLE employees DROP COLUMN phone;                     -- remove a column
ALTER TABLE employees RENAME COLUMN department TO dept;      -- rename a column
ALTER TABLE employees ALTER COLUMN dept TYPE VARCHAR(100);   -- change type
ALTER TABLE employees ADD CONSTRAINT chk_salary CHECK (salary >= 0);
DROP TABLE IF EXISTS employees CASCADE;  -- CASCADE drops dependent objects
```

---

## CRUD Operations

### INSERT - Creating Records

```sql
-- Insert a single row
INSERT INTO employees (first_name, last_name, email, department, salary)
VALUES ('Alice', 'Smith', 'alice@example.com', 'Engineering', 95000.00);

-- Insert multiple rows at once
INSERT INTO employees (first_name, last_name, email, department, salary)
VALUES
    ('Bob', 'Jones', 'bob@example.com', 'Marketing', 72000.00),
    ('Carol', 'White', 'carol@example.com', 'Engineering', 105000.00),
    ('David', 'Brown', 'david@example.com', 'Sales', 68000.00);

-- Insert and return the new row's generated data
INSERT INTO employees (first_name, last_name, email, salary)
VALUES ('Eve', 'Davis', 'eve@example.com', 88000.00)
RETURNING id, first_name, email;
```

### SELECT - Reading Records

```sql
-- Select all columns from a table
SELECT * FROM employees;

-- Select specific columns
SELECT first_name, last_name, salary FROM employees;

-- Aliasing columns for readability
SELECT
    first_name AS "First Name",
    last_name AS "Last Name",
    salary * 12 AS annual_salary  -- computed column
FROM employees;

-- Filtering with WHERE
SELECT * FROM employees
WHERE department = 'Engineering'
  AND salary > 80000;

-- Pattern matching with LIKE and ILIKE
SELECT * FROM employees
WHERE email LIKE '%@example.com'   -- case-sensitive match
   OR last_name ILIKE 'sm%';      -- case-insensitive match

SELECT * FROM employees WHERE department IS NULL;              -- check for NULL
SELECT * FROM employees
WHERE department IN ('Engineering', 'Marketing', 'Sales');     -- match a list
SELECT * FROM employees
WHERE salary BETWEEN 70000 AND 100000;                         -- inclusive range
SELECT DISTINCT department FROM employees;                     -- remove duplicates
```

### UPDATE - Modifying Records

```sql
-- Update a single column for matching rows
UPDATE employees
SET salary = 100000.00
WHERE email = 'alice@example.com';

-- Update multiple columns
UPDATE employees
SET department = 'Senior Engineering',
    salary = salary * 1.10        -- give a 10% raise
WHERE department = 'Engineering'
  AND hire_date < '2024-01-01';

-- Update with RETURNING to see the changed rows
UPDATE employees
SET is_active = FALSE
WHERE last_name = 'Brown'
RETURNING id, first_name, is_active;
```

### DELETE - Removing Records

```sql
-- Delete specific rows
DELETE FROM employees
WHERE is_active = FALSE;

-- Delete and return what was removed
DELETE FROM employees
WHERE id = 5
RETURNING *;

DELETE FROM employees;                                  -- delete all rows
TRUNCATE TABLE employees RESTART IDENTITY CASCADE;      -- faster, resets serials
```

### UPSERT - Insert or Update

```sql
-- Insert or update if a conflict on a unique column occurs
INSERT INTO employees (first_name, last_name, email, salary)
VALUES ('Alice', 'Smith', 'alice@example.com', 98000.00)
ON CONFLICT (email) DO UPDATE SET salary = EXCLUDED.salary;
```

---

## Querying Data

### JOINs

```sql
-- Sample tables for JOIN examples
-- departments(id, name)
-- employees(id, first_name, last_name, department_id)

-- INNER JOIN: returns only rows with matches in both tables
SELECT e.first_name, e.last_name, d.name AS department
FROM employees e
INNER JOIN departments d ON e.department_id = d.id;

-- LEFT JOIN: returns all rows from the left table, NULLs where no match
SELECT e.first_name, d.name AS department
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id;
-- Employees without a department will show NULL for department

-- RIGHT JOIN: returns all rows from the right table
SELECT e.first_name, d.name AS department
FROM employees e
RIGHT JOIN departments d ON e.department_id = d.id;
-- Departments with no employees will show NULL for first_name

-- FULL OUTER JOIN: returns all rows from both tables
SELECT e.first_name, d.name AS department
FROM employees e
FULL OUTER JOIN departments d ON e.department_id = d.id;
-- Shows all employees and all departments, NULLs where no match

-- Self JOIN: joining a table with itself (e.g., employee-manager)
SELECT e.first_name AS employee, m.first_name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

### Aggregation with GROUP BY and HAVING

```sql
-- Count employees per department
SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department;

-- Average salary by department, only showing departments with avg > 80k
SELECT department, AVG(salary)::NUMERIC(10,2) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 80000;  -- HAVING filters groups, WHERE filters rows

-- Multiple aggregates in one query
SELECT department, COUNT(*) AS total, MIN(salary) AS min_sal,
       MAX(salary) AS max_sal, ROUND(AVG(salary), 2) AS avg_sal
FROM employees
GROUP BY department
ORDER BY avg_sal DESC;
```

### ORDER BY and LIMIT

```sql
-- Sort by salary descending, then by last name ascending
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary DESC, last_name ASC;

-- Get the top 5 highest-paid employees
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary DESC
LIMIT 5;

-- Pagination with LIMIT and OFFSET
SELECT * FROM employees
ORDER BY id
LIMIT 10 OFFSET 20;  -- skip 20 rows, return next 10 (page 3)
```

### Subqueries

```sql
-- Subquery in WHERE: find employees earning above average
SELECT first_name, last_name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- EXISTS subquery: find departments that have at least one employee
SELECT d.name FROM departments d
WHERE EXISTS (SELECT 1 FROM employees e WHERE e.department_id = d.id);
```

### Common Table Expressions (CTEs)

```sql
-- CTEs make complex queries more readable by naming subqueries
WITH dept_salaries AS (
    -- First, calculate average salary per department
    SELECT department_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department_id
),
high_paying AS (
    -- Then, filter to departments with high average salaries
    SELECT department_id, avg_salary
    FROM dept_salaries
    WHERE avg_salary > 90000
)
-- Finally, get the department names
SELECT d.name, hp.avg_salary
FROM high_paying hp
JOIN departments d ON hp.department_id = d.id;

-- Recursive CTE: useful for hierarchical data (org charts, categories)
WITH RECURSIVE org_chart AS (
    -- Base case: top-level managers (no manager_id)
    SELECT id, first_name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: employees who report to someone in the previous level
    SELECT e.id, e.first_name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart ORDER BY level, first_name;
```

### Window Functions

```sql
-- ROW_NUMBER: assign a unique number to each row within a partition
SELECT
    first_name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rank_in_dept
FROM employees;

-- Running total with SUM as a window function
SELECT order_date, total,
    SUM(total) OVER (ORDER BY order_date) AS running_total
FROM orders;

-- LAG/LEAD: access previous/next row values
SELECT order_date, total,
    LAG(total) OVER (ORDER BY order_date) AS prev_total,
    LEAD(total) OVER (ORDER BY order_date) AS next_total
FROM orders;
```

---

## Indexes and Performance

### B-tree Indexes (Default)

```sql
-- B-tree is the default, ideal for equality and range queries
CREATE INDEX idx_emp_salary ON employees(salary);

-- Composite B-tree: column order matters (leftmost prefix rule)
CREATE INDEX idx_emp_dept_salary ON employees(department, salary);
-- Helps: WHERE department = 'X' AND salary > 50000
-- Helps: WHERE department = 'X' (uses leftmost prefix)
-- Does NOT help: WHERE salary > 50000 (skips first column)
```

### GIN Indexes

```sql
-- GIN (Generalized Inverted Index): ideal for JSONB, arrays, full-text search
CREATE INDEX idx_data_gin ON products USING GIN (metadata);   -- JSONB
CREATE INDEX idx_tags_gin ON articles USING GIN (tags);       -- arrays
CREATE INDEX idx_fts ON articles USING GIN (to_tsvector('english', body));
```

### EXPLAIN ANALYZE

```sql
-- Show the query plan without executing
EXPLAIN SELECT * FROM employees WHERE department = 'Engineering';

-- Show the query plan AND actual execution statistics
EXPLAIN ANALYZE SELECT * FROM employees WHERE department = 'Engineering';

-- Key terms in output:
-- Seq Scan = full table scan | Index Scan = using an index
-- Hash Join / Nested Loop = join strategies
-- cost = estimated cost | actual time = real execution time (ms)

-- Example: verify an index is being used
EXPLAIN ANALYZE
SELECT * FROM employees
WHERE email = 'alice@example.com';
-- Should show "Index Scan using idx_employees_email"
```

---

## Views and Functions

### Views

```sql
-- A view is a saved query that acts like a virtual table
CREATE VIEW active_employees AS
SELECT id, first_name, last_name, email, department, salary
FROM employees
WHERE is_active = TRUE;

-- Query the view like a regular table
SELECT * FROM active_employees WHERE department = 'Engineering';

-- Create or replace a view
CREATE OR REPLACE VIEW department_summary AS
SELECT department, COUNT(*) AS headcount, ROUND(AVG(salary), 2) AS avg_salary
FROM employees WHERE is_active = TRUE
GROUP BY department;

-- Materialized view: caches results, must be refreshed manually
CREATE MATERIALIZED VIEW monthly_revenue AS
SELECT DATE_TRUNC('month', order_date) AS month, SUM(total) AS revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date);

REFRESH MATERIALIZED VIEW monthly_revenue;  -- refresh when data changes
DROP VIEW IF EXISTS active_employees;       -- drop a view
```

### Stored Functions

```sql
-- Create a function that calculates a bonus based on salary
CREATE OR REPLACE FUNCTION calculate_bonus(emp_salary NUMERIC, performance TEXT)
RETURNS NUMERIC AS $$
BEGIN
    -- Return a bonus percentage based on performance rating
    IF performance = 'excellent' THEN
        RETURN emp_salary * 0.20;
    ELSIF performance = 'good' THEN
        RETURN emp_salary * 0.10;
    ELSE
        RETURN emp_salary * 0.05;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Use the function in a query
SELECT
    first_name,
    salary,
    calculate_bonus(salary, 'excellent') AS bonus
FROM employees;
```

### Triggers

```sql
-- Create a function to be called by a trigger
CREATE OR REPLACE FUNCTION update_modified_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    -- Automatically set the updated_at column on every UPDATE
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach the trigger to a table
CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON employees          -- fires before each row update
    FOR EACH ROW                        -- runs once per affected row
    EXECUTE FUNCTION update_modified_timestamp();
```

---

## Transactions

### Basic Transaction Control

```sql
-- A transaction groups multiple statements into one atomic unit
BEGIN;
    -- Deduct from one account
    UPDATE accounts SET balance = balance - 500 WHERE id = 1;
    -- Credit another account
    UPDATE accounts SET balance = balance + 500 WHERE id = 2;
COMMIT;  -- both updates succeed together, or neither does

-- Roll back a transaction if something goes wrong
BEGIN;
    DELETE FROM employees WHERE department = 'Temp';
    -- Oops, that was wrong! Undo everything since BEGIN
ROLLBACK;

-- Savepoints allow partial rollbacks within a transaction
BEGIN;
    INSERT INTO orders (customer_id, total) VALUES (1, 100.00);
    SAVEPOINT before_items;
    INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 99, 2);
    ROLLBACK TO SAVEPOINT before_items;  -- undo only the item insert
    INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 5, 2);
COMMIT;
```

### Isolation Levels

```sql
-- PostgreSQL supports four isolation levels (default is Read Committed)

-- Read Committed (default): each statement sees only committed data
BEGIN ISOLATION LEVEL READ COMMITTED;
    SELECT * FROM accounts;
COMMIT;

-- Repeatable Read: the entire transaction sees one consistent snapshot
BEGIN ISOLATION LEVEL REPEATABLE READ;
    SELECT balance FROM accounts WHERE id = 1;  -- returns 1000
    -- Re-reading always returns 1000, even if another transaction commits
COMMIT;

-- Serializable: strictest, aborts on conflict to prevent anomalies
BEGIN ISOLATION LEVEL SERIALIZABLE;
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;
```

---

## JSON Support

### Working with JSONB

```sql
-- Create a table with a JSONB column
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb
);

INSERT INTO events (name, metadata) VALUES
('signup', '{"user": "alice", "plan": "pro", "source": "web"}'),
('purchase', '{"user": "bob", "amount": 49.99, "items": ["widget", "gadget"]}');
```

### JSONB Operators

```sql
-- -> returns a JSON element (as JSON)
SELECT metadata -> 'user' FROM events;          -- returns "alice" (with quotes)

-- ->> returns a JSON element as text
SELECT metadata ->> 'user' FROM events;         -- returns alice (no quotes)

-- #> and #>> navigate nested paths (as JSON / as text)
SELECT metadata #>> '{address,city}' FROM events;

-- @> containment: does the left JSONB contain the right?
SELECT * FROM events
WHERE metadata @> '{"user": "alice"}';           -- find Alice's events

-- ? key existence: does the JSONB have this key?
SELECT * FROM events
WHERE metadata ? 'amount';                       -- rows that have an "amount" key

-- Updating a value inside JSONB
UPDATE events
SET metadata = jsonb_set(metadata, '{plan}', '"enterprise"')
WHERE metadata ->> 'user' = 'alice';

-- Removing a key from JSONB
UPDATE events
SET metadata = metadata - 'source'
WHERE id = 1;
```

### Indexing JSONB

```sql
-- GIN index on entire JSONB column (supports @>, ?, ?|, ?& operators)
CREATE INDEX idx_events_metadata ON events USING GIN (metadata);
-- GIN with jsonb_path_ops (smaller index, only supports @>)
CREATE INDEX idx_events_path ON events USING GIN (metadata jsonb_path_ops);
-- B-tree index on a specific key for equality lookups
CREATE INDEX idx_events_user ON events ((metadata ->> 'user'));
```

---

## Python Integration

### Using psycopg2

```python
# Install: pip install psycopg2-binary
import psycopg2

# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="shop",
    user="myuser",
    password="securepassword"
)

# Create a cursor to execute queries
cur = conn.cursor()

# Create a table and commit
cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY, name TEXT NOT NULL, price NUMERIC(10, 2))
""")
conn.commit()

# Insert with parameterized queries (prevents SQL injection)
cur.execute(
    "INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id",
    ("Widget", 29.99)  # never use f-strings or % formatting for SQL values
)
new_id = cur.fetchone()[0]
conn.commit()

# Insert multiple rows
cur.executemany(
    "INSERT INTO products (name, price) VALUES (%s, %s)",
    [("Gadget", 49.99), ("Doohickey", 19.99), ("Thingamajig", 39.99)]
)
conn.commit()

# Query data
cur.execute("SELECT id, name, price FROM products WHERE price > %s", (25.00,))
rows = cur.fetchall()  # returns a list of tuples
for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Price: {row[2]}")

# Always close the connection when done
cur.close()
conn.close()
```

### Connection Pooling

```python
from psycopg2 import pool

# Create a connection pool for better performance in applications
connection_pool = pool.SimpleConnectionPool(
    minconn=1, maxconn=10,  # maintain 1-10 connections
    host="localhost", database="shop",
    user="myuser", password="securepassword"
)

conn = connection_pool.getconn()       # borrow a connection from the pool
cur = conn.cursor()
cur.execute("SELECT * FROM products")
results = cur.fetchall()
cur.close()
connection_pool.putconn(conn)          # return connection to the pool
connection_pool.closeall()             # close all connections on shutdown
```

---

## Practice Exercises

### Exercise 1: Library Database

```sql
-- Create tables and insert sample data
CREATE TABLE authors (id SERIAL PRIMARY KEY, name TEXT NOT NULL, birth_year INT);
CREATE TABLE books (
    id SERIAL PRIMARY KEY, title TEXT NOT NULL,
    author_id INTEGER REFERENCES authors(id),
    published_year INTEGER, genre TEXT, available BOOLEAN DEFAULT TRUE
);

INSERT INTO authors (name, birth_year) VALUES
    ('George Orwell', 1903), ('Jane Austen', 1775), ('Toni Morrison', 1931);
INSERT INTO books (title, author_id, published_year, genre) VALUES
    ('1984', 1, 1949, 'Dystopian'), ('Animal Farm', 1, 1945, 'Satire'),
    ('Pride and Prejudice', 2, 1813, 'Romance'),
    ('Beloved', 3, 1987, 'Historical Fiction');

-- Try these:
-- 1. Find all books published before 1950
-- 2. List books with their author names using a JOIN
-- 3. Count the number of books per author
-- 4. Find authors who have more than one book
-- 5. Find the oldest book in each genre
```

### Exercise 2: E-commerce Analytics

Using the orders/order_items/customers/products schema from the Querying section:

```sql
-- Exercises to try:
-- 1. Calculate total revenue per month using DATE_TRUNC
-- 2. Find the top 3 customers by total spending (JOIN + GROUP BY + LIMIT)
-- 3. Use a CTE to find products that have never been ordered
-- 4. Use a window function to rank products by revenue within each category
-- 5. Write a query with EXPLAIN ANALYZE and add an index to improve it
```

---

## Summary

These notes cover the core concepts of PostgreSQL:

1. **Database Basics**: Creating databases, connecting, and navigating with psql
2. **Data Types**: Numeric, text, boolean, date/time, JSON, arrays, and UUID
3. **Table Design**: CREATE TABLE with constraints, primary/foreign keys, and indexes
4. **CRUD Operations**: INSERT, SELECT, UPDATE, DELETE with RETURNING and UPSERT
5. **Advanced Queries**: JOINs, subqueries, CTEs, window functions, aggregation
6. **Performance**: B-tree and GIN indexes, EXPLAIN ANALYZE for query tuning
7. **Views and Functions**: Virtual tables, stored functions, and triggers
8. **Transactions**: ACID guarantees, savepoints, and isolation levels
9. **JSON Support**: JSONB storage, operators, and indexing strategies
10. **Python Integration**: psycopg2 for connecting, querying, and connection pooling

### Next Steps

1. Practice the exercises and experiment with your own schemas
2. Explore PostgreSQL extensions (PostGIS, pg_trgm, pgcrypto)
3. Learn about table partitioning for large datasets
4. Study connection pooling tools like PgBouncer
5. Set up replication and backups for production use
6. Explore ORMs like SQLAlchemy or Django ORM for application development

### Additional Resources

- **Official Documentation**: https://www.postgresql.org/docs/
- **PostgreSQL Tutorial**: https://www.postgresqltutorial.com/
- **Interactive Practice**: https://pgexercises.com/
- **Books**: "PostgreSQL: Up and Running", "The Art of PostgreSQL"

Remember: The best way to learn PostgreSQL is by building real schemas, writing queries against real data, and using EXPLAIN ANALYZE to understand how the database processes your queries!
