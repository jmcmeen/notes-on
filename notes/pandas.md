# Introduction to Pandas

## Table of Contents

1. [What is Pandas?](#what-is-pandas)
2. [Installation and Setup](#installation-and-setup)
3. [Series](#series)
4. [DataFrames](#dataframes)
5. [Loading and Saving Data](#loading-and-saving-data)
6. [Indexing and Selection](#indexing-and-selection)
7. [Data Cleaning](#data-cleaning)
8. [Data Transformation](#data-transformation)
9. [Grouping and Aggregation](#grouping-and-aggregation)
10. [Merging and Joining](#merging-and-joining)
11. [Time Series](#time-series)
12. [Visualization](#visualization)
13. [Performance Tips](#performance-tips)
14. [Practice Exercises](#practice-exercises)
15. [Summary](#summary)

---

## What is Pandas?

Pandas is a Python library for data manipulation and analysis. It provides:
- **DataFrame**: 2D labeled data structure (like a spreadsheet or SQL table)
- **Series**: 1D labeled array
- **Data I/O**: Read/write CSV, Excel, SQL, JSON, Parquet, and more
- **Data cleaning**: Handle missing values, duplicates, type conversion
- **Grouping**: Split-apply-combine operations
- **Merging**: SQL-style joins, concatenation
- **Time series**: Date range generation, frequency conversion, resampling

---

## Installation and Setup

```bash
pip install pandas
```

```python
import pandas as pd
import numpy as np

print(pd.__version__)

# Display options
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 50)
pd.set_option("display.width", 120)
```

---

## Series

```python
# Creating a Series
s = pd.Series([10, 20, 30, 40, 50])
print(s)
# 0    10
# 1    20
# 2    30
# 3    40
# 4    50
# dtype: int64

# With custom index
s = pd.Series([10, 20, 30], index=["a", "b", "c"])
print(s["a"])     # 10
print(s[["a", "c"]])  # Select multiple

# From dictionary
s = pd.Series({"apples": 5, "bananas": 3, "cherries": 8})

# Properties
print(s.values)    # NumPy array: [5 3 8]
print(s.index)     # Index(['apples', 'bananas', 'cherries'])
print(s.dtype)     # int64
print(s.shape)     # (3,)

# Operations (vectorized)
print(s * 2)       # Double all values
print(s[s > 4])    # Filter: apples=5, cherries=8
print(s.sum())     # 16
print(s.mean())    # 5.333
print(s.describe())  # Summary statistics
```

---

## DataFrames

### Creating DataFrames

```python
# From dictionary
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana"],
    "age": [25, 30, 35, 28],
    "city": ["NYC", "LA", "Chicago", "NYC"],
    "salary": [70000, 85000, 90000, 75000]
})
print(df)
#       name  age     city  salary
# 0    Alice   25      NYC   70000
# 1      Bob   30       LA   85000
# 2  Charlie   35  Chicago   90000
# 3    Diana   28      NYC   75000

# From list of dicts
data = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30}
]
df2 = pd.DataFrame(data)

# From NumPy array
arr = np.random.randint(0, 100, size=(3, 4))
df3 = pd.DataFrame(arr, columns=["A", "B", "C", "D"])
```

### Inspecting DataFrames

```python
print(df.head(2))        # First 2 rows
print(df.tail(2))        # Last 2 rows
print(df.shape)          # (4, 4)
print(df.columns)        # Index(['name', 'age', 'city', 'salary'])
print(df.dtypes)         # Data types per column
print(df.info())         # Summary including non-null counts
print(df.describe())     # Statistical summary of numeric columns
print(df.nunique())      # Number of unique values per column
print(df.value_counts("city"))  # Value counts for a column
```

---

## Loading and Saving Data

```python
# CSV
df = pd.read_csv("data.csv")
df = pd.read_csv("data.csv", index_col=0, parse_dates=["date"])
df.to_csv("output.csv", index=False)

# Excel
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
df.to_excel("output.xlsx", index=False)

# JSON
df = pd.read_json("data.json")
df.to_json("output.json", orient="records")

# Parquet (fast, columnar format)
df = pd.read_parquet("data.parquet")
df.to_parquet("output.parquet")

# SQL
import sqlite3
conn = sqlite3.connect("database.db")
df = pd.read_sql("SELECT * FROM users", conn)
df.to_sql("users_backup", conn, if_exists="replace", index=False)

# Clipboard
# df = pd.read_clipboard()  # Paste from spreadsheet

# From URL
# df = pd.read_csv("https://example.com/data.csv")

# Read options
df = pd.read_csv("data.csv",
    sep=",",                  # Delimiter
    header=0,                 # Row number for header (None = no header)
    names=["a", "b", "c"],    # Column names
    usecols=["a", "b"],       # Only read these columns
    nrows=1000,               # Only read first 1000 rows
    skiprows=5,               # Skip first 5 rows
    na_values=["N/A", ""],    # Treat as NaN
    dtype={"a": int, "b": str}  # Column types
)
```

---

## Indexing and Selection

### Column Selection

```python
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "salary": [70000, 85000, 90000]
})

# Single column (returns Series)
print(df["name"])
print(df.name)          # Dot notation (avoid if column name has spaces)

# Multiple columns (returns DataFrame)
print(df[["name", "age"]])
```

### Row Selection with loc and iloc

```python
# loc - label-based indexing
print(df.loc[0])                    # First row (by index label)
print(df.loc[0:1])                  # Rows 0 and 1 (inclusive!)
print(df.loc[0, "name"])            # Single value
print(df.loc[:, "name"])            # All rows, "name" column
print(df.loc[0:1, ["name", "age"]]) # Rows 0-1, specific columns

# iloc - integer position-based indexing
print(df.iloc[0])                   # First row
print(df.iloc[0:2])                 # Rows 0 and 1 (exclusive end!)
print(df.iloc[0, 0])               # First row, first column
print(df.iloc[:, 0:2])             # All rows, first 2 columns

# Boolean indexing
print(df[df["age"] > 25])
print(df[(df["age"] > 25) & (df["salary"] > 80000)])
print(df[df["name"].isin(["Alice", "Charlie"])])
print(df[df["name"].str.contains("li")])

# query method (string expression)
print(df.query("age > 25 and salary > 80000"))
```

### Setting Values

```python
# Set a column
df["bonus"] = df["salary"] * 0.1
df["department"] = "Engineering"

# Set specific values
df.loc[0, "salary"] = 72000
df.loc[df["age"] > 30, "bonus"] = 15000

# Conditional assignment
df["seniority"] = np.where(df["age"] >= 30, "Senior", "Junior")
```

---

## Data Cleaning

### Missing Values

```python
df = pd.DataFrame({
    "name": ["Alice", "Bob", None, "Diana"],
    "age": [25, None, 35, 28],
    "score": [90, 85, None, None]
})

# Detect missing values
print(df.isna())         # Boolean mask of NaN values
print(df.isna().sum())   # Count NaNs per column
print(df.notna())        # Opposite of isna

# Drop missing values
print(df.dropna())                  # Drop rows with any NaN
print(df.dropna(subset=["name"]))   # Only check specific columns
print(df.dropna(thresh=2))          # Keep rows with at least 2 non-NaN

# Fill missing values
print(df.fillna(0))                 # Fill with constant
print(df.fillna({"age": df["age"].mean(), "score": 0}))  # Per-column fill
print(df["age"].fillna(method="ffill"))  # Forward fill
print(df["age"].fillna(method="bfill"))  # Backward fill
print(df["score"].interpolate())          # Linear interpolation
```

### Duplicates

```python
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Alice", "Charlie"],
    "age": [25, 30, 25, 35]
})

print(df.duplicated())                    # Boolean mask
print(df.duplicated(subset=["name"]))     # Check specific columns
print(df.drop_duplicates())               # Remove duplicates
print(df.drop_duplicates(subset=["name"], keep="last"))  # Keep last occurrence
```

### Type Conversion

```python
df = pd.DataFrame({
    "price": ["10.5", "20.3", "30.1"],
    "quantity": ["1", "2", "3"],
    "date": ["2024-01-01", "2024-02-01", "2024-03-01"]
})

df["price"] = df["price"].astype(float)
df["quantity"] = pd.to_numeric(df["quantity"])
df["date"] = pd.to_datetime(df["date"])

print(df.dtypes)

# Handle conversion errors
df["mixed"] = ["1", "2", "bad"]
df["mixed_numeric"] = pd.to_numeric(df["mixed"], errors="coerce")  # NaN for bad values
```

### Renaming and Reordering

```python
# Rename columns
df = df.rename(columns={"price": "unit_price", "quantity": "qty"})
df.columns = ["a", "b", "c"]  # Rename all at once

# Reorder columns
df = df[["c", "a", "b"]]

# Reset index
df = df.reset_index(drop=True)

# Set a column as index
df = df.set_index("a")
```

---

## Data Transformation

### Apply and Map

```python
df = pd.DataFrame({
    "name": ["alice", "bob", "charlie"],
    "score": [85, 92, 78]
})

# apply - apply function to each element, row, or column
df["name"] = df["name"].apply(str.title)           # Element-wise on Series
df["grade"] = df["score"].apply(lambda x: "A" if x >= 90 else "B" if x >= 80 else "C")

# apply on rows
df["summary"] = df.apply(lambda row: f"{row['name']}: {row['score']}", axis=1)

# map - element-wise transformation on Series
grade_map = {85: "B", 92: "A", 78: "C"}
df["grade2"] = df["score"].map(grade_map)

# replace
df["name"] = df["name"].replace({"Alice": "ALICE", "Bob": "BOB"})

# String methods
df["name_upper"] = df["name"].str.upper()
df["name_len"] = df["name"].str.len()
df["first_letter"] = df["name"].str[0]
```

### Sorting

```python
df = pd.DataFrame({
    "name": ["Charlie", "Alice", "Bob"],
    "age": [35, 25, 30],
    "salary": [90000, 70000, 85000]
})

# Sort by column
print(df.sort_values("age"))
print(df.sort_values("salary", ascending=False))
print(df.sort_values(["age", "salary"], ascending=[True, False]))

# Sort by index
print(df.sort_index())

# Rank
df["salary_rank"] = df["salary"].rank(ascending=False)
```

### Adding and Removing Columns

```python
# Add columns
df["tax"] = df["salary"] * 0.3
df["net"] = df["salary"] - df["tax"]

# Insert at specific position
df.insert(2, "department", "Engineering")

# Drop columns
df = df.drop(columns=["tax", "net"])
# or
df = df.drop(["tax", "net"], axis=1)

# Drop rows
df = df.drop(index=[0, 2])
```

---

## Grouping and Aggregation

### GroupBy

```python
df = pd.DataFrame({
    "department": ["Sales", "Sales", "Engineering", "Engineering", "HR"],
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "salary": [70000, 75000, 90000, 85000, 65000],
    "years": [3, 5, 7, 4, 2]
})

# Group and aggregate
grouped = df.groupby("department")

# Single aggregation
print(grouped["salary"].mean())
# department
# Engineering    87500.0
# HR             65000.0
# Sales          72500.0

# Multiple aggregations
print(grouped["salary"].agg(["mean", "min", "max", "count"]))

# Different aggregations per column
print(grouped.agg({
    "salary": ["mean", "sum"],
    "years": "max"
}))

# Named aggregation (cleaner output)
result = grouped.agg(
    avg_salary=("salary", "mean"),
    total_salary=("salary", "sum"),
    max_years=("years", "max"),
    headcount=("name", "count")
)
print(result)
```

### Transform and Filter

```python
# transform - returns same-sized output
df["dept_avg_salary"] = df.groupby("department")["salary"].transform("mean")
df["salary_vs_dept"] = df["salary"] - df["dept_avg_salary"]

# filter - keep/drop entire groups
high_salary_depts = df.groupby("department").filter(lambda g: g["salary"].mean() > 70000)
print(high_salary_depts)
```

### Pivot Tables and Cross-tabs

```python
df = pd.DataFrame({
    "date": ["2024-01", "2024-01", "2024-02", "2024-02"],
    "product": ["A", "B", "A", "B"],
    "sales": [100, 150, 120, 180],
    "quantity": [10, 15, 12, 18]
})

# Pivot table
pivot = pd.pivot_table(df, values="sales", index="date", columns="product", aggfunc="sum")
print(pivot)
# product      A    B
# date
# 2024-01    100  150
# 2024-02    120  180

# Cross-tabulation
ct = pd.crosstab(df["date"], df["product"], values=df["sales"], aggfunc="sum")
print(ct)
```

---

## Merging and Joining

```python
# Sample DataFrames
employees = pd.DataFrame({
    "emp_id": [1, 2, 3, 4],
    "name": ["Alice", "Bob", "Charlie", "Diana"],
    "dept_id": [10, 20, 10, 30]
})

departments = pd.DataFrame({
    "dept_id": [10, 20, 40],
    "dept_name": ["Engineering", "Marketing", "HR"]
})

# Inner join (only matching rows)
merged = pd.merge(employees, departments, on="dept_id", how="inner")
print(merged)
#    emp_id     name  dept_id    dept_name
# 0       1    Alice       10  Engineering
# 1       3  Charlie       10  Engineering
# 2       2      Bob       20    Marketing

# Left join (all left rows)
merged = pd.merge(employees, departments, on="dept_id", how="left")

# Right join (all right rows)
merged = pd.merge(employees, departments, on="dept_id", how="right")

# Outer join (all rows from both)
merged = pd.merge(employees, departments, on="dept_id", how="outer")

# Join on different column names
salaries = pd.DataFrame({"id": [1, 2, 3], "salary": [70000, 85000, 90000]})
merged = pd.merge(employees, salaries, left_on="emp_id", right_on="id")

# Concatenate (stack)
df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df2 = pd.DataFrame({"A": [5, 6], "B": [7, 8]})
stacked = pd.concat([df1, df2], ignore_index=True)
print(stacked)
# Side by side
side = pd.concat([df1, df2], axis=1)
```

---

## Time Series

```python
# Date ranges
dates = pd.date_range("2024-01-01", periods=6, freq="M")
print(dates)

# Time series DataFrame
ts = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=365, freq="D"),
    "value": np.random.randn(365).cumsum()
})
ts = ts.set_index("date")

# Accessing components
print(ts.index.year)
print(ts.index.month)
print(ts.index.day_name())

# Slicing by date
print(ts["2024-03"])           # All of March
print(ts["2024-01":"2024-03"]) # Jan through March

# Resampling
print(ts.resample("W").mean())    # Weekly average
print(ts.resample("M").sum())     # Monthly sum
print(ts.resample("Q").last())    # Quarterly last value

# Rolling window
print(ts.rolling(window=7).mean())    # 7-day moving average
print(ts.rolling(window=30).std())    # 30-day rolling std

# Shifting
ts["lag_1"] = ts["value"].shift(1)    # Previous day
ts["lead_1"] = ts["value"].shift(-1)  # Next day
ts["pct_change"] = ts["value"].pct_change()  # Percent change

# Frequency aliases:
# D=daily, W=weekly, M=month end, MS=month start,
# Q=quarter end, Y=year end, H=hourly, min=minutely
```

---

## Visualization

```python
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "x": range(10),
    "y": np.random.randn(10).cumsum(),
    "category": ["A", "B"] * 5
})

# Line plot
df.plot(x="x", y="y", kind="line", title="Line Plot")
plt.show()

# Bar plot
df.groupby("category")["y"].mean().plot(kind="bar", title="Mean by Category")
plt.show()

# Histogram
df["y"].plot(kind="hist", bins=10, title="Distribution")
plt.show()

# Box plot
df.plot(kind="box", title="Box Plot")
plt.show()

# Scatter plot
df.plot(kind="scatter", x="x", y="y", title="Scatter Plot")
plt.show()

# Multiple plots
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
df["y"].plot(ax=axes[0], title="Line")
df["y"].plot(kind="hist", ax=axes[1], title="Histogram")
plt.tight_layout()
plt.show()
```

---

## Performance Tips

```python
# 1. Use appropriate dtypes
df["category"] = df["category"].astype("category")  # Saves memory for repeated strings
df["id"] = df["id"].astype("int32")                  # Use smaller int if possible

# 2. Read only needed columns
df = pd.read_csv("big_file.csv", usecols=["col1", "col2"])

# 3. Use chunked reading for large files
for chunk in pd.read_csv("huge_file.csv", chunksize=10000):
    process(chunk)

# 4. Vectorize instead of iterrows
# Bad
for idx, row in df.iterrows():
    df.loc[idx, "new_col"] = row["col1"] * 2

# Good
df["new_col"] = df["col1"] * 2

# 5. Use query() for complex filters (can be faster)
df.query("age > 25 and salary > 80000")

# 6. Use Parquet for storage (faster read/write, smaller files)
df.to_parquet("data.parquet")
df = pd.read_parquet("data.parquet")

# 7. Check memory usage
print(df.memory_usage(deep=True))
print(df.info(memory_usage="deep"))
```

---

## Practice Exercises

### Exercise 1: Sales Analysis

```python
# Create sample sales data
rng = np.random.default_rng(42)
n = 100
sales = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=n, freq="D"),
    "product": rng.choice(["Widget", "Gadget", "Doohickey"], n),
    "region": rng.choice(["North", "South", "East", "West"], n),
    "quantity": rng.integers(1, 50, n),
    "price": rng.uniform(10, 100, n).round(2)
})
sales["revenue"] = sales["quantity"] * sales["price"]

# Top product by total revenue
top = sales.groupby("product")["revenue"].sum().idxmax()
print(f"Top product: {top}")

# Average daily revenue by region
daily_by_region = sales.groupby("region")["revenue"].mean()
print(daily_by_region.round(2))

# Monthly trend
sales = sales.set_index("date")
monthly = sales.resample("M")["revenue"].sum()
print(monthly)
```

### Exercise 2: Data Cleaning Pipeline

```python
# Messy data
messy = pd.DataFrame({
    "Name": ["  alice ", "BOB", "charlie", "  alice ", "diana"],
    "Age": ["25", "thirty", "35", "25", "28"],
    "Score": [90, 85, None, 90, 75]
})

# Clean it
clean = (messy
    .assign(Name=lambda d: d["Name"].str.strip().str.title())
    .assign(Age=lambda d: pd.to_numeric(d["Age"], errors="coerce"))
    .dropna(subset=["Age"])
    .drop_duplicates()
    .fillna({"Score": lambda d: d["Score"].median()})
    .sort_values("Name")
    .reset_index(drop=True)
)
print(clean)
```

---

## Summary

These notes cover the fundamental concepts of Pandas:

1. **Data Structures**: Series (1D) and DataFrame (2D) with labeled axes
2. **I/O**: Read/write CSV, Excel, JSON, Parquet, SQL with extensive options
3. **Selection**: Column access, `loc` (label), `iloc` (position), boolean indexing, `query()`
4. **Cleaning**: Missing values (`isna`, `fillna`, `dropna`), duplicates, type conversion
5. **Transformation**: `apply`, `map`, string methods, sorting, adding/dropping columns
6. **Grouping**: `groupby` with `agg`, `transform`, `filter`; pivot tables
7. **Merging**: `merge` (inner/left/right/outer joins), `concat` (stacking)
8. **Time Series**: Date ranges, resampling, rolling windows, shifting
9. **Visualization**: Built-in plotting via Matplotlib integration
10. **Performance**: Appropriate dtypes, vectorization, chunked reading, Parquet format

### Next Steps

1. Practice with real-world datasets (Kaggle, UCI ML Repository)
2. Learn Matplotlib and Seaborn for advanced visualization
3. Explore method chaining with `pipe()` for clean data pipelines
4. Study MultiIndex for hierarchical indexing
5. Learn about `pandas.eval()` and `query()` for optimized expressions

### Additional Resources

- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Pandas User Guide**: https://pandas.pydata.org/docs/user_guide/
- **10 Minutes to Pandas**: https://pandas.pydata.org/docs/user_guide/10min.html
- **Modern Pandas**: https://tomaugspurger.net/posts/modern-1-intro/
