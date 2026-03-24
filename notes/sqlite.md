# Introduction to SQLite

## Table of Contents

1. [What is SQLite?](#what-is-sqlite)
2. [Installation and Setup](#installation-and-setup)
3. [Database Basics](#database-basics)
4. [Data Types and Type Affinity](#data-types-and-type-affinity)
5. [Creating Tables](#creating-tables)
6. [CRUD Operations](#crud-operations)
7. [Querying Data](#querying-data)
8. [Python Integration](#python-integration)
9. [Transactions](#transactions)
10. [Full-Text Search (FTS5)](#full-text-search-fts5)
11. [JSON Support](#json-support)
12. [Performance Tips](#performance-tips)
13. [Practice Exercises](#practice-exercises)
14. [Summary](#summary)

---

## What is SQLite?

SQLite is a self-contained, serverless, zero-configuration SQL database engine. It provides:
- **Serverless**: No separate server process — the library reads/writes directly to a file on disk
- **File-based**: An entire database lives in a single cross-platform file
- **Embedded**: Linked directly into your application (a C library, ~600 KB)
- **Zero-configuration**: No setup, no administration, no user management
- **ACID-compliant**: Full transaction support with crash recovery
- **Ubiquitous**: Deployed on billions of devices (phones, browsers, OSes, embedded systems)

```python
# SQLite is already built into Python's standard library
import sqlite3

# That's it — no pip install, no server to start, no config files
print(sqlite3.sqlite_version)  # e.g., "3.39.4" (underlying C library version)
print(sqlite3.version)         # e.g., "2.6.0" (Python module version)
```

**When to use SQLite:**
- Embedded applications and mobile apps
- Local data storage and caching
- Prototyping before migrating to PostgreSQL/MySQL
- Data analysis on small-to-medium datasets (up to ~1 TB)
- Testing (in-memory databases spin up instantly)
- Configuration and application state storage
- Single-writer, moderate-read workloads

**When NOT to use SQLite:**
- High-concurrency write-heavy applications (one writer at a time)
- Client/server architectures with many simultaneous users
- Very large datasets exceeding a few terabytes
- Situations requiring fine-grained user permissions/roles
- Distributed or replicated database needs

---

## Installation and Setup

```bash
# Python: sqlite3 is part of the standard library — nothing to install
python3 -c "import sqlite3; print(sqlite3.sqlite_version)"

# The sqlite3 CLI tool (usually pre-installed on macOS and Linux)
sqlite3 --version

# Install the CLI on Ubuntu/Debian if needed
sudo apt install sqlite3

# Install on macOS via Homebrew (for a newer version)
brew install sqlite
```

```bash
# Open or create a database file with the CLI
sqlite3 myapp.db

# Open an in-memory database (useful for quick experiments)
sqlite3 :memory:
```

---

## Database Basics

```bash
# The sqlite3 CLI uses dot-commands (not SQL — no semicolons needed)
sqlite3 myapp.db

.tables                     # show all tables
.schema users               # show schema for a specific table
.headers on                 # toggle column headers
.mode column                # output format: column, csv, json, table, markdown
.show                       # show current settings
.import --csv data.csv t    # import CSV into table t
.output results.csv         # redirect output to a file
.read setup.sql             # run a SQL file
.quit                       # exit the CLI
```

```sql
-- Every SQLite database has a special table listing all objects
SELECT name, type FROM sqlite_master
WHERE type = 'table'
ORDER BY name;

-- Check SQLite version from SQL
SELECT sqlite_version();
```

---

## Data Types and Type Affinity

SQLite uses **dynamic typing** — any column can hold any type regardless of the declared type. The declared type determines the column's **type affinity** (a preference, not a constraint).

```sql
-- SQLite has five storage classes (not traditional "data types")
-- INTEGER  — signed integer (1, 2, 3, 4, 6, or 8 bytes)
-- REAL     — 8-byte IEEE floating-point number
-- TEXT     — UTF-8 or UTF-16 string
-- BLOB     — raw binary data, stored exactly as input
-- NULL     — the absence of a value

-- Type affinity rules: SQLite maps declared types to affinities
-- "INT", "INTEGER", "TINYINT", "BIGINT"  →  INTEGER affinity
-- "CHAR", "VARCHAR", "TEXT", "CLOB"      →  TEXT affinity
-- "REAL", "DOUBLE", "FLOAT"              →  REAL affinity
-- "BLOB" or no type specified            →  BLOB affinity (NONE)
-- Anything else                          →  NUMERIC affinity
```

```sql
-- Dynamic typing means this is perfectly valid in SQLite
CREATE TABLE flexible (value ANY);
INSERT INTO flexible VALUES (42);         -- stored as INTEGER
INSERT INTO flexible VALUES (3.14);       -- stored as REAL
INSERT INTO flexible VALUES ('hello');    -- stored as TEXT
INSERT INTO flexible VALUES (NULL);       -- stored as NULL
INSERT INTO flexible VALUES (x'CAFE');   -- stored as BLOB

-- Check what type SQLite actually stored
SELECT value, typeof(value) FROM flexible;
-- 42      | integer
-- 3.14    | real
-- hello   | text
--         | null
-- (blob)  | blob
```

```sql
-- STRICT tables (SQLite 3.37+) enforce types like traditional databases
CREATE TABLE measurements (
    id INTEGER PRIMARY KEY,
    label TEXT NOT NULL,
    reading REAL NOT NULL
) STRICT;

-- This would raise an error in a STRICT table:
-- INSERT INTO measurements VALUES (1, 'temp', 'not_a_number');
-- Error: cannot store TEXT value in REAL column
```

---

## Creating Tables

```sql
-- Basic table creation
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- auto-incrementing PK
    username TEXT NOT NULL UNIQUE,          -- must be unique and non-null
    email TEXT NOT NULL,
    age INTEGER CHECK(age >= 0),           -- check constraint
    bio TEXT DEFAULT '',                    -- default value
    created_at TEXT DEFAULT (datetime('now'))  -- default to current timestamp
);

-- INTEGER PRIMARY KEY is special in SQLite: it becomes an alias for rowid
-- AUTOINCREMENT prevents rowid reuse (slightly slower, rarely needed)
-- Without AUTOINCREMENT, SQLite reuses deleted rowids

-- Table with a composite primary key
CREATE TABLE enrollments (
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrolled_at TEXT DEFAULT (datetime('now')),
    grade REAL,
    PRIMARY KEY (student_id, course_id)
);
```

```sql
-- Foreign key constraints (must be enabled per connection)
PRAGMA foreign_keys = ON;  -- off by default for backward compatibility

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
    -- Foreign key referencing the users table
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE      -- delete posts when user is deleted
        ON UPDATE CASCADE      -- update user_id if user id changes
);

-- WITHOUT ROWID tables (optimization for certain access patterns)
-- Useful when the primary key is not an integer and you want clustered storage
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
) WITHOUT ROWID;

-- WITHOUT ROWID tables store data ordered by primary key
-- Faster for lookups by PK, smaller on disk when PK is the main access path
-- Cannot use AUTOINCREMENT with WITHOUT ROWID
```

```sql
-- Other useful table operations
CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value BLOB, expires_at INTEGER);

CREATE TABLE active_users AS SELECT id, username, email FROM users WHERE age >= 18; -- from query
ALTER TABLE active_users RENAME TO verified_users;  -- rename
ALTER TABLE users ADD COLUMN avatar_url TEXT DEFAULT '';  -- add column
ALTER TABLE users DROP COLUMN avatar_url;  -- drop column (SQLite 3.35.0+)
DROP TABLE IF EXISTS verified_users;
```

---

## CRUD Operations

```sql
-- CREATE (INSERT)
INSERT INTO users (username, email, age) VALUES ('alice', 'alice@example.com', 30);
INSERT INTO users (username, email, age) VALUES ('bob', 'bob@example.com', 25);

-- Insert multiple rows at once
INSERT INTO users (username, email, age) VALUES
    ('charlie', 'charlie@example.com', 35),
    ('diana', 'diana@example.com', 28),
    ('eve', 'eve@example.com', 22);

-- Upsert with ON CONFLICT (SQLite 3.24+)
INSERT INTO users (username, email, age) VALUES ('alice', 'alice@work.com', 31)
ON CONFLICT(username) DO UPDATE SET
    email = excluded.email,   -- "excluded" refers to the row that would be inserted
    age = excluded.age;
```

```sql
-- READ (SELECT)
SELECT * FROM users;                          -- all rows
SELECT username, email FROM users;            -- specific columns
SELECT * FROM users WHERE age > 25;           -- filter
SELECT * FROM users ORDER BY age DESC;        -- sort
SELECT * FROM users LIMIT 10 OFFSET 20;      -- pagination
SELECT DISTINCT age FROM users;               -- unique values
```

```sql
-- UPDATE
UPDATE users SET email = 'alice@newmail.com' WHERE username = 'alice';

UPDATE posts SET title = UPPER(title)
WHERE user_id = (SELECT id FROM users WHERE username = 'alice');  -- with subquery
```

```sql
-- DELETE
DELETE FROM users WHERE username = 'eve';
DELETE FROM users;  -- delete all rows (table structure remains)
```

---

## Querying Data

```sql
-- JOINs work just like other SQL databases
-- INNER JOIN: only matching rows from both tables
SELECT u.username, p.title, p.created_at
FROM users u
INNER JOIN posts p ON u.id = p.user_id
ORDER BY p.created_at DESC;

-- LEFT JOIN: all rows from left table, matching rows from right
SELECT u.username, COUNT(p.id) AS post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id;

```

```sql
-- Subqueries
SELECT username,
       (SELECT COUNT(*) FROM posts WHERE posts.user_id = users.id) AS post_count
FROM users;  -- scalar subquery in SELECT

SELECT * FROM users
WHERE id IN (SELECT DISTINCT user_id FROM posts);  -- subquery in WHERE
```

```sql
-- Common Table Expressions (CTEs) — cleaner than nested subqueries
WITH active_authors AS (
    SELECT user_id, COUNT(*) AS post_count
    FROM posts
    GROUP BY user_id
    HAVING COUNT(*) >= 3
)
SELECT u.username, a.post_count
FROM users u
JOIN active_authors a ON u.id = a.user_id
ORDER BY a.post_count DESC;

-- Recursive CTE (e.g., generating a sequence of numbers)
WITH RECURSIVE counter(n) AS (
    SELECT 1               -- base case
    UNION ALL
    SELECT n + 1 FROM counter WHERE n < 10  -- recursive step
)
SELECT n FROM counter;
```

```sql
-- Window Functions (SQLite 3.25+, 2018)
-- Perform calculations across related rows without collapsing them
SELECT
    username,
    age,
    ROW_NUMBER() OVER (ORDER BY age) AS row_num,
    RANK() OVER (ORDER BY age) AS rank,
    AVG(age) OVER () AS overall_avg,         -- avg across all rows
    LAG(username) OVER (ORDER BY age) AS prev_user,
    LEAD(username) OVER (ORDER BY age) AS next_user
FROM users;

-- Window function with PARTITION BY
SELECT
    u.username,
    p.title,
    p.created_at,
    ROW_NUMBER() OVER (
        PARTITION BY u.id           -- restart numbering per user
        ORDER BY p.created_at DESC  -- newest first
    ) AS post_rank
FROM users u
JOIN posts p ON u.id = p.user_id;
```

```sql
-- GROUP BY with aggregate functions
SELECT
    CASE WHEN age < 25 THEN 'young' WHEN age < 35 THEN 'mid' ELSE 'senior' END AS age_group,
    COUNT(*) AS count, AVG(age) AS avg_age,
    GROUP_CONCAT(username, ', ') AS names  -- SQLite-specific string aggregation
FROM users
GROUP BY age_group
HAVING COUNT(*) > 1;

-- LIMIT and OFFSET for pagination
SELECT * FROM posts ORDER BY created_at DESC LIMIT 10;           -- first page
SELECT * FROM posts ORDER BY created_at DESC LIMIT 10 OFFSET 10; -- second page

-- Keyset pagination (faster on large tables — avoids scanning skipped rows)
SELECT * FROM posts WHERE created_at < '2025-01-15T00:00:00'
ORDER BY created_at DESC LIMIT 10;
```

---

## Python Integration

```python
import sqlite3

# Connect to a database file (created if it doesn't exist)
conn = sqlite3.connect("myapp.db")

# Or use an in-memory database (great for testing)
conn = sqlite3.connect(":memory:")

# Always enable foreign keys (off by default)
conn.execute("PRAGMA foreign_keys = ON")

# Create a cursor to execute SQL
cursor = conn.cursor()

# Execute a single statement
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        age INTEGER CHECK(age >= 0),
        created_at TEXT DEFAULT (datetime('now'))
    )
""")

# Commit the change
conn.commit()

# Always close when done
conn.close()
```

```python
# Parameterized queries — ALWAYS use these to prevent SQL injection
conn = sqlite3.connect("myapp.db")
cursor = conn.cursor()

# Use ? placeholders (positional parameters)
cursor.execute(
    "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
    ("alice", "alice@example.com", 30)
)

# Use :name placeholders (named parameters)
cursor.execute(
    "INSERT INTO users (username, email, age) VALUES (:name, :email, :age)",
    {"name": "bob", "email": "bob@example.com", "age": 25}
)

# NEVER do string formatting — SQL injection risk:
# cursor.execute(f"INSERT INTO users (username) VALUES ('{user_input}')")
conn.commit()
```

```python
# Fetching results
cursor.execute("SELECT * FROM users WHERE age > ?", (20,))

row = cursor.fetchone()     # returns a single row as a tuple, or None
rows = cursor.fetchall()    # returns all remaining rows as a list of tuples
many = cursor.fetchmany(5)  # returns up to 5 rows

# Iterate directly over the cursor (memory-efficient for large results)
cursor.execute("SELECT username, age FROM users ORDER BY age")
for username, age in cursor:
    print(f"{username}: {age}")
```

```python
# executemany() for batch inserts — much faster than looping execute()
users_data = [
    ("charlie", "charlie@example.com", 35),
    ("diana", "diana@example.com", 28),
    ("eve", "eve@example.com", 22),
    ("frank", "frank@example.com", 40),
]

cursor.executemany(
    "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
    users_data
)
conn.commit()
```

```python
# Context managers — the recommended way to handle connections
# The context manager auto-commits on success, auto-rolls-back on exception
import sqlite3

with sqlite3.connect("myapp.db") as conn:
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute(
        "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
        ("grace", "grace@example.com", 27)
    )
    # No need to call conn.commit() — done automatically on exit
    # If an exception occurs, changes are rolled back automatically

# Note: the context manager does NOT close the connection
# For full cleanup, combine with a try/finally or use a helper function
```

```python
# Row factories — access columns by name instead of index
conn = sqlite3.connect("myapp.db")
conn.row_factory = sqlite3.Row  # built-in Row factory

cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE username = ?", ("alice",))
user = cursor.fetchone()

# Access by column name (like a dict)
print(user["username"])    # "alice"
print(user["email"])       # "alice@example.com"
print(user["age"])         # 30

# Row objects also support index access and iteration
print(user[0])             # id value
print(dict(user))          # convert to a regular dict
print(user.keys())         # list of column names
```

```python
# Custom row factory returning namedtuples
from collections import namedtuple

def namedtuple_factory(cursor, row):
    fields = [description[0] for description in cursor.description]
    return namedtuple("Row", fields)(*row)

conn = sqlite3.connect("myapp.db")
conn.row_factory = namedtuple_factory
for user in conn.execute("SELECT username, email, age FROM users"):
    print(f"{user.username} ({user.age}): {user.email}")
```

```python
# A practical helper class wrapping common SQLite patterns
import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")  # better concurrency
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def query(self, sql, params=()):
        with self.get_connection() as conn:
            return conn.execute(sql, params).fetchall()

    def execute(self, sql, params=()):
        with self.get_connection() as conn:
            return conn.execute(sql, params)

    def executemany(self, sql, params_list):
        with self.get_connection() as conn:
            return conn.executemany(sql, params_list)

# Usage
db = Database("myapp.db")
users = db.query("SELECT * FROM users WHERE age > ?", (25,))
for user in users:
    print(dict(user))
```

---

## Transactions

```sql
-- By default, each statement auto-commits. Explicit transactions are faster and atomic.
BEGIN TRANSACTION;
    INSERT INTO users (username, email, age) VALUES ('test1', 't1@x.com', 20);
    INSERT INTO users (username, email, age) VALUES ('test2', 't2@x.com', 21);
COMMIT;
-- Use ROLLBACK to undo all changes within a transaction
```

```python
# Python's sqlite3 auto-begins transactions before DML statements
# You must call conn.commit() to persist, or conn.rollback() to undo
conn = sqlite3.connect("myapp.db")
try:
    conn.execute("BEGIN")
    conn.execute("UPDATE users SET age = age + 1 WHERE username = ?", ("alice",))
    conn.execute("UPDATE users SET age = age - 1 WHERE username = ?", ("bob",))
    conn.commit()   # both changes applied atomically
except Exception:
    conn.rollback()  # neither change applied
```

```sql
-- WAL (Write-Ahead Logging) — recommended for most applications
-- Persists across connections (set it once, stored in the database)
PRAGMA journal_mode = WAL;
-- Benefits: readers don't block writers, faster for most workloads
-- Drawbacks: two files on disk (.db + .db-wal), not for network filesystems
```

```python
# Setting WAL mode and isolation level in Python
conn = sqlite3.connect("myapp.db")
conn.execute("PRAGMA journal_mode = WAL")
conn.isolation_level = "IMMEDIATE"  # options: "DEFERRED" (default), "IMMEDIATE", "EXCLUSIVE"
# IMMEDIATE acquires a write lock right away — prevents other writers
```

---

## Full-Text Search (FTS5)

```sql
-- FTS5 enables fast text search across large amounts of text
-- It creates a virtual table with its own inverted index

-- Create an FTS5 virtual table
CREATE VIRTUAL TABLE articles_fts USING fts5(
    title,            -- columns to index
    body,             -- all columns are TEXT in FTS5
    content='articles',          -- link to an existing content table
    content_rowid='id'           -- which column maps to rowid
);

-- Or a standalone FTS table (simpler, stores its own data)
CREATE VIRTUAL TABLE notes_fts USING fts5(title, body);
INSERT INTO notes_fts (title, body) VALUES
    ('Python Basics', 'Python is a versatile programming language'),
    ('SQLite Guide', 'SQLite is an embedded database engine'),
    ('Web Dev', 'Flask and Django are Python web frameworks');
```

```sql
-- Search using MATCH (much faster than LIKE for text search)
SELECT * FROM notes_fts WHERE notes_fts MATCH 'python';
SELECT * FROM notes_fts WHERE notes_fts MATCH '"programming language"';  -- phrase search
SELECT * FROM notes_fts WHERE notes_fts MATCH 'python OR sqlite';       -- boolean operators
SELECT * FROM notes_fts WHERE notes_fts MATCH 'prog*';                  -- prefix search
SELECT * FROM notes_fts WHERE notes_fts MATCH 'title:python';           -- column-specific

-- Rank results by relevance
SELECT *, rank FROM notes_fts WHERE notes_fts MATCH 'python' ORDER BY rank;

-- Highlight matching terms and show snippets
SELECT highlight(notes_fts, 0, '<b>', '</b>') AS title,
       snippet(notes_fts, 1, '<b>', '</b>', '...', 20) AS preview
FROM notes_fts WHERE notes_fts MATCH 'python';
```

```python
# Using FTS5 from Python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE VIRTUAL TABLE docs USING fts5(title, content)")
conn.executemany(
    "INSERT INTO docs (title, content) VALUES (?, ?)",
    [
        ("Python Tutorial", "Learn Python programming from scratch"),
        ("SQLite Handbook", "Master embedded SQL database with Python"),
        ("Data Science", "Use Python and pandas for data analysis"),
    ]
)

# Search and rank results
results = conn.execute(
    "SELECT title, rank FROM docs WHERE docs MATCH ? ORDER BY rank",
    ("python",)
).fetchall()
for title, rank in results:
    print(f"{title} (relevance: {rank:.4f})")
```

---

## JSON Support

```sql
-- SQLite has built-in JSON functions (since 3.9.0, 2015)
-- JSON is stored as TEXT but can be queried with special functions

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    metadata TEXT NOT NULL  -- stores JSON as plain text
);

INSERT INTO events (name, metadata) VALUES
    ('signup', '{"user": "alice", "plan": "pro", "source": "google"}'),
    ('purchase', '{"user": "bob", "amount": 49.99, "items": ["book", "pen"]}'),
    ('signup', '{"user": "charlie", "plan": "free", "source": "twitter"}');
```

```sql
-- json_extract(): pull values out of JSON
SELECT
    name,
    json_extract(metadata, '$.user') AS user,
    json_extract(metadata, '$.plan') AS plan
FROM events
WHERE name = 'signup';

-- The -> and ->> operators (SQLite 3.38+, 2022) — shorthand for json_extract
-- -> returns a JSON value, ->> returns a SQL value (unquoted text)
SELECT
    metadata->>'$.user' AS user,
    metadata->>'$.plan' AS plan
FROM events
WHERE name = 'signup';

-- Filter by JSON values
SELECT * FROM events
WHERE json_extract(metadata, '$.plan') = 'pro';
```

```sql
-- json_each(): expand a JSON array into rows
SELECT e.name, json_extract(e.metadata, '$.user') AS user, j.value AS item
FROM events e, json_each(json_extract(e.metadata, '$.items')) j
WHERE e.name = 'purchase';
-- Result: purchase | bob | book  /  purchase | bob | pen

-- Build and aggregate JSON from SQL values
SELECT json_object('name', username, 'age', age) AS user_json FROM users;
SELECT json_group_array(username) AS all_users FROM users;
SELECT json_group_object(username, age) AS user_ages FROM users;
SELECT json_valid('{"key": "value"}');  -- 1 (valid)
```

---

## Performance Tips

```sql
-- INDEXES: speed up lookups on frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE INDEX idx_posts_user_date ON posts(user_id, created_at);  -- composite index

-- Check what indexes exist
SELECT name, tbl_name, sql FROM sqlite_master WHERE type = 'index';

-- See the query plan to verify index usage
EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'alice@example.com';
-- SEARCH users USING INDEX idx_users_email (email=?)
```

```sql
-- PRAGMA statements for performance (connection-level, must be set each time)
PRAGMA journal_mode = WAL;       -- write-ahead logging for better concurrency
PRAGMA synchronous = NORMAL;     -- safe with WAL, faster than FULL (default)
PRAGMA cache_size = -64000;      -- 64 MB page cache (negative = KB)
PRAGMA temp_store = MEMORY;      -- keep temp tables in RAM
PRAGMA mmap_size = 268435456;    -- memory-map up to 256 MB of the database file
PRAGMA busy_timeout = 5000;      -- wait up to 5 seconds if database is locked
ANALYZE;                         -- collect statistics for the query planner
```

```python
# Batch inserts: dramatically faster with transactions
import sqlite3, time

conn = sqlite3.connect("bench.db")
conn.execute("PRAGMA journal_mode = WAL")
conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, value TEXT)")
data = [(i, f"value_{i}") for i in range(100_000)]

# SLOW: autocommit (each insert is its own transaction)
start = time.time()
for row in data:
    conn.execute("INSERT INTO test VALUES (?, ?)", row)
    conn.commit()
print(f"Individual commits: {time.time() - start:.2f}s")

conn.execute("DELETE FROM test")

# FAST: single transaction with executemany() — typically 50-100x faster
start = time.time()
conn.executemany("INSERT INTO test VALUES (?, ?)", data)
conn.commit()
print(f"Batch insert: {time.time() - start:.2f}s")
conn.close()
```

```python
# Recommended connection setup for most Python applications
import sqlite3

def get_optimized_connection(db_path):
    """Create a connection with production-ready PRAGMA settings."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 5000")
    conn.execute("PRAGMA cache_size = -64000")
    conn.execute("PRAGMA temp_store = MEMORY")
    return conn

# Use it everywhere you open a connection
conn = get_optimized_connection("myapp.db")
```

---

## Practice Exercises

### Exercise 1: Build a Task Manager

```python
# Create a CLI task manager backed by SQLite
# Requirements:
# - Table: tasks (id, title, description, status, priority, created_at, completed_at)
# - Functions: add_task(), list_tasks(), complete_task(), delete_task()
# - Use parameterized queries and context managers
# - Add an index on status for filtering

import sqlite3
from datetime import datetime

def init_db(db_path="tasks.db"):
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending','done')),
                priority INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                completed_at TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")

# Implement the remaining functions as practice:
# add_task(title, description="", priority=0)
# list_tasks(status=None)  — filter by status if provided
# complete_task(task_id)    — set status='done' and completed_at
# delete_task(task_id)
```

### Exercise 2: Full-Text Search Application

```python
# Build a searchable notes application using FTS5
# Requirements:
# - Tables: notes (id, title, body, created_at) and notes_fts (FTS5)
# - Keep FTS index in sync when notes are added/updated/deleted
# - Implement search with ranked results and highlighted snippets
# - Use triggers to auto-sync the FTS index:

# CREATE TRIGGER notes_ai AFTER INSERT ON notes BEGIN
#     INSERT INTO notes_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
# END;

# CREATE TRIGGER notes_ad AFTER DELETE ON notes BEGIN
#     INSERT INTO notes_fts(notes_fts, rowid, title, body)
#     VALUES ('delete', old.id, old.title, old.body);
# END;
```

### Exercise 3: JSON Event Store

```python
# Create an event store that logs application events as JSON
# Requirements:
# - Table: events (id, event_type, payload JSON, created_at)
# - Insert events with arbitrary JSON payloads
# - Query events by JSON fields using json_extract()
# - Aggregate data from JSON using json_each() and json_group_array()
# - Find all events where payload.user = 'alice'
# - Count events grouped by payload.source
```

---

## Summary

These notes cover the fundamental concepts of SQLite:

1. **Architecture**: Serverless, file-based, embedded database with zero configuration
2. **Data Types**: Five storage classes (INTEGER, REAL, TEXT, BLOB, NULL) with type affinity
3. **Tables**: CREATE TABLE with constraints, foreign keys, AUTOINCREMENT, WITHOUT ROWID
4. **CRUD**: INSERT (with upsert), SELECT, UPDATE, DELETE operations
5. **Querying**: JOINs, subqueries, CTEs, window functions, GROUP BY, pagination
6. **Python Integration**: sqlite3 module with connections, cursors, parameterized queries, row factories
7. **Transactions**: Autocommit behavior, explicit transactions, WAL mode for concurrency
8. **FTS5**: Full-text search with MATCH, ranking, highlighting, and snippets
9. **JSON**: json_extract, json_each, ->> operator for querying JSON stored as TEXT
10. **Performance**: Indexes, PRAGMA tuning, WAL mode, batch inserts with executemany

### Next Steps

1. Build a small Python project with SQLite as the backend (CLI tool, web app, data pipeline)
2. Learn about SQLAlchemy for ORM-style access to SQLite (and easy migration to PostgreSQL)
3. Explore Datasette for instant web APIs on top of SQLite databases
4. Study Litestream for SQLite replication and backup
5. Practice writing complex queries with CTEs, window functions, and JSON functions

### Additional Resources

- **SQLite Official Docs**: https://www.sqlite.org/docs.html
- **Python sqlite3 Module**: https://docs.python.org/3/library/sqlite3.html
- **SQLite Tutorial**: https://www.sqlitetutorial.net/
- **Datasette**: https://datasette.io/
