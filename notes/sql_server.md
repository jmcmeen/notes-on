# Introduction to SQL Server

## Table of Contents

1. [What is SQL Server](#what-is-sql-server)
2. [Installation and Setup](#installation-and-setup)
3. [Database Basics](#database-basics)
4. [Data Types](#data-types)
5. [Creating Tables](#creating-tables)
6. [CRUD Operations](#crud-operations)
7. [Querying Data](#querying-data)
8. [T-SQL Programming Features](#t-sql-programming-features)
9. [Indexes and Performance](#indexes-and-performance)
10. [Views and Temp Tables](#views-and-temp-tables)
11. [Transactions and Isolation Levels](#transactions-and-isolation-levels)
12. [Python Integration with pyodbc](#python-integration-with-pyodbc)
13. [Practice Exercises](#practice-exercises)
14. [Summary](#summary)

---

## What is SQL Server

### Overview

Microsoft SQL Server is a relational database management system (RDBMS) developed by Microsoft. It uses T-SQL (Transact-SQL), Microsoft's extension of the SQL standard, and is widely used in enterprise environments.

Key characteristics:

- **Relational**: Data is organized into tables with rows and columns
- **ACID-compliant**: Guarantees data integrity through transactions
- **Scalable**: Handles workloads from small apps to enterprise data warehouses
- **Integrated**: Works seamlessly with the Microsoft ecosystem (.NET, Azure, Power BI)
- **Secure**: Row-level security, Always Encrypted, auditing features

### Editions

| Edition | Use Case |
| ------- | -------- |
| **Express** | Free, limited to 10 GB per database, good for learning and small apps |
| **Developer** | Free, full-featured, licensed for development and testing only |
| **Standard** | Production workloads with moderate performance requirements |
| **Enterprise** | Mission-critical workloads, all features unlocked |
| **Azure SQL** | Cloud-hosted, fully managed database-as-a-service |

---

## Installation and Setup

1. Download **SQL Server Developer Edition** from Microsoft's website
2. Run the installer and choose **Basic** or **Custom** installation
3. Install **SQL Server Management Studio (SSMS)** separately

In SSMS, connect using:

- **Server name**: `localhost` or `.\SQLEXPRESS` for Express edition
- **Authentication**: Windows Authentication (default) or SQL Server Authentication

### Connecting via sqlcmd

```sql
-- From terminal: sqlcmd -S localhost -E (the -E flag uses Windows Authentication)
-- Once connected, run queries followed by GO
SELECT @@VERSION;
GO
```

---

## Database Basics

### Creating and Using Databases

```sql
-- Create a new database
CREATE DATABASE CompanyDB;
GO

-- Switch to the new database
USE CompanyDB;
GO

-- View all databases on the server
SELECT name, create_date FROM sys.databases ORDER BY name;
GO

-- Drop a database (careful -- this is irreversible)
-- DROP DATABASE CompanyDB;
```

### SSMS Overview

SQL Server Management Studio (SSMS) provides:

- **Object Explorer**: Browse servers, databases, tables, views, and stored procedures
- **Query Editor**: Write and execute T-SQL with IntelliSense
- **Execution Plans**: Visual display of how queries are processed
- **Activity Monitor**: Real-time server performance metrics
- **Import/Export Wizard**: Move data between sources

---

## Data Types

### Commonly Used Data Types

```sql
-- Numeric types
DECLARE @wholeNumber INT;              -- Integer: -2^31 to 2^31-1
DECLARE @bigNum BIGINT;                -- Large range: -2^63 to 2^63-1
DECLARE @price DECIMAL(10, 2);         -- Exact numeric: 10 digits, 2 after decimal
DECLARE @rate FLOAT;                   -- Approximate numeric (8-byte floating point)

-- String types
DECLARE @name VARCHAR(100);            -- Variable-length ASCII string (up to 100 chars)
DECLARE @unicodeName NVARCHAR(100);    -- Variable-length Unicode (supports international chars)
DECLARE @fixedCode CHAR(5);            -- Fixed-length ASCII string (always 5 chars, padded)

-- Date and time types
DECLARE @createdAt DATETIME2(7);       -- Date and time with fractional seconds precision
DECLARE @today DATE;                   -- Date only (no time component)
DECLARE @legacy DATETIME;              -- Older type, less precision than DATETIME2

-- Other types
DECLARE @isActive BIT;                 -- Boolean: 0 (false), 1 (true), or NULL
DECLARE @rowId UNIQUEIDENTIFIER;       -- 16-byte GUID (globally unique identifier)
DECLARE @notes NVARCHAR(MAX);          -- Large Unicode text field (up to 2 GB)

-- Assigning values
SET @wholeNumber = 42;
SET @price = 19.99;
SET @name = 'SQL Server';
SET @unicodeName = N'日本語テキスト';   -- N prefix required for Unicode literals
SET @isActive = 1;
SET @rowId = NEWID();                  -- Generate a new GUID
SET @createdAt = SYSDATETIME();        -- Current date and time with high precision
```

---

## Creating Tables

### Basic Table Creation

```sql
USE CompanyDB;
GO

-- Create a table with various constraints
CREATE TABLE Employees (
    EmployeeID INT IDENTITY(1,1) PRIMARY KEY,  -- Auto-incrementing primary key
    FirstName NVARCHAR(50) NOT NULL,            -- Required field, Unicode
    LastName NVARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,         -- Must be unique and not null
    HireDate DATE NOT NULL DEFAULT GETDATE(),   -- Defaults to current date
    Salary DECIMAL(10,2) CHECK (Salary > 0),   -- Must be positive
    DepartmentID INT NULL,                      -- Nullable foreign key column
    IsActive BIT NOT NULL DEFAULT 1,            -- Defaults to true
    RowGuid UNIQUEIDENTIFIER DEFAULT NEWID(),   -- Auto-generated GUID
    CreatedAt DATETIME2 DEFAULT SYSDATETIME()   -- Timestamp with high precision
);
GO

-- Create a related table
CREATE TABLE Departments (
    DepartmentID INT IDENTITY(1,1) PRIMARY KEY,
    DepartmentName NVARCHAR(100) NOT NULL UNIQUE,
    Budget DECIMAL(15,2) DEFAULT 0,
    ManagerID INT NULL
);
GO

-- Add a foreign key constraint after table creation
ALTER TABLE Employees
ADD CONSTRAINT FK_Employees_Departments
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID);
GO
```

### Composite Keys and Additional Constraints

```sql
-- Table with composite primary key
CREATE TABLE ProjectAssignments (
    EmployeeID INT NOT NULL,
    ProjectID INT NOT NULL,
    AssignedDate DATE NOT NULL DEFAULT GETDATE(),
    HoursAllocated DECIMAL(5,2) DEFAULT 0,
    CONSTRAINT PK_ProjectAssignments PRIMARY KEY (EmployeeID, ProjectID),  -- Composite key
    CONSTRAINT FK_PA_Employee FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID),
    CONSTRAINT CK_Hours CHECK (HoursAllocated >= 0 AND HoursAllocated <= 168)  -- Max hours/week
);
GO

-- Modify an existing table
ALTER TABLE Employees ADD PhoneNumber VARCHAR(20) NULL;           -- Add a column
ALTER TABLE Employees ALTER COLUMN PhoneNumber VARCHAR(25) NULL;  -- Change column size
```

---

## CRUD Operations

```sql
-- INSERT: Single row
INSERT INTO Departments (DepartmentName, Budget)
VALUES ('Engineering', 500000.00);

-- INSERT: Multiple rows at once
INSERT INTO Employees (FirstName, LastName, Email, Salary, DepartmentID)
VALUES ('Alice', 'Johnson', 'alice.j@company.com', 85000.00, 1),
       ('Bob', 'Smith', 'bob.s@company.com', 72000.00, 1),
       ('Carol', 'Williams', 'carol.w@company.com', 91000.00, 2);

-- SELECT: Filtering, aliases, and calculated columns
SELECT
    FirstName + ' ' + LastName AS FullName,   -- Concatenate with alias
    Salary / 12 AS MonthlySalary,             -- Calculated column
    DATEDIFF(YEAR, HireDate, GETDATE()) AS YearsEmployed
FROM Employees
WHERE DepartmentID = 1 AND Salary > 70000     -- Filter conditions
ORDER BY Salary DESC;                          -- Sort descending

-- UPDATE: Single row and bulk update
UPDATE Employees SET Salary = 90000.00 WHERE EmployeeID = 1;

UPDATE Employees
SET Salary = Salary * 1.10             -- 10% raise for department
WHERE DepartmentID = 1;

-- DELETE: Remove specific rows
DELETE FROM Employees WHERE EmployeeID = 5;
DELETE FROM Employees WHERE IsActive = 0 AND HireDate < '2020-01-01';

-- TRUNCATE: Remove all rows (faster than DELETE, resets identity)
-- TRUNCATE TABLE StagingData;
```

---

## Querying Data

### JOINs

```sql
-- INNER JOIN: Only matching rows from both tables
SELECT e.FirstName, e.LastName, d.DepartmentName, e.Salary
FROM Employees e
INNER JOIN Departments d ON e.DepartmentID = d.DepartmentID;

-- LEFT JOIN: All rows from left table, matching from right (shows depts with no employees)
SELECT d.DepartmentName, e.FirstName, e.LastName
FROM Departments d
LEFT JOIN Employees e ON d.DepartmentID = e.DepartmentID;

-- Multiple JOINs in one query
SELECT e.FirstName + ' ' + e.LastName AS EmployeeName, d.DepartmentName, pa.HoursAllocated
FROM Employees e
INNER JOIN Departments d ON e.DepartmentID = d.DepartmentID
LEFT JOIN ProjectAssignments pa ON e.EmployeeID = pa.EmployeeID;
```

### Subqueries

```sql
-- Subquery in WHERE clause
SELECT FirstName, LastName, Salary
FROM Employees
WHERE Salary > (
    SELECT AVG(Salary) FROM Employees  -- Employees earning above average
);

-- EXISTS subquery
SELECT d.DepartmentName
FROM Departments d
WHERE EXISTS (                          -- Departments that have at least one employee
    SELECT 1 FROM Employees e
    WHERE e.DepartmentID = d.DepartmentID
);
```

### Common Table Expressions (CTEs)

```sql
-- Basic CTE: Define a named result set used by the following SELECT
WITH HighEarners AS (
    SELECT FirstName, LastName, Salary, DepartmentID
    FROM Employees
    WHERE Salary > 80000
)
SELECT he.FirstName, he.LastName, he.Salary, d.DepartmentName
FROM HighEarners he
INNER JOIN Departments d ON he.DepartmentID = d.DepartmentID;

-- Multiple CTEs chained together
WITH DeptSalaries AS (
    SELECT DepartmentID, AVG(Salary) AS AvgSalary, COUNT(*) AS EmpCount
    FROM Employees
    GROUP BY DepartmentID
),
TopDepts AS (
    SELECT DepartmentID, AvgSalary, EmpCount
    FROM DeptSalaries
    WHERE AvgSalary > 70000
)
SELECT d.DepartmentName, td.AvgSalary, td.EmpCount
FROM TopDepts td
INNER JOIN Departments d ON td.DepartmentID = d.DepartmentID;
```

### Window Functions

```sql
-- ROW_NUMBER with PARTITION BY: Rank resets per group
SELECT FirstName, LastName, Salary, DepartmentID,
    ROW_NUMBER() OVER (PARTITION BY DepartmentID ORDER BY Salary DESC) AS DeptRank
FROM Employees;

-- RANK and DENSE_RANK: Handle ties differently
SELECT FirstName, Salary,
    RANK() OVER (ORDER BY Salary DESC) AS RankNum,            -- Skips numbers after ties
    DENSE_RANK() OVER (ORDER BY Salary DESC) AS DenseRankNum  -- No gaps after ties
FROM Employees;

-- LAG and LEAD: Access previous/next row values
SELECT FirstName, HireDate, Salary,
    LAG(Salary) OVER (ORDER BY HireDate) AS PrevEmpSalary,   -- Previous row's salary
    LEAD(Salary) OVER (ORDER BY HireDate) AS NextEmpSalary   -- Next row's salary
FROM Employees;
```

### GROUP BY and Aggregations

```sql
-- Aggregation with GROUP BY and HAVING
SELECT d.DepartmentName,
    COUNT(*) AS EmployeeCount,
    AVG(e.Salary) AS AvgSalary,
    MIN(e.Salary) AS MinSalary,
    MAX(e.Salary) AS MaxSalary
FROM Employees e
INNER JOIN Departments d ON e.DepartmentID = d.DepartmentID
GROUP BY d.DepartmentName
HAVING COUNT(*) >= 2                   -- Only departments with 2+ employees
   AND AVG(e.Salary) > 70000;         -- And average salary above 70k
```

### TOP and OFFSET-FETCH (Pagination)

```sql
-- TOP: Return only the first N rows
SELECT TOP 3 FirstName, LastName, Salary
FROM Employees
ORDER BY Salary DESC;                  -- Top 3 highest paid

-- OFFSET-FETCH: Pagination (SQL Server 2012+)
SELECT FirstName, LastName, Salary
FROM Employees
ORDER BY EmployeeID
OFFSET 0 ROWS                         -- Skip 0 rows (page 1)
FETCH NEXT 10 ROWS ONLY;              -- Return 10 rows per page
```

---

## T-SQL Programming Features

### Variables and Control Flow

```sql
-- Declaring and using variables
DECLARE @employeeName NVARCHAR(100);
DECLARE @totalSalary DECIMAL(15,2);
DECLARE @deptId INT = 1;               -- Declare and assign in one statement

-- Assign from a query
SELECT @totalSalary = SUM(Salary)
FROM Employees
WHERE DepartmentID = @deptId;

PRINT 'Total salary for dept ' + CAST(@deptId AS VARCHAR) + ': ' + CAST(@totalSalary AS VARCHAR);

-- IF/ELSE conditional
IF @totalSalary > 200000
    PRINT 'Department budget is high';
ELSE IF @totalSalary > 100000
    PRINT 'Department budget is moderate';
ELSE
    PRINT 'Department budget is low';

-- WHILE loop (use BEGIN/END for multi-statement blocks)
DECLARE @counter INT = 1;
WHILE @counter <= 5
BEGIN
    PRINT 'Iteration: ' + CAST(@counter AS VARCHAR);
    SET @counter = @counter + 1;
    IF @counter = 4 BREAK;             -- Exit the loop early
END
```

### TRY-CATCH Error Handling

```sql
BEGIN TRY
    -- Attempt an operation that might fail
    INSERT INTO Employees (FirstName, LastName, Email, Salary, DepartmentID)
    VALUES ('Test', 'User', 'duplicate@company.com', 50000, 999);  -- Bad DepartmentID
END TRY
BEGIN CATCH
    -- Handle the error
    PRINT 'Error Number: ' + CAST(ERROR_NUMBER() AS VARCHAR);
    PRINT 'Error Message: ' + ERROR_MESSAGE();
    PRINT 'Error Severity: ' + CAST(ERROR_SEVERITY() AS VARCHAR);
    PRINT 'Error Line: ' + CAST(ERROR_LINE() AS VARCHAR);
END CATCH
```

### Stored Procedures

```sql
-- Create a stored procedure with input parameters
CREATE OR ALTER PROCEDURE usp_GetEmployeesByDepartment
    @DeptName NVARCHAR(100),           -- Input parameter
    @MinSalary DECIMAL(10,2) = 0       -- Optional parameter with default
AS
BEGIN
    SET NOCOUNT ON;                    -- Suppress "rows affected" messages
    SELECT e.EmployeeID, e.FirstName + ' ' + e.LastName AS FullName, e.Salary
    FROM Employees e
    INNER JOIN Departments d ON e.DepartmentID = d.DepartmentID
    WHERE d.DepartmentName = @DeptName AND e.Salary >= @MinSalary
    ORDER BY e.Salary DESC;
END
GO

EXEC usp_GetEmployeesByDepartment @DeptName = 'Engineering', @MinSalary = 80000;

-- Procedure with OUTPUT parameter
CREATE OR ALTER PROCEDURE usp_GetDepartmentStats
    @DeptId INT,
    @AvgSalary DECIMAL(10,2) OUTPUT,   -- Output parameter
    @EmpCount INT OUTPUT
AS
BEGIN
    SELECT @AvgSalary = AVG(Salary), @EmpCount = COUNT(*)
    FROM Employees
    WHERE DepartmentID = @DeptId;
END
GO

-- Call with output parameters
DECLARE @avg DECIMAL(10,2), @count INT;
EXEC usp_GetDepartmentStats @DeptId = 1, @AvgSalary = @avg OUTPUT, @EmpCount = @count OUTPUT;
```

### User-Defined Functions

```sql
-- Scalar function: Returns a single value
CREATE OR ALTER FUNCTION dbo.fn_GetFullName (@FirstName NVARCHAR(50), @LastName NVARCHAR(50))
RETURNS NVARCHAR(101)
AS
BEGIN
    RETURN @FirstName + ' ' + @LastName;
END
GO

SELECT dbo.fn_GetFullName(FirstName, LastName) AS FullName, Salary FROM Employees;

-- Inline table-valued function: Returns a table result set
CREATE OR ALTER FUNCTION dbo.fn_GetEmployeesAboveSalary (@MinSalary DECIMAL(10,2))
RETURNS TABLE
AS
RETURN (
    SELECT EmployeeID, FirstName, LastName, Salary
    FROM Employees WHERE Salary >= @MinSalary
);
GO

SELECT * FROM dbo.fn_GetEmployeesAboveSalary(80000);  -- Use like a table in FROM clause
```

### Triggers

```sql
-- Create an audit table to store change history
CREATE TABLE EmployeeAudit (
    AuditID INT IDENTITY(1,1) PRIMARY KEY,
    EmployeeID INT,
    Action NVARCHAR(10),               -- INSERT, UPDATE, DELETE
    OldSalary DECIMAL(10,2),
    NewSalary DECIMAL(10,2),
    ChangedAt DATETIME2 DEFAULT SYSDATETIME()
);
GO

-- AFTER trigger: Fires after the operation completes
CREATE OR ALTER TRIGGER trg_EmployeeSalaryAudit
ON Employees
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    -- 'inserted' holds new values, 'deleted' holds old values
    INSERT INTO EmployeeAudit (EmployeeID, Action, OldSalary, NewSalary)
    SELECT i.EmployeeID, 'UPDATE', d.Salary, i.Salary
    FROM inserted i
    INNER JOIN deleted d ON i.EmployeeID = d.EmployeeID
    WHERE i.Salary <> d.Salary;        -- Only log if salary actually changed
END
GO
```

---

## Indexes and Performance

### Clustered and Nonclustered Indexes

```sql
-- Clustered index: Defines the physical order of data in the table
-- A table can have only ONE clustered index (PRIMARY KEY creates one by default)
-- The Employees table already has a clustered index on EmployeeID

-- Nonclustered index: Separate structure pointing back to data rows
CREATE NONCLUSTERED INDEX IX_Employees_LastName
ON Employees (LastName);               -- Speed up queries filtering by LastName

-- Composite index: Multiple columns
CREATE NONCLUSTERED INDEX IX_Employees_Dept_Salary
ON Employees (DepartmentID, Salary DESC);  -- Order matters for query optimization

-- Index with INCLUDE: Add non-key columns to avoid lookups
CREATE NONCLUSTERED INDEX IX_Employees_Email_Include
ON Employees (Email)
INCLUDE (FirstName, LastName, Salary); -- Covers queries needing these columns

-- Unique index
CREATE UNIQUE NONCLUSTERED INDEX IX_Employees_Email_Unique
ON Employees (Email);                  -- Enforces uniqueness like a UNIQUE constraint
```

### Execution Plans

```sql
-- Show I/O and timing statistics for performance analysis
SET STATISTICS IO ON;                  -- Show logical/physical reads
SET STATISTICS TIME ON;                -- Show CPU and elapsed time

SELECT FirstName, LastName, Salary FROM Employees WHERE DepartmentID = 1;

SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;

-- In SSMS: Press Ctrl+M to enable "Include Actual Execution Plan"
-- Look for: Table Scans (bad), Index Seeks (good), Key Lookups (can improve with INCLUDE)
```

---

## Views and Temp Tables

### Views

```sql
-- Create a view: A saved query that acts like a virtual table
CREATE OR ALTER VIEW vw_EmployeeDetails AS
SELECT e.EmployeeID, e.FirstName + ' ' + e.LastName AS FullName,
    e.Email, e.Salary, e.HireDate, d.DepartmentName
FROM Employees e
INNER JOIN Departments d ON e.DepartmentID = d.DepartmentID
WHERE e.IsActive = 1;
GO

SELECT * FROM vw_EmployeeDetails WHERE Salary > 80000;  -- Query like a regular table
```

### Temporary Tables

```sql
-- Local temp table: Visible only in the current session (# prefix)
CREATE TABLE #TempHighEarners (EmployeeID INT, FullName NVARCHAR(101), Salary DECIMAL(10,2));
INSERT INTO #TempHighEarners
SELECT EmployeeID, FirstName + ' ' + LastName, Salary FROM Employees WHERE Salary > 80000;

SELECT * FROM #TempHighEarners;        -- Use like a regular table
DROP TABLE #TempHighEarners;           -- Auto-cleaned when session ends, but explicit drop is good practice

-- Table variables: Scoped to the current batch (no need to drop)
DECLARE @DeptSummary TABLE (DepartmentName NVARCHAR(100), EmployeeCount INT, AvgSalary DECIMAL(10,2));
INSERT INTO @DeptSummary
SELECT d.DepartmentName, COUNT(*), AVG(e.Salary)
FROM Departments d
INNER JOIN Employees e ON d.DepartmentID = e.DepartmentID
GROUP BY d.DepartmentName;

SELECT * FROM @DeptSummary;

-- CTEs as lightweight temp tables (exist only for the next statement)
WITH RecentHires AS (
    SELECT FirstName, LastName, HireDate, Salary
    FROM Employees
    WHERE HireDate >= DATEADD(YEAR, -1, GETDATE())  -- Hired in the last year
)
SELECT * FROM RecentHires ORDER BY HireDate DESC;
```

### When to Use Each

| Feature | Scope | Indexed? | Best For |
| ------- | ----- | -------- | -------- |
| **#Temp Table** | Session | Yes | Large datasets, multiple references, need indexes |
| **@Table Variable** | Batch | Limited | Small datasets (<1000 rows), simple operations |
| **CTE** | Single statement | No | Readability, recursive queries, one-time use |
| **View** | Permanent | No (unless indexed) | Reusable query logic, security abstraction |

---

## Transactions and Isolation Levels

### Transaction Basics

```sql
-- Transaction with error handling and ROLLBACK
BEGIN TRY
    BEGIN TRANSACTION;

    -- Transfer budget between departments
    UPDATE Departments SET Budget = Budget - 50000 WHERE DepartmentName = 'Marketing';
    UPDATE Departments SET Budget = Budget + 50000 WHERE DepartmentName = 'Engineering';

    IF EXISTS (SELECT 1 FROM Departments WHERE Budget < 0)
        RAISERROR('Budget cannot be negative', 16, 1);

    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0                 -- Check if transaction is still open
        ROLLBACK TRANSACTION;          -- Undo all changes
    PRINT 'Transfer failed: ' + ERROR_MESSAGE();
END CATCH
```

### Isolation Levels

```sql
-- READ UNCOMMITTED: Allows dirty reads (fastest, least safe)
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SELECT * FROM Employees WITH (NOLOCK); -- NOLOCK hint is equivalent per-query

-- READ COMMITTED: Default, only reads committed data
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- REPEATABLE READ: Locks rows so they cannot change until transaction ends
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- SERIALIZABLE: Strictest, prevents phantom reads (range locks)
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- SNAPSHOT: Row versioning, reads see a point-in-time snapshot
-- Requires: ALTER DATABASE CompanyDB SET ALLOW_SNAPSHOT_ISOLATION ON;
SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
```

---

## Python Integration with pyodbc

### Connecting and Querying

```python
import pyodbc

# Connection string for SQL Server
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"  # Use appropriate driver version
    "SERVER=localhost;"
    "DATABASE=CompanyDB;"
    "Trusted_Connection=yes;"                   # Windows Authentication
    "TrustServerCertificate=yes;"               # For local development
)

# Establish connection and execute queries
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

cursor.execute("SELECT FirstName, LastName, Salary FROM Employees WHERE DepartmentID = ?", (1,))
for row in cursor.fetchall():
    print(f"{row.FirstName} {row.LastName}: ${row.Salary:,.2f}")  # Access columns by name

# Parameterized INSERT (prevents SQL injection -- use ? placeholders)
cursor.execute(
    "INSERT INTO Employees (FirstName, LastName, Email, Salary, DepartmentID) VALUES (?, ?, ?, ?, ?)",
    ("Frank", "Miller", "frank.m@company.com", 73000.00, 2)
)
conn.commit()                                   # Must commit for INSERT/UPDATE/DELETE

cursor.close()
conn.close()
```

### Using Context Managers

```python
# Context manager ensures connection is closed even if an error occurs
with pyodbc.connect(conn_str) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT EmployeeID, FirstName, LastName, Salary FROM Employees")
        columns = [col[0] for col in cursor.description]  # Get column names
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        for emp in results:
            print(emp)  # {'EmployeeID': 1, 'FirstName': 'Alice', ...}
```

---

## Practice Exercises

### Exercise 1: Table Design

Create a `Products` table with columns for ProductID (identity), ProductName, Category, Price, StockQuantity, and CreatedAt. Add appropriate constraints.

```sql
-- Try it yourself, then check:
CREATE TABLE Products (
    ProductID INT IDENTITY(1,1) PRIMARY KEY,
    ProductName NVARCHAR(200) NOT NULL,
    Category NVARCHAR(50) NOT NULL,
    Price DECIMAL(10,2) NOT NULL CHECK (Price >= 0),
    StockQuantity INT NOT NULL DEFAULT 0 CHECK (StockQuantity >= 0),
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
```

### Exercise 2: Complex Query

Write a query to find the second highest salary in each department using window functions.

```sql
-- Solution using CTE and ROW_NUMBER
WITH RankedSalaries AS (
    SELECT
        FirstName,
        LastName,
        Salary,
        DepartmentID,
        ROW_NUMBER() OVER (
            PARTITION BY DepartmentID
            ORDER BY Salary DESC
        ) AS SalaryRank
    FROM Employees
)
SELECT FirstName, LastName, Salary, DepartmentID
FROM RankedSalaries
WHERE SalaryRank = 2;                  -- Second highest per department
```

### Exercise 3: Stored Procedure with Error Handling

Create a procedure that transfers an employee between departments with validation and rollback on failure.

```sql
CREATE OR ALTER PROCEDURE usp_TransferEmployee
    @EmployeeID INT,
    @NewDepartmentID INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        IF NOT EXISTS (SELECT 1 FROM Employees WHERE EmployeeID = @EmployeeID)
            RAISERROR('Employee not found', 16, 1);
        IF NOT EXISTS (SELECT 1 FROM Departments WHERE DepartmentID = @NewDepartmentID)
            RAISERROR('Department not found', 16, 1);

        UPDATE Employees SET DepartmentID = @NewDepartmentID WHERE EmployeeID = @EmployeeID;
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;                         -- Re-throw the error to the caller
    END CATCH
END
GO
```

### Exercise 4: Pagination Query

Write a query that supports pagination for an employee directory, 20 records per page.

```sql
DECLARE @PageNumber INT = 1;
DECLARE @PageSize INT = 20;

SELECT EmployeeID, FirstName + ' ' + LastName AS FullName, Email, Salary
FROM Employees
ORDER BY LastName, FirstName
OFFSET (@PageNumber - 1) * @PageSize ROWS  -- Calculate rows to skip
FETCH NEXT @PageSize ROWS ONLY;             -- Return one page of results
```

---

## Summary

Key takeaways from this introduction to SQL Server:

- **SQL Server** is Microsoft's enterprise RDBMS, available in free (Express, Developer) and paid editions
- **T-SQL** extends standard SQL with variables, control flow, error handling, and procedural features
- **Data types** include `INT`, `VARCHAR`/`NVARCHAR`, `DATETIME2`, `BIT`, `DECIMAL`, and `UNIQUEIDENTIFIER`
- **Tables** support identity columns, primary/foreign keys, CHECK constraints, and default values
- **JOINs** (INNER, LEFT, RIGHT, FULL) combine related tables; **CTEs** improve readability
- **Window functions** (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD`) enable advanced analytics without collapsing rows
- **Stored procedures** and **functions** encapsulate reusable logic on the server
- **Triggers** automate auditing and enforce business rules on data changes
- **Indexes** (clustered, nonclustered, with INCLUDE) are critical for query performance
- **Temp tables** (`#temp`), **table variables** (`@var`), and **CTEs** serve different scoping needs
- **Transactions** with `TRY-CATCH` ensure data integrity; isolation levels control concurrency
- **pyodbc** provides Python connectivity using parameterized queries

## Next Steps

- Practice writing complex queries with multiple JOINs and window functions
- Learn about **indexed views** and **columnstore indexes** for analytical workloads
- Explore **SQL Server Agent** for scheduling jobs and automated maintenance
- Study **database design and normalization** (1NF, 2NF, 3NF)
- Investigate **Always Encrypted** and **Row-Level Security** for data protection
- Experiment with **SQL Server Integration Services (SSIS)** for ETL pipelines
- Try **Azure SQL Database** for cloud-hosted SQL Server

## Additional Resources

- [Microsoft SQL Server Documentation](https://learn.microsoft.com/en-us/sql/sql-server/)
- [T-SQL Reference](https://learn.microsoft.com/en-us/sql/t-sql/language-reference)
- [SQL Server Management Studio (SSMS)](https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms)
- [pyodbc Documentation](https://github.com/mkleehammer/pyodbc/wiki)
- [SQL Server Sample Databases (AdventureWorks, WideWorldImporters)](https://learn.microsoft.com/en-us/sql/samples/sql-samples-where-are)
