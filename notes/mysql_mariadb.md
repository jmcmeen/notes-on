# Introduction to MySQL and MariaDB

---

## Table of Contents

1. [What Are MySQL and MariaDB](#what-are-mysql-and-mariadb)
2. [Installation and Setup](#installation-and-setup)
3. [Database Basics](#database-basics)
4. [Data Types](#data-types)
5. [Storage Engines](#storage-engines)
6. [Creating Tables](#creating-tables)
7. [CRUD Operations](#crud-operations)
8. [Querying Data](#querying-data)
9. [Stored Procedures and Functions](#stored-procedures-and-functions)
10. [Views](#views)
11. [Transactions](#transactions)
12. [JSON Support](#json-support)
13. [User Management and Security](#user-management-and-security)
14. [Python Integration](#python-integration)
15. [Practice Exercises](#practice-exercises)
16. [Summary](#summary)
17. [Next Steps](#next-steps)
18. [Additional Resources](#additional-resources)

---

## What Are MySQL and MariaDB

MySQL is an open-source RDBMS now owned by Oracle. MariaDB is a community fork
created by the original MySQL founder after Oracle's acquisition. MariaDB maintains
drop-in compatibility: same SQL syntax, client protocols, and wire format.

### Key Differences

| Feature              | MySQL                        | MariaDB                        |
|----------------------|------------------------------|--------------------------------|
| Owner                | Oracle Corporation           | MariaDB Foundation / Corp      |
| License              | GPL + proprietary options    | GPL (fully open source)        |
| Storage Engines      | InnoDB, MyISAM, etc.         | InnoDB, Aria, ColumnStore, etc.|
| JSON Support         | Native JSON type (5.7+)      | JSON as alias for LONGTEXT     |
| CTEs / Window Funcs  | MySQL 8.0+                   | MariaDB 10.2+                  |
| Thread Pool          | Enterprise only              | Built-in                       |
| Replication          | GTID-based                   | GTID-based (different format)  |

### When to Use Which

- **MySQL**: Oracle support contracts, native JSON type, MySQL Shell, Group Replication.
- **MariaDB**: Fully open-source, extra storage engines (Aria, ColumnStore), community-driven.

---

## Installation and Setup

```sql
-- MySQL on Ubuntu/Debian:
-- sudo apt update && sudo apt install mysql-server
-- sudo mysql_secure_installation

-- MariaDB on Ubuntu/Debian:
-- sudo apt update && sudo apt install mariadb-server
-- sudo mysql_secure_installation

-- RHEL/Fedora: replace apt with dnf, package names are mysql-server / mariadb-server

-- Verify installation
-- mysql -u root -p
SELECT VERSION();  -- e.g. 8.0.36 or 10.11.6-MariaDB
```

---

## Database Basics

### The mysql CLI

```sql
-- Connect locally:             mysql -u root -p
-- Connect to remote server:    mysql -h 192.168.1.100 -P 3306 -u appuser -p
-- Run a single command:        mysql -u root -p -e "SHOW DATABASES;"
-- Import a SQL file:           mysql -u root -p mydatabase < backup.sql
```

### Creating and Managing Databases

```sql
-- Show all databases on the server
SHOW DATABASES;

-- Create a new database with a specific character set
CREATE DATABASE shop
    CHARACTER SET utf8mb4          -- supports full Unicode including emojis
    COLLATE utf8mb4_unicode_ci;    -- case-insensitive Unicode collation

-- Switch to the newly created database
USE shop;

-- Show which database is currently selected
SELECT DATABASE();

-- Drop a database (use with caution)
DROP DATABASE IF EXISTS shop;
```

---

## Data Types

### Numeric Types

```sql
-- Integer types (signed ranges shown)
TINYINT          -- -128 to 127                (1 byte)
SMALLINT         -- -32,768 to 32,767          (2 bytes)
MEDIUMINT        -- -8,388,608 to 8,388,607    (3 bytes)
INT              -- -2,147,483,648 to 2.1B     (4 bytes)
BIGINT           -- -9.2 quintillion to 9.2Q   (8 bytes)

-- Fixed-point decimal (exact precision for money, etc.)
DECIMAL(10, 2)   -- 10 total digits, 2 after decimal point

-- Floating-point (approximate, faster math)
FLOAT            -- 4 bytes, ~7 decimal digits precision
DOUBLE           -- 8 bytes, ~15 decimal digits precision
```

### String Types

```sql
CHAR(50)         -- fixed-length string, always uses 50 bytes
VARCHAR(255)     -- variable-length string, up to 255 characters
TEXT             -- variable-length, up to 65,535 characters
MEDIUMTEXT       -- up to 16,777,215 characters
LONGTEXT         -- up to 4,294,967,295 characters
ENUM('a','b')    -- one value from a predefined list
SET('x','y','z') -- zero or more values from a predefined list
```

### Date and Time Types

```sql
DATE             -- 'YYYY-MM-DD'                     (3 bytes)
TIME             -- 'HH:MM:SS'                       (3 bytes)
DATETIME         -- 'YYYY-MM-DD HH:MM:SS'            (8 bytes, no timezone)
TIMESTAMP        -- like DATETIME but stored as UTC   (4 bytes, auto-converts)
YEAR             -- 'YYYY'                            (1 byte)
```

### Other Types

```sql
BOOLEAN          -- alias for TINYINT(1), stores 0 or 1
JSON             -- native JSON document type in MySQL 5.7+
                 -- alias for LONGTEXT in MariaDB (with JSON validation in 10.2+)
BLOB             -- binary large object, up to 65,535 bytes
BINARY(16)       -- fixed-length binary, useful for UUIDs
```

---

## Storage Engines

### InnoDB vs MyISAM

```sql
-- Check available storage engines
SHOW ENGINES;

-- InnoDB (default since MySQL 5.5 / MariaDB 10.2)
-- + ACID-compliant transactions
-- + Row-level locking (better concurrency)
-- + Foreign key constraints
-- + Crash recovery via redo log
-- - Slightly more disk space overhead

-- MyISAM (legacy default)
-- + Faster for read-heavy, rarely-updated tables
-- + Full-text indexing (before InnoDB supported it)
-- - Table-level locking (poor concurrency for writes)
-- - No transaction support
-- - No foreign key support
-- - Prone to corruption on crashes

-- Specify engine when creating a table
CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT
) ENGINE=InnoDB;                   -- explicitly set InnoDB

-- MariaDB also offers:
-- Aria       : crash-safe replacement for MyISAM
-- ColumnStore: columnar engine for analytics / OLAP workloads
-- MEMORY     : in-memory tables, data lost on restart
```

---

## Creating Tables

### Basic Table Creation

```sql
CREATE TABLE customers (
    customer_id   INT AUTO_INCREMENT PRIMARY KEY,  -- auto-incrementing PK
    first_name    VARCHAR(100) NOT NULL,            -- required field
    last_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(255) NOT NULL UNIQUE,     -- unique constraint
    phone         VARCHAR(20),                      -- nullable by default
    is_active     BOOLEAN DEFAULT TRUE,             -- default value
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;
```

### Constraints and Foreign Keys

```sql
CREATE TABLE orders (
    order_id      INT AUTO_INCREMENT PRIMARY KEY,
    customer_id   INT NOT NULL,
    order_date    DATETIME DEFAULT CURRENT_TIMESTAMP,
    status        ENUM('pending', 'shipped', 'delivered', 'cancelled')
                      DEFAULT 'pending',
    total_amount  DECIMAL(10, 2) NOT NULL CHECK (total_amount >= 0),

    -- Foreign key linking orders to customers
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE RESTRICT              -- prevent deleting a customer with orders
        ON UPDATE CASCADE               -- update FK if customer PK changes
) ENGINE=InnoDB;

CREATE TABLE order_items (
    item_id       INT AUTO_INCREMENT PRIMARY KEY,
    order_id      INT NOT NULL,
    product_name  VARCHAR(255) NOT NULL,
    quantity      INT NOT NULL DEFAULT 1,
    unit_price    DECIMAL(10, 2) NOT NULL,

    CONSTRAINT fk_items_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE               -- delete items when order is deleted
) ENGINE=InnoDB;
```

### Indexes

```sql
-- Single-column index for faster lookups on last_name
CREATE INDEX idx_customers_last_name
    ON customers(last_name);

-- Composite index (leftmost prefix rule applies)
CREATE INDEX idx_orders_customer_date
    ON orders(customer_id, order_date);

-- Full-text index for search (InnoDB supports this in MySQL 5.6+)
ALTER TABLE order_items
    ADD FULLTEXT INDEX ft_product_name (product_name);

-- Show indexes on a table
SHOW INDEX FROM customers;
```

### Altering Tables

```sql
ALTER TABLE customers ADD COLUMN loyalty_points INT DEFAULT 0 AFTER is_active;
ALTER TABLE customers MODIFY COLUMN phone VARCHAR(30);
ALTER TABLE customers RENAME COLUMN phone TO phone_number;  -- MySQL 8+ / MariaDB 10.5+
ALTER TABLE customers DROP COLUMN loyalty_points;
```

---

## CRUD Operations

### INSERT (Create)

```sql
-- Insert a single row
INSERT INTO customers (first_name, last_name, email)
VALUES ('Alice', 'Johnson', 'alice@example.com');

-- Insert multiple rows in one statement (more efficient)
INSERT INTO customers (first_name, last_name, email) VALUES
    ('Bob',   'Smith',   'bob@example.com'),
    ('Carol', 'Davis',   'carol@example.com'),
    ('Dave',  'Wilson',  'dave@example.com');

-- Insert or update if a unique key conflict occurs
INSERT INTO customers (first_name, last_name, email)
VALUES ('Alice', 'Johnson', 'alice@example.com')
ON DUPLICATE KEY UPDATE
    first_name = VALUES(first_name),  -- update existing row instead of failing
    last_name  = VALUES(last_name);
```

### SELECT (Read)

```sql
-- Select all columns
SELECT * FROM customers;

-- Select specific columns with aliases
SELECT
    customer_id AS id,
    CONCAT(first_name, ' ', last_name) AS full_name,  -- concatenate strings
    email
FROM customers
WHERE is_active = TRUE
ORDER BY last_name ASC, first_name ASC;

-- Pattern matching with LIKE
SELECT * FROM customers
WHERE email LIKE '%@example.com';      -- % matches any sequence of characters

-- IN clause for matching against a list
SELECT * FROM orders
WHERE status IN ('pending', 'shipped');
```

### UPDATE

```sql
-- Update a single row
UPDATE customers
SET email = 'alice.j@example.com'
WHERE customer_id = 1;                 -- always use WHERE to avoid updating all rows

-- Update multiple columns
UPDATE orders
SET status = 'shipped',
    updated_at = NOW()                 -- not present on orders, but illustrative
WHERE order_id = 42;

-- Conditional update
UPDATE orders
SET status = CASE
    WHEN DATEDIFF(NOW(), order_date) > 30 THEN 'cancelled'
    WHEN DATEDIFF(NOW(), order_date) > 7  THEN 'shipped'
    ELSE status END
WHERE status = 'pending';
```

### DELETE

```sql
-- Delete a specific row
DELETE FROM customers
WHERE customer_id = 4;

-- Delete with a subquery
DELETE FROM order_items
WHERE order_id IN (
    SELECT order_id FROM orders WHERE status = 'cancelled'
);

-- Truncate removes all rows quickly (resets AUTO_INCREMENT)
TRUNCATE TABLE order_items;
```

---

## Querying Data

### JOINs

```sql
-- INNER JOIN: only rows with matches in both tables
SELECT
    o.order_id,
    c.first_name,
    c.last_name,
    o.total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;

-- LEFT JOIN: all rows from the left table, NULLs where no match
SELECT
    c.first_name,
    c.last_name,
    COUNT(o.order_id) AS order_count   -- 0 for customers with no orders
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name;

```

### GROUP BY and HAVING

```sql
-- Aggregate with GROUP BY
SELECT
    status,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value
FROM orders
GROUP BY status;

-- HAVING filters groups (WHERE filters rows before grouping)
SELECT
    customer_id,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_spent
FROM orders
GROUP BY customer_id
HAVING total_spent > 500               -- only customers who spent over 500
ORDER BY total_spent DESC;
```

### Subqueries

```sql
-- Scalar subquery in WHERE
SELECT * FROM customers
WHERE customer_id = (
    SELECT customer_id FROM orders
    ORDER BY total_amount DESC
    LIMIT 1                            -- customer with the single largest order
);

-- Subquery with IN
SELECT * FROM customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id FROM orders
    WHERE order_date >= '2025-01-01'
);

-- Correlated subquery (references outer query)
SELECT
    c.first_name,
    c.last_name,
    (SELECT COUNT(*) FROM orders o
     WHERE o.customer_id = c.customer_id) AS num_orders
FROM customers c;
```

### Common Table Expressions (CTEs) -- MySQL 8.0+ / MariaDB 10.2+

```sql
-- CTE for readability and reuse within a single query
WITH customer_totals AS (
    SELECT
        customer_id,
        SUM(total_amount) AS lifetime_value
    FROM orders
    GROUP BY customer_id
)
SELECT
    c.first_name,
    c.last_name,
    ct.lifetime_value
FROM customers c
JOIN customer_totals ct ON c.customer_id = ct.customer_id
WHERE ct.lifetime_value > 1000
ORDER BY ct.lifetime_value DESC;

-- Recursive CTE (hierarchical data like categories)
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 0 AS depth   -- anchor: top-level
    FROM categories WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.name, c.parent_id, ct.depth + 1  -- recursive step
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY depth, name;
```

### Window Functions -- MySQL 8.0+ / MariaDB 10.2+

```sql
-- ROW_NUMBER, RANK, and DENSE_RANK
SELECT
    customer_id,
    order_id,
    total_amount,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id       -- reset numbering per customer
        ORDER BY total_amount DESC     -- largest orders first
    ) AS order_rank
FROM orders;

-- Running total with SUM window function
SELECT
    order_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER (
        ORDER BY order_date            -- cumulative sum ordered by date
        ROWS UNBOUNDED PRECEDING
    ) AS running_total
FROM orders;

-- LAG / LEAD to compare with previous / next rows
SELECT
    order_id,
    order_date,
    total_amount,
    LAG(total_amount) OVER (ORDER BY order_date) AS prev_amount,
    total_amount - LAG(total_amount) OVER (ORDER BY order_date) AS diff
FROM orders;
```

### LIMIT and OFFSET

```sql
-- Pagination: page 1
SELECT * FROM customers ORDER BY customer_id LIMIT 10 OFFSET 0;

-- Page 3 (rows 21-30)
SELECT * FROM customers ORDER BY customer_id LIMIT 10 OFFSET 20;
```

---

## Stored Procedures and Functions

### Stored Procedures

```sql
-- Create a procedure that retrieves orders for a given customer
DELIMITER //
CREATE PROCEDURE GetCustomerOrders(IN cust_id INT)
BEGIN
    SELECT
        o.order_id,
        o.order_date,
        o.status,
        o.total_amount
    FROM orders o
    WHERE o.customer_id = cust_id      -- use the input parameter
    ORDER BY o.order_date DESC;
END //
DELIMITER ;

-- Call the procedure
CALL GetCustomerOrders(1);

-- Procedure with OUT parameter
DELIMITER //
CREATE PROCEDURE CountCustomerOrders(IN cust_id INT, OUT order_count INT)
BEGIN
    SELECT COUNT(*) INTO order_count FROM orders WHERE customer_id = cust_id;
END //
DELIMITER ;

CALL CountCustomerOrders(1, @cnt);
SELECT @cnt AS total_orders;

DROP PROCEDURE IF EXISTS GetCustomerOrders;
```

### Stored Functions

```sql
-- Create a function that calculates order total from items
DELIMITER //
CREATE FUNCTION CalcOrderTotal(ord_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC                          -- same input always gives same output
READS SQL DATA
BEGIN
    DECLARE total DECIMAL(10,2);
    SELECT SUM(quantity * unit_price) INTO total
    FROM order_items
    WHERE order_id = ord_id;
    RETURN IFNULL(total, 0.00);        -- return 0 if no items found
END //
DELIMITER ;

-- Use the function in a query
SELECT order_id, CalcOrderTotal(order_id) AS computed_total
FROM orders;
```

---

## Views

```sql
-- Create a view to simplify a common join
CREATE OR REPLACE VIEW vw_order_summary AS
SELECT o.order_id, c.first_name, c.last_name, c.email,
       o.order_date, o.status, o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;

-- Query the view like a regular table
SELECT * FROM vw_order_summary WHERE status = 'pending';

-- Views are updatable if they map to a single base table without
-- aggregates, DISTINCT, GROUP BY, UNION, or subqueries

DROP VIEW IF EXISTS vw_order_summary;
```

---

## Transactions

### Basic Transaction Flow

```sql
-- Start a transaction explicitly
START TRANSACTION;

-- Perform multiple related operations
INSERT INTO orders (customer_id, total_amount)
VALUES (1, 150.00);

SET @new_order_id = LAST_INSERT_ID();  -- capture the auto-generated ID

INSERT INTO order_items (order_id, product_name, quantity, unit_price)
VALUES (@new_order_id, 'Widget', 3, 50.00);

-- If everything succeeded, make it permanent
COMMIT;

-- If something went wrong, undo all changes since START TRANSACTION
-- ROLLBACK;
```

### Savepoints

```sql
START TRANSACTION;

INSERT INTO customers (first_name, last_name, email)
VALUES ('Eve', 'Taylor', 'eve@example.com');

SAVEPOINT after_customer;              -- mark a point to roll back to

INSERT INTO orders (customer_id, total_amount)
VALUES (LAST_INSERT_ID(), 99.99);

-- Oops, roll back only the order, keep the customer
ROLLBACK TO SAVEPOINT after_customer;

COMMIT;                                -- commits the customer insert only
```

### InnoDB Locking

```sql
-- Shared lock: other transactions can read but not write
SELECT * FROM customers
WHERE customer_id = 1
LOCK IN SHARE MODE;                    -- or FOR SHARE in MySQL 8.0+

-- Exclusive lock: other transactions can neither read nor write
SELECT * FROM customers
WHERE customer_id = 1
FOR UPDATE;                            -- acquires exclusive row lock

-- InnoDB auto-detects deadlocks and rolls back the cheaper transaction.
-- Handle error code 1213 in application code and retry.

-- Set transaction isolation level
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- Options: READ UNCOMMITTED, READ COMMITTED,
--          REPEATABLE READ (default), SERIALIZABLE
```

---

## JSON Support

```sql
-- Create a table with a JSON column
CREATE TABLE products (
    product_id   INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(255) NOT NULL,
    attributes   JSON                          -- flexible schema per product
);

-- Insert JSON data
INSERT INTO products (name, attributes) VALUES
('Laptop', '{"brand": "Acme", "ram_gb": 16, "tags": ["electronics", "portable"]}'),
('Desk',   '{"brand": "OakCo", "material": "wood", "tags": ["furniture"]}');

-- Extract a value with -> (returns JSON) or ->> (returns text)
SELECT
    name,
    attributes->>'$.brand' AS brand,           -- ->> extracts as unquoted string
    attributes->'$.ram_gb' AS ram              -- -> keeps JSON type
FROM products;

-- Search inside JSON
SELECT * FROM products
WHERE JSON_CONTAINS(attributes->'$.tags', '"electronics"');

-- Modify JSON in place
UPDATE products
SET attributes = JSON_SET(attributes, '$.ram_gb', 32)  -- update existing key
WHERE product_id = 1;

-- Add a new key
UPDATE products
SET attributes = JSON_INSERT(attributes, '$.weight_kg', 1.8)
WHERE product_id = 1;

-- Remove a key
UPDATE products
SET attributes = JSON_REMOVE(attributes, '$.material')
WHERE product_id = 2;

-- Aggregate: build a JSON array from query results (MySQL 8+)
SELECT JSON_ARRAYAGG(name) AS all_names FROM products;
```

---

## User Management and Security

### Creating and Managing Users

```sql
-- Create a new user (specify host for network security)
CREATE USER 'appuser'@'localhost'
    IDENTIFIED BY 'Strong_P@ssw0rd!';          -- always use strong passwords

-- Create a user that can connect from any host
CREATE USER 'remote_user'@'%' IDENTIFIED BY 'An0therStr0ng!';

-- Change a user's password
ALTER USER 'appuser'@'localhost'
    IDENTIFIED BY 'New_Str0ng_P@ss!';

-- Drop a user
DROP USER IF EXISTS 'remote_user'@'%';
```

### Granting and Revoking Privileges

```sql
-- Grant all privileges on a specific database
GRANT ALL PRIVILEGES ON shop.*
    TO 'appuser'@'localhost';

-- Grant only SELECT and INSERT on specific tables
GRANT SELECT, INSERT ON shop.customers
    TO 'appuser'@'localhost';

-- Apply privilege changes and view grants
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'appuser'@'localhost';

-- Revoke specific privileges
REVOKE INSERT ON shop.customers
    FROM 'appuser'@'localhost';

-- Revoke all privileges
REVOKE ALL PRIVILEGES, GRANT OPTION
    FROM 'appuser'@'localhost';
```

### Security Best Practices

```sql
-- 1. Always run mysql_secure_installation after install
-- 2. Remove anonymous users:  DELETE FROM mysql.user WHERE User = '';
-- 3. Disable remote root:     DELETE FROM mysql.user WHERE User='root' AND Host!='localhost';
-- 4. Require SSL in production: GRANT ALL ON shop.* TO 'appuser'@'%' REQUIRE SSL;
-- 5. Audit accounts regularly:
SELECT User, Host FROM mysql.user;
FLUSH PRIVILEGES;
```

---

## Python Integration

### Using mysql-connector-python

```python
# Install: pip install mysql-connector-python
import mysql.connector

# Establish a connection
conn = mysql.connector.connect(
    host="localhost",
    user="appuser",
    password="Strong_P@ssw0rd!",
    database="shop"
)
cursor = conn.cursor(dictionary=True)     # return rows as dicts

# Parameterized query (prevents SQL injection)
customer_id = 1
cursor.execute(
    "SELECT * FROM customers WHERE customer_id = %s",
    (customer_id,)                         # always use tuple for params
)
row = cursor.fetchone()
print(row)                                 # {'customer_id': 1, 'first_name': 'Alice', ...}

# Insert with commit
cursor.execute(
    "INSERT INTO customers (first_name, last_name, email) VALUES (%s, %s, %s)",
    ("Frank", "Miller", "frank@example.com")
)
conn.commit()                              # must commit for InnoDB writes
print(f"Inserted row ID: {cursor.lastrowid}")

# Fetch multiple rows
cursor.execute("SELECT first_name, email FROM customers ORDER BY first_name")
for row in cursor.fetchall():
    print(row["first_name"], row["email"])

# Always clean up
cursor.close()
conn.close()
```

### Using PyMySQL

```python
# Install: pip install pymysql
import pymysql

# PyMySQL follows the same DB-API 2.0 interface as mysql-connector-python
conn = pymysql.connect(
    host="localhost", user="appuser",
    password="Strong_P@ssw0rd!", database="shop",
    cursorclass=pymysql.cursors.DictCursor
)
try:
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS cnt FROM orders")
        print(f"Total orders: {cursor.fetchone()['cnt']}")
    conn.commit()
except pymysql.MySQLError as e:
    conn.rollback()
    print(f"Database error: {e}")
finally:
    conn.close()
```

---

## Practice Exercises

1. **Database Setup**: Create a `library` database with `books`, `authors`, and
   `borrowers` tables. Define primary keys, foreign keys, and indexes.
2. **CRUD Practice**: Insert five books and three authors. Update a title, delete
   a borrower, and SELECT all books by a specific author using a JOIN.
3. **Aggregation**: Show how many books each author has, including those with
   zero books (LEFT JOIN + GROUP BY).
4. **CTE + Window Function**: Rank books by publication year within each genre
   using a CTE and ROW_NUMBER().
5. **Stored Procedure**: Write `CheckOutBook(borrower_id, book_id)` that inserts
   into `checkouts` and decrements `available_copies` inside a transaction.
6. **JSON Column**: Add a `metadata` JSON column to `books`, store page count /
   ISBN / keywords, and query for books where keywords contains "science".
7. **User Security**: Create a `librarian` (SELECT/INSERT/UPDATE) and a `patron`
   (SELECT only) user. Verify with SHOW GRANTS.
8. **Python Script**: Connect to `library` with mysql-connector-python, insert a
   book, and retrieve all books ordered by publication year.

---

## Summary

- **MySQL and MariaDB** are closely related; MariaDB is a compatible community fork.
- **InnoDB** is the default engine, providing transactions, row-level locking, and
  foreign key support.
- **Data types**: use INT for IDs, VARCHAR for text, DECIMAL for money, DATETIME for
  timestamps, JSON for semi-structured data.
- **CRUD** (INSERT, SELECT, UPDATE, DELETE) is the foundation of data manipulation.
- **JOINs, CTEs, and window functions** (MySQL 8+ / MariaDB 10.2+) enable expressive queries.
- **Transactions** ensure atomicity -- all operations succeed or none do.
- **User management** with CREATE USER, GRANT, REVOKE enforces least privilege.
- **Python**: mysql-connector-python and PyMySQL offer DB-API 2.0 access; always use
  parameterized queries to prevent SQL injection.

---

## Next Steps

- **Replication**: Primary-replica replication for high availability.
- **Performance Tuning**: EXPLAIN plans, query optimization, covering indexes.
- **Backup and Recovery**: mysqldump, mysqlpump, point-in-time recovery with binlogs.
- **ORMs**: SQLAlchemy or Django ORM for Python applications.
- **Partitioning**: RANGE, LIST, HASH partitioning for very large tables.
- **Docker**: Run in containers for dev/test environments.

---

## Additional Resources

- [MySQL Official Documentation](https://dev.mysql.com/doc/)
- [MariaDB Knowledge Base](https://mariadb.com/kb/en/)
- [MySQL Tutorial (mysqltutorial.org)](https://www.mysqltutorial.org/)
- [MariaDB Tutorial (mariadbtutorial.com)](https://www.mariadbtutorial.com/)
- [Use The Index, Luke (indexing guide)](https://use-the-index-luke.com/)
- [High Performance MySQL (O'Reilly book)](https://www.oreilly.com/library/view/high-performance-mysql/9781492080503/)
- [Planet MySQL (community blog aggregator)](https://planet.mysql.com/)
