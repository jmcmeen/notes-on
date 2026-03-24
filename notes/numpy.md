# Introduction to NumPy

## Table of Contents

1. [What is NumPy?](#what-is-numpy)
2. [Installation and Setup](#installation-and-setup)
3. [Creating Arrays](#creating-arrays)
4. [Array Properties](#array-properties)
5. [Indexing and Slicing](#indexing-and-slicing)
6. [Array Operations](#array-operations)
7. [Broadcasting](#broadcasting)
8. [Reshaping and Manipulating](#reshaping-and-manipulating)
9. [Mathematical Functions](#mathematical-functions)
10. [Linear Algebra](#linear-algebra)
11. [Random Numbers](#random-numbers)
12. [File I/O](#file-io)
13. [Performance Tips](#performance-tips)
14. [Practice Exercises](#practice-exercises)
15. [Summary](#summary)

---

## What is NumPy?

NumPy (Numerical Python) is the fundamental library for scientific computing in Python. It provides:
- **ndarray**: Fast, memory-efficient multi-dimensional array object
- **Vectorized operations**: Element-wise operations without Python loops
- **Broadcasting**: Rules for operations on arrays of different shapes
- **Linear algebra**: Matrix operations, decompositions, solvers
- **Random number generation**: Statistical distributions and sampling
- **C/Fortran integration**: Interface for compiled code
- **Foundation**: Underlies Pandas, SciPy, scikit-learn, TensorFlow, and more

---

## Installation and Setup

```bash
pip install numpy
```

```python
import numpy as np

print(np.__version__)
```

---

## Creating Arrays

### From Python Lists

```python
import numpy as np

# 1D array
a = np.array([1, 2, 3, 4, 5])
print(a)        # [1 2 3 4 5]
print(type(a))  # <class 'numpy.ndarray'>

# 2D array (matrix)
b = np.array([[1, 2, 3],
              [4, 5, 6]])
print(b)
# [[1 2 3]
#  [4 5 6]]

# Specifying data type
c = np.array([1, 2, 3], dtype=np.float64)
print(c)        # [1. 2. 3.]
print(c.dtype)  # float64
```

### Array Creation Functions

```python
# Zeros and ones
zeros = np.zeros((3, 4))         # 3x4 matrix of zeros
ones = np.ones((2, 3))           # 2x3 matrix of ones
full = np.full((2, 3), 7)        # 2x3 matrix filled with 7

# Identity matrix
eye = np.eye(3)                  # 3x3 identity matrix

# Ranges
arange = np.arange(0, 10, 2)    # [0, 2, 4, 6, 8] (start, stop, step)
linspace = np.linspace(0, 1, 5) # [0.  0.25 0.5  0.75 1.] (start, stop, num)
logspace = np.logspace(0, 3, 4) # [1. 10. 100. 1000.] (10^start to 10^stop)

# Empty (uninitialized, faster than zeros)
empty = np.empty((2, 3))        # Values are whatever is in memory

# Like existing arrays
a = np.array([1, 2, 3])
z = np.zeros_like(a)            # Same shape, filled with zeros
o = np.ones_like(a)             # Same shape, filled with ones

print(linspace)
```

---

## Array Properties

```python
a = np.array([[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12]])

print(a.ndim)     # 2 (number of dimensions)
print(a.shape)    # (3, 4) (rows, columns)
print(a.size)     # 12 (total number of elements)
print(a.dtype)    # int64 (data type)
print(a.itemsize) # 8 (bytes per element)
print(a.nbytes)   # 96 (total bytes = size * itemsize)

# Common data types
# np.int32, np.int64, np.float32, np.float64
# np.bool_, np.complex128, np.str_, np.object_

# Type conversion
b = a.astype(np.float32)
print(b.dtype)    # float32
```

---

## Indexing and Slicing

### 1D Indexing

```python
a = np.array([10, 20, 30, 40, 50])

# Basic indexing
print(a[0])       # 10
print(a[-1])      # 50
print(a[1:4])     # [20 30 40]
print(a[:3])      # [10 20 30]
print(a[::2])     # [10 30 50] (every other element)
print(a[::-1])    # [50 40 30 20 10] (reversed)

# Modify with indexing
a[0] = 99
a[1:3] = [88, 77]
print(a)          # [99 88 77 40 50]
```

### 2D Indexing

```python
a = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

# Single element
print(a[0, 0])     # 1
print(a[2, 1])     # 8

# Row and column slicing
print(a[0, :])     # [1 2 3] (first row)
print(a[:, 0])     # [1 4 7] (first column)
print(a[0:2, 1:3]) # [[2 3] [5 6]] (submatrix)

# Last row, last column
print(a[-1, :])    # [7 8 9]
print(a[:, -1])    # [3 6 9]
```

### Boolean and Fancy Indexing

```python
a = np.array([10, 20, 30, 40, 50])

# Boolean indexing (masking)
mask = a > 25
print(mask)          # [False False  True  True  True]
print(a[mask])       # [30 40 50]
print(a[a > 25])     # [30 40 50] (shorthand)

# Combine conditions
print(a[(a > 15) & (a < 45)])  # [20 30 40]
print(a[(a < 20) | (a > 40)])  # [10 50]

# Fancy indexing (index with arrays)
indices = np.array([0, 2, 4])
print(a[indices])    # [10 30 50]

# 2D fancy indexing
b = np.array([[1, 2], [3, 4], [5, 6]])
rows = np.array([0, 2])
cols = np.array([1, 0])
print(b[rows, cols])  # [2 5] (elements at (0,1) and (2,0))
```

### np.where

```python
a = np.array([1, -2, 3, -4, 5])

# np.where(condition, x, y) - returns x where True, y where False
result = np.where(a > 0, a, 0)
print(result)  # [1 0 3 0 5]

# Just get indices
indices = np.where(a > 0)
print(indices)  # (array([0, 2, 4]),)
print(a[indices])  # [1 3 5]
```

---

## Array Operations

### Element-wise Operations

```python
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

# Arithmetic (element-wise)
print(a + b)     # [11 22 33 44]
print(a - b)     # [-9 -18 -27 -36]
print(a * b)     # [10 40 90 160]
print(a / b)     # [0.1 0.1 0.1 0.1]
print(a ** 2)    # [1 4 9 16]
print(a % 2)     # [1 0 1 0]
print(a // 3)    # [0 0 1 1]

# Scalar operations
print(a + 10)    # [11 12 13 14]
print(a * 2)     # [2 4 6 8]

# Comparison (returns boolean array)
print(a > 2)     # [False False  True  True]
print(a == 3)    # [False False  True False]
```

### Aggregation Functions

```python
a = np.array([[1, 2, 3],
              [4, 5, 6]])

# Global aggregation
print(np.sum(a))       # 21
print(np.mean(a))      # 3.5
print(np.std(a))       # 1.707...
print(np.var(a))       # 2.916...
print(np.min(a))       # 1
print(np.max(a))       # 6
print(np.median(a))    # 3.5
print(np.prod(a))      # 720

# Along an axis
print(np.sum(a, axis=0))   # [5 7 9] (sum each column)
print(np.sum(a, axis=1))   # [6 15] (sum each row)
print(np.mean(a, axis=0))  # [2.5 3.5 4.5]
print(np.mean(a, axis=1))  # [2. 5.]

# Cumulative
print(np.cumsum(a))          # [ 1  3  6 10 15 21]
print(np.cumsum(a, axis=1))  # [[ 1  3  6] [ 4  9 15]]
print(np.cumprod(a, axis=1)) # [[ 1  2  6] [ 4 20 120]]

# Argmin / Argmax (index of min/max)
print(np.argmin(a))          # 0
print(np.argmax(a))          # 5
print(np.argmax(a, axis=0))  # [1 1 1] (row index of max per column)
```

---

## Broadcasting

Broadcasting allows operations on arrays with different shapes when certain rules are met.

```python
# Scalar broadcast
a = np.array([[1, 2, 3],
              [4, 5, 6]])
print(a + 10)
# [[11 12 13]
#  [14 15 16]]

# 1D broadcast across rows
row = np.array([10, 20, 30])
print(a + row)
# [[11 22 33]
#  [14 25 36]]

# 1D broadcast across columns (need column vector)
col = np.array([[100], [200]])
print(a + col)
# [[101 102 103]
#  [204 205 206]]

# Broadcasting rules:
# 1. Arrays are compared from trailing dimensions
# 2. Dimensions are compatible if equal or one of them is 1
# 3. Arrays with fewer dimensions are padded with 1s on the left

# Example: (3,4) + (4,) works because (4,) becomes (1,4) -> broadcasts to (3,4)
# Example: (3,4) + (3,1) works because (3,1) broadcasts to (3,4)
# Example: (3,4) + (3,) FAILS because trailing dimensions 4 != 3

# Practical: normalize columns to zero mean
data = np.array([[1.0, 200.0],
                 [2.0, 400.0],
                 [3.0, 600.0]])
means = data.mean(axis=0)       # [2. 400.]
normalized = data - means
print(normalized)
# [[-1. -200.]
#  [ 0.    0.]
#  [ 1.  200.]]
```

---

## Reshaping and Manipulating

### Reshaping

```python
a = np.arange(12)
print(a)  # [ 0  1  2  3  4  5  6  7  8  9 10 11]

# Reshape (total elements must match)
b = a.reshape(3, 4)
print(b)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# -1 means "infer this dimension"
c = a.reshape(2, -1)   # (2, 6)
d = a.reshape(-1, 3)   # (4, 3)

# Flatten (to 1D)
print(b.flatten())    # [ 0  1 ... 11] (returns copy)
print(b.ravel())      # [ 0  1 ... 11] (returns view when possible)

# Transpose
print(b.T)
# [[ 0  4  8]
#  [ 1  5  9]
#  [ 2  6 10]
#  [ 3  7 11]]

# Add/remove dimensions
e = np.array([1, 2, 3])
print(e.shape)                    # (3,)
print(e[np.newaxis, :].shape)    # (1, 3) - row vector
print(e[:, np.newaxis].shape)    # (3, 1) - column vector
print(np.expand_dims(e, 0).shape) # (1, 3)
print(np.squeeze(np.array([[[1, 2, 3]]])).shape)  # (3,) - remove size-1 dims
```

### Joining and Splitting

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Concatenate
print(np.concatenate([a, b]))       # [1 2 3 4 5 6]

# Stack
print(np.vstack([a, b]))            # [[1 2 3] [4 5 6]] (vertical)
print(np.hstack([a, b]))            # [1 2 3 4 5 6] (horizontal)
print(np.column_stack([a, b]))      # [[1 4] [2 5] [3 6]]

# 2D concatenate
c = np.array([[1, 2], [3, 4]])
d = np.array([[5, 6], [7, 8]])
print(np.concatenate([c, d], axis=0))  # Vertical: [[1,2],[3,4],[5,6],[7,8]]
print(np.concatenate([c, d], axis=1))  # Horizontal: [[1,2,5,6],[3,4,7,8]]

# Split
arr = np.arange(12)
print(np.split(arr, 3))            # [array([0,1,2,3]), array([4,5,6,7]), array([8,9,10,11])]
print(np.split(arr, [3, 7]))       # Split at indices 3 and 7
```

### Sorting

```python
a = np.array([3, 1, 4, 1, 5, 9, 2, 6])

# Sort (returns copy)
print(np.sort(a))              # [1 1 2 3 4 5 6 9]

# Sort in place
a.sort()

# Argsort (indices that would sort the array)
a = np.array([30, 10, 20])
indices = np.argsort(a)
print(indices)                 # [1 2 0]
print(a[indices])              # [10 20 30]

# Sort 2D
b = np.array([[3, 1], [2, 4]])
print(np.sort(b, axis=0))     # Sort each column: [[2,1],[3,4]]
print(np.sort(b, axis=1))     # Sort each row: [[1,3],[2,4]]
```

---

## Mathematical Functions

```python
a = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])

# Trigonometric
print(np.sin(a))
print(np.cos(a))
print(np.tan(a))

# Inverse trig
print(np.arcsin(np.array([0, 0.5, 1])))
print(np.arctan2(1, 1))  # atan2(y, x) = pi/4

# Exponential and logarithmic
b = np.array([1, 2, 3])
print(np.exp(b))          # [2.718  7.389  20.086]
print(np.log(b))          # Natural log: [0.  0.693  1.099]
print(np.log2(b))         # Base-2 log
print(np.log10(b))        # Base-10 log

# Rounding
c = np.array([1.4, 2.5, 3.6, -1.7])
print(np.round(c))        # [ 1.  2.  4. -2.]
print(np.floor(c))        # [ 1.  2.  3. -2.]
print(np.ceil(c))         # [ 2.  3.  4. -1.]
print(np.trunc(c))        # [ 1.  2.  3. -1.]

# Other useful functions
print(np.abs(np.array([-1, -2, 3])))  # [1 2 3]
print(np.sqrt(np.array([4, 9, 16])))  # [2. 3. 4.]
print(np.clip(b, 1.5, 2.5))           # [1.5 2.  2.5]
print(np.sign(np.array([-3, 0, 5])))  # [-1  0  1]
```

---

## Linear Algebra

```python
# Matrix multiplication
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

print(a @ b)                # Matrix multiply (Python 3.5+)
print(np.dot(a, b))         # Same thing
# [[19 22]
#  [43 50]]

# Dot product of 1D arrays
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])
print(np.dot(v1, v2))       # 32 (1*4 + 2*5 + 3*6)

# Transpose
print(a.T)

# Determinant
print(np.linalg.det(a))     # -2.0

# Inverse
print(np.linalg.inv(a))
# [[-2.   1. ]
#  [ 1.5 -0.5]]

# Eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(a)
print("Eigenvalues:", eigenvalues)
print("Eigenvectors:\n", eigenvectors)

# Solve linear system: ax = b
A = np.array([[2, 1], [1, 3]])
b = np.array([5, 10])
x = np.linalg.solve(A, b)
print("Solution:", x)        # [1. 3.]

# Norms
v = np.array([3, 4])
print(np.linalg.norm(v))     # 5.0 (L2 norm / Euclidean distance)
print(np.linalg.norm(v, 1))  # 7.0 (L1 norm / Manhattan distance)

# SVD (Singular Value Decomposition)
U, S, Vt = np.linalg.svd(a)
print("Singular values:", S)
```

---

## Random Numbers

```python
# Modern API (NumPy >= 1.17)
rng = np.random.default_rng(seed=42)

# Uniform distribution [0, 1)
print(rng.random(5))
print(rng.random((2, 3)))       # 2x3 matrix

# Uniform in range [low, high)
print(rng.uniform(0, 10, size=5))

# Normal (Gaussian) distribution
print(rng.normal(loc=0, scale=1, size=5))  # mean=0, std=1
print(rng.standard_normal(5))               # Same as above

# Integers
print(rng.integers(0, 10, size=5))          # [0, 10)
print(rng.integers(1, 7, size=(2, 3)))      # Dice rolls

# Choice (sampling)
arr = np.array([10, 20, 30, 40, 50])
print(rng.choice(arr, size=3, replace=False))  # Sample without replacement

# Shuffle
a = np.arange(10)
rng.shuffle(a)
print(a)

# Permutation (returns shuffled copy)
print(rng.permutation(10))

# Other distributions
print(rng.poisson(lam=5, size=5))       # Poisson
print(rng.binomial(n=10, p=0.5, size=5)) # Binomial
print(rng.exponential(scale=1.0, size=5)) # Exponential
```

---

## File I/O

```python
a = np.array([[1, 2, 3], [4, 5, 6]])

# Save/load binary format (.npy)
np.save("array.npy", a)
loaded = np.load("array.npy")
print(loaded)

# Save/load multiple arrays (.npz)
b = np.array([7, 8, 9])
np.savez("arrays.npz", first=a, second=b)
data = np.load("arrays.npz")
print(data["first"])
print(data["second"])

# Compressed
np.savez_compressed("arrays_compressed.npz", first=a, second=b)

# Save/load text format (CSV-like)
np.savetxt("array.csv", a, delimiter=",", fmt="%.2f", header="col1,col2,col3")
loaded_csv = np.loadtxt("array.csv", delimiter=",")
print(loaded_csv)

# Load with specific columns or rows
partial = np.loadtxt("array.csv", delimiter=",", usecols=(0, 2))

# Cleanup
import os
for f in ["array.npy", "arrays.npz", "arrays_compressed.npz", "array.csv"]:
    os.remove(f)
```

---

## Performance Tips

```python
import numpy as np

# 1. Vectorize - avoid Python loops
# Bad (slow)
a = np.arange(1000000)
result = np.empty_like(a)
for i in range(len(a)):
    result[i] = a[i] ** 2

# Good (fast)
result = a ** 2

# 2. Use in-place operations when possible
a = np.ones(1000000)
a += 1          # In-place (no new array allocated)
# vs
b = a + 1       # Allocates new array

# 3. Use appropriate dtypes
a = np.array([1, 2, 3], dtype=np.float32)  # 4 bytes vs 8 for float64

# 4. Preallocate arrays instead of growing them
# Bad
result = []
for i in range(1000):
    result.append(i ** 2)
result = np.array(result)

# Good
result = np.empty(1000)
for i in range(1000):
    result[i] = i ** 2

# 5. Use views instead of copies when possible
a = np.arange(10)
view = a[::2]      # View (shares memory)
copy = a[::2].copy()  # Copy (separate memory)

# Check if array is a view
print(view.base is a)   # True (it's a view)
print(copy.base is None) # True (it's a copy)

# 6. Use np.einsum for complex operations
a = np.random.rand(3, 4)
b = np.random.rand(4, 5)
c = np.einsum("ij,jk->ik", a, b)  # Matrix multiply
# Equivalent to a @ b but more flexible for complex tensor ops
```

---

## Practice Exercises

### Exercise 1: Statistics

```python
# Generate sample data and compute statistics
data = np.random.default_rng(42).normal(loc=50, scale=10, size=1000)

print(f"Mean:   {np.mean(data):.2f}")
print(f"Median: {np.median(data):.2f}")
print(f"Std:    {np.std(data):.2f}")
print(f"Min:    {np.min(data):.2f}")
print(f"Max:    {np.max(data):.2f}")

# Percentiles
print(f"25th:   {np.percentile(data, 25):.2f}")
print(f"75th:   {np.percentile(data, 75):.2f}")

# How many values within 1 std of mean?
within_1std = np.sum(np.abs(data - np.mean(data)) < np.std(data))
print(f"Within 1 std: {within_1std / len(data) * 100:.1f}%")
```

### Exercise 2: Image as Array

```python
# Simulate a grayscale image as a 2D array
rng = np.random.default_rng(42)
image = rng.integers(0, 256, size=(100, 100), dtype=np.uint8)

# Normalize to [0, 1]
normalized = image / 255.0
print(f"Range: [{normalized.min():.3f}, {normalized.max():.3f}]")

# Threshold (binary image)
binary = (image > 128).astype(np.uint8) * 255
print(f"White pixels: {np.sum(binary == 255)}")

# Flip horizontally
flipped = image[:, ::-1]

# Rotate 90 degrees
rotated = np.rot90(image)
print(f"Rotated shape: {rotated.shape}")
```

### Exercise 3: Distance Matrix

```python
# Compute pairwise Euclidean distances
points = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])

# Using broadcasting
diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]  # (4, 4, 2)
distances = np.sqrt(np.sum(diff ** 2, axis=2))               # (4, 4)

print("Distance matrix:")
print(np.round(distances, 3))
# [[0.    1.    1.    1.414]
#  [1.    0.    1.414 1.   ]
#  [1.    1.414 0.    1.   ]
#  [1.414 1.    1.    0.   ]]
```

---

## Summary

These notes cover the fundamental concepts of NumPy:

1. **Array Creation**: `np.array`, `zeros`, `ones`, `arange`, `linspace`, `empty`
2. **Properties**: `shape`, `dtype`, `ndim`, `size`, type conversion with `astype`
3. **Indexing**: Basic slicing, boolean masking, fancy indexing, `np.where`
4. **Operations**: Element-wise arithmetic, aggregations (`sum`, `mean`, `std`), axis parameter
5. **Broadcasting**: Rules for operating on arrays of different shapes
6. **Reshaping**: `reshape`, `flatten`, `ravel`, `transpose`, `concatenate`, `stack`, `split`
7. **Math**: Trig, exponential, logarithmic, rounding, clipping
8. **Linear Algebra**: Matrix multiply (`@`), `det`, `inv`, `eig`, `solve`, `svd`, norms
9. **Random**: `default_rng`, uniform, normal, integers, choice, shuffle
10. **I/O**: `save`/`load` (binary), `savetxt`/`loadtxt` (text)

### Next Steps

1. Practice with real datasets to build intuition for vectorized operations
2. Learn Pandas for labeled data and tabular analysis
3. Explore SciPy for advanced scientific computing
4. Study Matplotlib for visualizing NumPy arrays
5. Learn about memory layout (C vs Fortran order) and structured arrays

### Additional Resources

- **NumPy Documentation**: https://numpy.org/doc/stable/
- **NumPy User Guide**: https://numpy.org/doc/stable/user/
- **100 NumPy Exercises**: https://github.com/rougier/numpy-100
- **From Python to NumPy**: https://www.labri.fr/perso/nrougier/from-python-to-numpy/
