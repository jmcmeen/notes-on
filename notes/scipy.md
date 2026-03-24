# Introduction to SciPy

## Table of Contents

1. [What is SciPy?](#what-is-scipy)
2. [Installation and Setup](#installation-and-setup)
3. [Statistical Functions](#statistical-functions)
4. [Optimization](#optimization)
5. [Interpolation](#interpolation)
6. [Integration](#integration)
7. [Linear Algebra](#linear-algebra)
8. [Signal Processing](#signal-processing)
9. [Spatial Data](#spatial-data)
10. [Sparse Matrices](#sparse-matrices)
11. [Practice Exercises](#practice-exercises)
12. [Summary](#summary)

---

## What is SciPy?

SciPy (Scientific Python) builds on NumPy to provide a collection of algorithms and functions for scientific computing:
- **scipy.stats**: Statistical distributions, tests, and descriptive statistics
- **scipy.optimize**: Minimization, curve fitting, root finding
- **scipy.interpolate**: Interpolation of 1D and multi-dimensional data
- **scipy.integrate**: Numerical integration and ODE solvers
- **scipy.linalg**: Extended linear algebra (beyond NumPy)
- **scipy.signal**: Signal processing (filtering, spectral analysis)
- **scipy.spatial**: Spatial data structures (KD-trees, distance computations)
- **scipy.sparse**: Sparse matrix representations and algorithms

---

## Installation and Setup

```bash
pip install scipy
```

```python
import numpy as np
from scipy import stats, optimize, interpolate, integrate, linalg, signal, spatial, sparse

print(scipy.__version__)
```

---

## Statistical Functions

### Descriptive Statistics

```python
from scipy import stats
import numpy as np

data = np.random.default_rng(42).normal(loc=50, scale=10, size=1000)

# Descriptive statistics
print(f"Mean:     {np.mean(data):.2f}")
print(f"Median:   {np.median(data):.2f}")
print(f"Mode:     {stats.mode(data.round(), keepdims=True).mode[0]:.0f}")
print(f"Skewness: {stats.skew(data):.4f}")
print(f"Kurtosis: {stats.kurtosis(data):.4f}")
print(f"SEM:      {stats.sem(data):.4f}")

# Comprehensive description
result = stats.describe(data)
print(f"N:        {result.nobs}")
print(f"Min/Max:  {result.minmax}")
print(f"Variance: {result.variance:.4f}")
```

### Probability Distributions

```python
from scipy import stats

# Normal distribution
norm = stats.norm(loc=0, scale=1)  # mean=0, std=1

# PDF (Probability Density Function)
print(f"PDF at 0: {norm.pdf(0):.4f}")       # 0.3989

# CDF (Cumulative Distribution Function)
print(f"CDF at 0: {norm.cdf(0):.4f}")       # 0.5000
print(f"P(X < 1.96): {norm.cdf(1.96):.4f}") # 0.9750

# Inverse CDF (Percent Point Function)
print(f"95th percentile: {norm.ppf(0.95):.4f}")  # 1.6449

# Random samples
samples = norm.rvs(size=1000, random_state=42)

# Fit distribution to data
mu, sigma = stats.norm.fit(samples)
print(f"Fitted: mu={mu:.4f}, sigma={sigma:.4f}")

# Other distributions
t_dist = stats.t(df=10)            # Student's t
chi2 = stats.chi2(df=5)            # Chi-squared
poisson = stats.poisson(mu=5)       # Poisson
binom = stats.binom(n=10, p=0.5)   # Binomial
uniform = stats.uniform(loc=0, scale=10)  # Uniform [0, 10]
```

### Statistical Tests

```python
from scipy import stats
import numpy as np

rng = np.random.default_rng(42)

# t-test (compare means)
group_a = rng.normal(50, 10, 100)
group_b = rng.normal(55, 10, 100)

# Independent two-sample t-test
t_stat, p_value = stats.ttest_ind(group_a, group_b)
print(f"t-statistic: {t_stat:.4f}, p-value: {p_value:.4f}")

# One-sample t-test (compare to known mean)
t_stat, p_value = stats.ttest_1samp(group_a, 50)
print(f"t-statistic: {t_stat:.4f}, p-value: {p_value:.4f}")

# Paired t-test
before = rng.normal(50, 10, 30)
after = before + rng.normal(5, 3, 30)
t_stat, p_value = stats.ttest_rel(before, after)
print(f"Paired t: {t_stat:.4f}, p-value: {p_value:.4f}")

# Mann-Whitney U test (non-parametric)
u_stat, p_value = stats.mannwhitneyu(group_a, group_b)
print(f"U-statistic: {u_stat:.4f}, p-value: {p_value:.4f}")

# Chi-squared test of independence
observed = np.array([[30, 10], [20, 40]])
chi2, p_value, dof, expected = stats.chi2_contingency(observed)
print(f"Chi2: {chi2:.4f}, p-value: {p_value:.4f}")

# Normality test (Shapiro-Wilk)
stat, p_value = stats.shapiro(group_a[:50])
print(f"Shapiro-Wilk: stat={stat:.4f}, p-value={p_value:.4f}")

# Correlation
x = rng.normal(0, 1, 100)
y = 2 * x + rng.normal(0, 0.5, 100)

# Pearson (linear correlation)
r, p = stats.pearsonr(x, y)
print(f"Pearson r: {r:.4f}, p-value: {p:.4f}")

# Spearman (rank correlation)
rho, p = stats.spearmanr(x, y)
print(f"Spearman rho: {rho:.4f}, p-value: {p:.4f}")
```

---

## Optimization

### Minimization

```python
from scipy import optimize
import numpy as np

# Minimize a scalar function
def f(x):
    return (x - 3) ** 2 + 1

result = optimize.minimize_scalar(f)
print(f"Minimum at x={result.x:.4f}, f(x)={result.fun:.4f}")
# x=3.0, f(x)=1.0

# Minimize a multivariate function
def rosenbrock(x):
    return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

result = optimize.minimize(rosenbrock, x0=[0, 0], method="Nelder-Mead")
print(f"Minimum at: {result.x}")    # [1. 1.]
print(f"Value: {result.fun:.6f}")   # ~0.0
print(f"Success: {result.success}")

# With gradient (faster convergence)
def rosenbrock_grad(x):
    return np.array([
        -2 * (1 - x[0]) - 400 * x[0] * (x[1] - x[0]**2),
        200 * (x[1] - x[0]**2)
    ])

result = optimize.minimize(rosenbrock, x0=[0, 0], jac=rosenbrock_grad, method="BFGS")
print(f"Minimum at: {result.x}")

# Constrained optimization
result = optimize.minimize(
    lambda x: x[0]**2 + x[1]**2,
    x0=[1, 1],
    constraints={"type": "eq", "fun": lambda x: x[0] + x[1] - 1},
    bounds=[(0, None), (0, None)]
)
print(f"Constrained min: {result.x}")  # [0.5, 0.5]
```

### Curve Fitting

```python
from scipy import optimize
import numpy as np

# Generate noisy data
rng = np.random.default_rng(42)
x_data = np.linspace(0, 10, 50)
y_data = 3 * np.sin(2 * x_data) + rng.normal(0, 0.5, 50)

# Define model function
def model(x, a, b):
    return a * np.sin(b * x)

# Fit
params, covariance = optimize.curve_fit(model, x_data, y_data, p0=[1, 1])
print(f"Fitted parameters: a={params[0]:.4f}, b={params[1]:.4f}")
# a≈3.0, b≈2.0

# Parameter uncertainties (1 standard deviation)
errors = np.sqrt(np.diag(covariance))
print(f"Uncertainties: a±{errors[0]:.4f}, b±{errors[1]:.4f}")

# Predicted values
y_pred = model(x_data, *params)
```

### Root Finding

```python
from scipy import optimize
import numpy as np

# Find root of f(x) = 0
def f(x):
    return x**3 - 2*x - 5

# Brentq (bracketing method, guaranteed convergence)
root = optimize.brentq(f, 1, 3)
print(f"Root: {root:.6f}")  # 2.094552

# fsolve (Newton-type, for systems of equations)
root = optimize.fsolve(f, x0=2)
print(f"Root: {root[0]:.6f}")

# System of equations
def system(vars):
    x, y = vars
    return [x + y - 3, x**2 + y**2 - 5]

solution = optimize.fsolve(system, x0=[1, 1])
print(f"Solution: x={solution[0]:.4f}, y={solution[1]:.4f}")
```

---

## Interpolation

```python
from scipy import interpolate
import numpy as np

# Sample data points
x = np.array([0, 1, 2, 3, 4, 5])
y = np.array([0, 0.8, 0.9, 0.1, -0.8, -1.0])

# Linear interpolation
f_linear = interpolate.interp1d(x, y, kind="linear")

# Cubic interpolation (smooth)
f_cubic = interpolate.interp1d(x, y, kind="cubic")

# Evaluate at new points
x_new = np.linspace(0, 5, 50)
y_linear = f_linear(x_new)
y_cubic = f_cubic(x_new)

# Cubic spline (more control)
cs = interpolate.CubicSpline(x, y)
y_spline = cs(x_new)
y_derivative = cs(x_new, 1)  # First derivative

# 2D interpolation
from scipy.interpolate import griddata

# Scattered data
points = np.random.rand(100, 2)
values = np.sin(points[:, 0] * np.pi) * np.cos(points[:, 1] * np.pi)

# Create regular grid
grid_x, grid_y = np.mgrid[0:1:50j, 0:1:50j]
grid_values = griddata(points, values, (grid_x, grid_y), method="cubic")
```

---

## Integration

```python
from scipy import integrate
import numpy as np

# Definite integral of f(x) from a to b
def f(x):
    return np.sin(x) ** 2

result, error = integrate.quad(f, 0, np.pi)
print(f"∫sin²(x)dx from 0 to π = {result:.6f} (error: {error:.2e})")
# = π/2 ≈ 1.570796

# Double integral
def f2d(y, x):  # Note: y first, then x
    return x * y

result, error = integrate.dblquad(f2d, 0, 1, 0, 1)
print(f"∫∫xy dydx = {result:.6f}")  # 0.25

# Integral from data points (trapezoidal rule)
x = np.linspace(0, np.pi, 100)
y = np.sin(x)
result = integrate.trapezoid(y, x)
print(f"Trapezoid: {result:.6f}")  # ≈ 2.0

# Simpson's rule (more accurate)
result = integrate.simpson(y, x=x)
print(f"Simpson: {result:.6f}")

# ODE solver
from scipy.integrate import solve_ivp

# dy/dt = -2y, y(0) = 1  (solution: y = e^(-2t))
def ode(t, y):
    return -2 * y

sol = solve_ivp(ode, t_span=[0, 5], y0=[1], t_eval=np.linspace(0, 5, 50))
print(f"y(5) = {sol.y[0, -1]:.6f}")  # ≈ e^(-10) ≈ 0.0000454

# System of ODEs (Lotka-Volterra / predator-prey)
def lotka_volterra(t, y, a=1.0, b=0.1, c=1.5, d=0.075):
    prey, predator = y
    dprey = a * prey - b * prey * predator
    dpredator = -c * predator + d * prey * predator
    return [dprey, dpredator]

sol = solve_ivp(lotka_volterra, [0, 30], [10, 5], t_eval=np.linspace(0, 30, 300))
# sol.t = time points, sol.y[0] = prey, sol.y[1] = predator
```

---

## Linear Algebra

```python
from scipy import linalg
import numpy as np

A = np.array([[1, 2], [3, 4]])

# Determinant and inverse (same as NumPy but can be faster)
print(f"Det: {linalg.det(A):.4f}")
print(f"Inv:\n{linalg.inv(A)}")

# LU decomposition
P, L, U = linalg.lu(A)
print(f"P:\n{P}\nL:\n{L}\nU:\n{U}")

# Cholesky decomposition (for positive definite matrices)
B = np.array([[4, 2], [2, 3]])
L = linalg.cholesky(B, lower=True)
print(f"Cholesky L:\n{L}")

# QR decomposition
Q, R = linalg.qr(A)
print(f"Q:\n{Q}\nR:\n{R}")

# SVD
U, S, Vt = linalg.svd(A)
print(f"Singular values: {S}")

# Solve Ax = b
b = np.array([5, 11])
x = linalg.solve(A, b)
print(f"Solution: {x}")

# Least squares (overdetermined systems)
A_over = np.array([[1, 1], [2, 1], [3, 1]])
b_over = np.array([2.1, 3.9, 6.2])
result = linalg.lstsq(A_over, b_over)
print(f"Least squares: {result[0]}")  # Slope and intercept

# Matrix exponential
print(f"expm(A):\n{linalg.expm(A)}")

# Eigenvalues (generalized)
eigenvalues, eigenvectors = linalg.eig(A)
print(f"Eigenvalues: {eigenvalues}")
```

---

## Signal Processing

```python
from scipy import signal
import numpy as np

# Create a noisy signal
t = np.linspace(0, 1, 1000, endpoint=False)
clean = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 50 * t)
rng = np.random.default_rng(42)
noisy = clean + rng.normal(0, 0.5, len(t))

# Butterworth low-pass filter
b, a = signal.butter(N=4, Wn=10, fs=1000, btype="low")
filtered = signal.filtfilt(b, a, noisy)

# Find peaks
peaks, properties = signal.find_peaks(filtered, height=0.5, distance=50)
print(f"Found {len(peaks)} peaks")

# FFT (frequency analysis)
from scipy.fft import fft, fftfreq

N = len(t)
yf = fft(noisy)
xf = fftfreq(N, 1/1000)

# Power spectrum (positive frequencies only)
power = 2.0/N * np.abs(yf[:N//2])
freqs = xf[:N//2]

# Spectrogram
f, t_spec, Sxx = signal.spectrogram(noisy, fs=1000)

# Convolution
kernel = np.ones(10) / 10  # Moving average
smoothed = signal.convolve(noisy, kernel, mode="same")

# Welch's method (power spectral density)
f_welch, Pxx = signal.welch(noisy, fs=1000, nperseg=256)
```

---

## Spatial Data

```python
from scipy import spatial
import numpy as np

# KD-Tree (fast nearest neighbor queries)
points = np.random.default_rng(42).random((100, 2))
tree = spatial.KDTree(points)

# Find nearest neighbor
query = np.array([0.5, 0.5])
dist, idx = tree.query(query)
print(f"Nearest point: {points[idx]}, distance: {dist:.4f}")

# Find k nearest neighbors
dists, idxs = tree.query(query, k=5)
print(f"5 nearest distances: {dists}")

# Find all points within radius
idxs = tree.query_ball_point(query, r=0.1)
print(f"Points within r=0.1: {len(idxs)}")

# Distance matrix
from scipy.spatial import distance

# Pairwise distances
pts = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
dist_matrix = distance.cdist(pts, pts, metric="euclidean")
print(f"Distance matrix:\n{dist_matrix.round(3)}")

# Condensed distance matrix (for clustering)
condensed = distance.pdist(pts, metric="euclidean")
square = distance.squareform(condensed)

# Other metrics: cityblock, cosine, correlation, minkowski

# Convex hull
hull = spatial.ConvexHull(points)
print(f"Hull vertices: {hull.vertices}")
print(f"Hull area: {hull.volume:.4f}")  # .volume is area in 2D

# Delaunay triangulation
tri = spatial.Delaunay(points)
print(f"Number of triangles: {len(tri.simplices)}")

# Voronoi diagram
vor = spatial.Voronoi(points)
print(f"Number of regions: {len(vor.regions)}")
```

---

## Sparse Matrices

```python
from scipy import sparse
import numpy as np

# Create sparse matrices
# CSR (Compressed Sparse Row) - efficient for row operations
row = [0, 0, 1, 2, 2]
col = [0, 2, 1, 0, 2]
data = [1, 3, 4, 5, 6]
csr = sparse.csr_matrix((data, (row, col)), shape=(3, 3))
print(csr.toarray())
# [[1 0 3]
#  [0 4 0]
#  [5 0 6]]

# From dense array
dense = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
sp = sparse.csr_matrix(dense)

# Identity and diagonal
eye = sparse.eye(5)
diag = sparse.diags([1, 2, 3, 4, 5])

# Random sparse matrix
random_sp = sparse.random(100, 100, density=0.05, random_state=42)
print(f"Non-zero elements: {random_sp.nnz}")
print(f"Density: {random_sp.nnz / (100*100):.2%}")

# Operations
A = sparse.random(1000, 1000, density=0.01, format="csr")
B = sparse.random(1000, 1000, density=0.01, format="csr")

C = A + B           # Addition
D = A @ B           # Matrix multiply
E = A.multiply(B)   # Element-wise multiply

# Solve sparse linear system
from scipy.sparse.linalg import spsolve
b = np.ones(1000)
x = spsolve(A + sparse.eye(1000), b)

# Eigenvalues of sparse matrix
from scipy.sparse.linalg import eigs
eigenvalues, eigenvectors = eigs(A, k=5)  # Top 5 eigenvalues
print(f"Top eigenvalues: {eigenvalues}")

# Convert between formats
csc = csr.tocsc()  # CSC (Compressed Sparse Column)
coo = csr.tocoo()  # COO (Coordinate format)
dense = csr.toarray()
```

---

## Practice Exercises

### Exercise 1: Distribution Fitting

```python
from scipy import stats
import numpy as np

# Generate mystery data
rng = np.random.default_rng(42)
data = np.concatenate([rng.normal(30, 5, 500), rng.normal(60, 8, 500)])

# Test if normally distributed
stat, p = stats.shapiro(data[:500])
print(f"Shapiro-Wilk: p={p:.4f} ({'Normal' if p > 0.05 else 'Not normal'})")

# Fit a normal distribution
mu, sigma = stats.norm.fit(data)
print(f"Normal fit: mu={mu:.2f}, sigma={sigma:.2f}")

# Kolmogorov-Smirnov test
ks_stat, ks_p = stats.kstest(data, "norm", args=(mu, sigma))
print(f"KS test: statistic={ks_stat:.4f}, p={ks_p:.4f}")
```

### Exercise 2: Curve Fitting

```python
from scipy import optimize
import numpy as np

# Exponential decay data
rng = np.random.default_rng(42)
t = np.linspace(0, 10, 50)
y_true = 5.0 * np.exp(-0.3 * t)
y_noisy = y_true + rng.normal(0, 0.2, len(t))

# Fit exponential model
def exp_decay(t, A, k):
    return A * np.exp(-k * t)

params, cov = optimize.curve_fit(exp_decay, t, y_noisy, p0=[1, 1])
print(f"A = {params[0]:.4f} (true: 5.0)")
print(f"k = {params[1]:.4f} (true: 0.3)")

# R-squared
y_pred = exp_decay(t, *params)
ss_res = np.sum((y_noisy - y_pred) ** 2)
ss_tot = np.sum((y_noisy - np.mean(y_noisy)) ** 2)
r_squared = 1 - ss_res / ss_tot
print(f"R² = {r_squared:.4f}")
```

---

## Summary

These notes cover the fundamental concepts of SciPy:

1. **Statistics**: Descriptive stats, distributions (PDF/CDF/PPF), hypothesis tests (t-test, chi-squared, Mann-Whitney), correlation
2. **Optimization**: Scalar and multivariate minimization, curve fitting (`curve_fit`), root finding (`brentq`, `fsolve`)
3. **Interpolation**: Linear, cubic, spline interpolation; 2D griddata
4. **Integration**: Definite integrals (`quad`), double integrals, trapezoidal/Simpson's rule, ODE solvers (`solve_ivp`)
5. **Linear Algebra**: Decompositions (LU, Cholesky, QR, SVD), least squares, matrix exponential
6. **Signal Processing**: Filtering (Butterworth), FFT, peak finding, spectrograms
7. **Spatial**: KD-trees, distance matrices, convex hulls, Delaunay triangulation, Voronoi diagrams
8. **Sparse Matrices**: CSR/CSC/COO formats, sparse solvers, sparse eigenvalues

### Next Steps

1. Apply statistical tests to real datasets
2. Use optimization for model fitting and parameter estimation
3. Explore `scipy.ndimage` for image processing
4. Combine with Matplotlib for visualizing results
5. Learn about `scipy.special` for special mathematical functions

### Additional Resources

- **SciPy Documentation**: https://docs.scipy.org/doc/scipy/
- **SciPy Lecture Notes**: https://scipy-lectures.org/
- **SciPy Cookbook**: https://scipy-cookbook.readthedocs.io/
- **SciPy Tutorial**: https://docs.scipy.org/doc/scipy/tutorial/
