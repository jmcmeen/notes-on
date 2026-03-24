# Introduction to UMAP

## Table of Contents

1. [What is UMAP?](#what-is-umap)
2. [Installation and Setup](#installation-and-setup)
3. [Core Concepts](#core-concepts)
4. [Basic Usage](#basic-usage)
5. [Key Parameters](#key-parameters)
6. [Visualizing Results](#visualizing-results)
7. [Supervised and Semi-Supervised UMAP](#supervised-and-semi-supervised-umap)
8. [Working with Different Data Types](#working-with-different-data-types)
9. [Integration with scikit-learn](#integration-with-scikit-learn)
10. [Performance Tips](#performance-tips)
11. [Practice Exercises](#practice-exercises)
12. [Summary](#summary)

---

## What is UMAP?

UMAP (Uniform Manifold Approximation and Projection) is a dimensionality reduction technique that projects high-dimensional data into a lower-dimensional space while preserving both local and global structure:

- **Dimensionality Reduction**: Converts data with many features into 2D or 3D representations for visualization or downstream tasks
- **Manifold Learning**: Assumes high-dimensional data lies on a lower-dimensional manifold and attempts to recover that structure
- **Speed**: Significantly faster than t-SNE, especially on large datasets
- **Scalability**: Handles millions of data points with reasonable compute requirements
- **Versatility**: Works for visualization, clustering preprocessing, and general feature reduction

### How UMAP Compares to PCA and t-SNE

| Feature            | PCA              | t-SNE            | UMAP             |
|--------------------|------------------|------------------|-------------------|
| Method             | Linear           | Non-linear       | Non-linear        |
| Global structure   | Preserved well   | Poorly preserved | Better preserved  |
| Local structure    | May distort      | Excellent        | Excellent         |
| Speed              | Very fast        | Slow             | Fast              |
| Scalability        | Excellent        | Poor (>10k)      | Good (millions)   |
| New data transform | Yes              | No (re-fit)      | Yes               |
| Deterministic      | Yes              | No               | No                |

---

## Installation and Setup

```bash
# Install umap-learn (not "umap" which is a different package)
pip install umap-learn

# Optional: install pynndescent for faster approximate nearest neighbors
pip install pynndescent

# Common companion libraries
pip install scikit-learn matplotlib numpy pandas
```

```python
import umap
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits, load_iris
from sklearn.preprocessing import StandardScaler

print(umap.__version__)
```

---

## Core Concepts

### Manifold Learning Intuition

UMAP is built on the idea that high-dimensional data often lies on a lower-dimensional manifold — a curved surface embedded in the higher space. Think of a sheet of paper crumpled into a ball: the paper is 2D, but it exists in 3D space. UMAP tries to "unfold" the paper.

### Topological Data Analysis Foundation

UMAP works in two main phases:

1. **Build a weighted graph in high-dimensional space**: For each point, find its nearest neighbors and connect them with edges. Edge weights reflect how close points are relative to each point's local notion of distance.
2. **Optimize a low-dimensional layout**: Arrange points in 2D (or nD) so the graph structure is preserved as faithfully as possible, using cross-entropy as the cost function.

```python
# Conceptual overview of what UMAP does internally:

# Phase 1 — High-dimensional graph construction
# For each point x_i:
#   1. Find k nearest neighbors
#   2. Compute local distance scale (rho_i, sigma_i)
#   3. Build fuzzy simplicial set (weighted graph)

# Phase 2 — Low-dimensional optimization
# 1. Initialize layout (spectral embedding or random)
# 2. Minimize fuzzy set cross-entropy between
#    the high-dim graph and the low-dim graph
# 3. Uses stochastic gradient descent for efficiency
```

PCA only captures linear relationships and typically explains a small fraction of variance in 2D (e.g., ~28% for digits). UMAP reveals the non-linear cluster structure that PCA misses entirely.

---

## Basic Usage

### Fitting and Transforming

```python
import umap
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler

# Load data
digits = load_digits()
X, y = digits.data, digits.target

# Scale features to zero mean, unit variance (recommended)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Create and fit UMAP reducer
reducer = umap.UMAP(
    n_components=2,     # output dimensionality
    random_state=42     # for reproducibility
)

# fit_transform does fit + transform in one step
X_umap = reducer.fit_transform(X_scaled)

print(f"Input shape:  {X_scaled.shape}")    # (1797, 64)
print(f"Output shape: {X_umap.shape}")      # (1797, 2)
```

```
Input shape:  (1797, 64)
Output shape: (1797, 2)
```

### Separate Fit and Transform

```python
import umap
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.3, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)   # use training stats

# Fit on training data, then transform new data separately
reducer = umap.UMAP(n_components=2, random_state=42)
reducer.fit(X_train_scaled)

X_train_umap = reducer.transform(X_train_scaled)
X_test_umap = reducer.transform(X_test_scaled)  # project new data

print(f"Train embedding: {X_train_umap.shape}")  # (105, 2)
print(f"Test embedding:  {X_test_umap.shape}")    # (45, 2)
```

---

## Key Parameters

### n_neighbors (default: 15)

Controls how UMAP balances local vs. global structure. It determines how many neighbors each point considers when building the high-dimensional graph.

- **Low values (2-10)**: Focus on very local structure, captures fine detail, may fragment clusters
- **High values (50-200)**: Focus on global structure, broader view, may merge distinct clusters

```python
import umap
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

digits = load_digits()
X_scaled = StandardScaler().fit_transform(digits.data)

# Compare different n_neighbors values
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for ax, n in zip(axes, [5, 15, 100]):
    reducer = umap.UMAP(n_neighbors=n, random_state=42)
    embedding = reducer.fit_transform(X_scaled)
    ax.scatter(embedding[:, 0], embedding[:, 1],
               c=digits.target, cmap="Spectral", s=5, alpha=0.7)
    ax.set_title(f"n_neighbors={n}")
    ax.set_xlabel("UMAP 1")
    ax.set_ylabel("UMAP 2")
plt.tight_layout()
plt.show()
```

### min_dist (default: 0.1)

Controls how tightly UMAP packs points together in the low-dimensional space.

- **Low values (0.0-0.1)**: Points cluster very tightly, good for revealing cluster structure
- **High values (0.5-1.0)**: Points spread out more evenly, preserves broader topology

```python
# Compare different min_dist values
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for ax, d in zip(axes, [0.0, 0.1, 0.8]):
    reducer = umap.UMAP(min_dist=d, random_state=42)
    embedding = reducer.fit_transform(X_scaled)
    ax.scatter(embedding[:, 0], embedding[:, 1],
               c=digits.target, cmap="Spectral", s=5, alpha=0.7)
    ax.set_title(f"min_dist={d}")
    ax.set_xlabel("UMAP 1")
    ax.set_ylabel("UMAP 2")
plt.tight_layout()
plt.show()
```

### n_components (default: 2)

The number of dimensions in the output embedding.

```python
# 2D for visualization
reducer_2d = umap.UMAP(n_components=2, random_state=42)
X_2d = reducer_2d.fit_transform(X_scaled)

# 3D for richer structure
reducer_3d = umap.UMAP(n_components=3, random_state=42)
X_3d = reducer_3d.fit_transform(X_scaled)

# Higher dimensions for downstream ML tasks (e.g., clustering)
reducer_10d = umap.UMAP(n_components=10, random_state=42)
X_10d = reducer_10d.fit_transform(X_scaled)

print(f"2D shape:  {X_2d.shape}")    # (1797, 2)
print(f"3D shape:  {X_3d.shape}")    # (1797, 3)
print(f"10D shape: {X_10d.shape}")   # (1797, 10)
```

```
2D shape:  (1797, 2)
3D shape:  (1797, 3)
10D shape: (1797, 10)
```

### metric (default: "euclidean")

The distance function used to measure similarity in the original high-dimensional space.

```python
# Common metric choices
reducer_euclidean = umap.UMAP(metric="euclidean", random_state=42)   # default, general purpose
reducer_cosine    = umap.UMAP(metric="cosine", random_state=42)      # text/embeddings
reducer_manhattan = umap.UMAP(metric="manhattan", random_state=42)   # sparse data
reducer_corr      = umap.UMAP(metric="correlation", random_state=42) # time series
# You can also pass a custom callable (must be numba @njit decorated)
```

### Parameter Tuning Summary

| Goal                        | n_neighbors | min_dist | metric      |
|-----------------------------|-------------|----------|-------------|
| Fine-grained clusters       | 5-15        | 0.0-0.1  | euclidean   |
| Global topology overview    | 50-200      | 0.5-1.0  | euclidean   |
| Text / embedding similarity | 15-30       | 0.0-0.1  | cosine      |
| Feature reduction for ML    | 15-30       | 0.0-0.1  | euclidean   |
| Sparse binary data          | 15-30       | 0.1      | jaccard     |

---

## Visualizing Results

### Basic 2D Scatter Plot

```python
import umap
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler

digits = load_digits()
X_scaled = StandardScaler().fit_transform(digits.data)

reducer = umap.UMAP(random_state=42)
embedding = reducer.fit_transform(X_scaled)

# Color by digit label
plt.figure(figsize=(10, 8))
scatter = plt.scatter(
    embedding[:, 0], embedding[:, 1],
    c=digits.target,          # color by class label
    cmap="Spectral",          # perceptually distinct colormap
    s=10,                     # point size
    alpha=0.7                 # slight transparency for overlap
)
plt.colorbar(scatter, label="Digit")
plt.title("UMAP Projection of Handwritten Digits")
plt.xlabel("UMAP 1")
plt.ylabel("UMAP 2")
plt.tight_layout()
plt.show()
```

### Annotated Plot with Legend

```python
import umap
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

reducer = umap.UMAP(n_neighbors=20, min_dist=0.1, random_state=42)
embedding = reducer.fit_transform(X_scaled)

# Plot each class separately for a proper legend
fig, ax = plt.subplots(figsize=(9, 7))
for i, name in enumerate(iris.target_names):
    mask = iris.target == i
    ax.scatter(
        embedding[mask, 0], embedding[mask, 1],
        label=name, s=30, alpha=0.8
    )

ax.legend(title="Species", fontsize=11)
ax.set_title("UMAP Projection of Iris Dataset")
ax.set_xlabel("UMAP 1")
ax.set_ylabel("UMAP 2")
plt.tight_layout()
plt.show()
```

---

## Supervised and Semi-Supervised UMAP

### Supervised UMAP

When labels are available, you can pass them to `fit()` so UMAP adjusts the embedding to better separate known classes.

```python
import umap
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler

digits = load_digits()
X_scaled = StandardScaler().fit_transform(digits.data)

# Unsupervised — UMAP uses only feature distances
reducer_unsup = umap.UMAP(random_state=42)
emb_unsup = reducer_unsup.fit_transform(X_scaled)

# Supervised — pass labels via the y parameter
reducer_sup = umap.UMAP(random_state=42)
emb_sup = reducer_sup.fit_transform(X_scaled, y=digits.target)

# Compare side by side
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

ax1.scatter(emb_unsup[:, 0], emb_unsup[:, 1],
            c=digits.target, cmap="Spectral", s=5, alpha=0.7)
ax1.set_title("Unsupervised UMAP")

ax2.scatter(emb_sup[:, 0], emb_sup[:, 1],
            c=digits.target, cmap="Spectral", s=5, alpha=0.7)
ax2.set_title("Supervised UMAP")

plt.tight_layout()
plt.show()
```

### Semi-Supervised UMAP

When only some labels are available, use `-1` for unlabeled points. UMAP uses the known labels to guide the embedding while still learning from unlabeled data.

```python
import umap
import numpy as np
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler

digits = load_digits()
X_scaled = StandardScaler().fit_transform(digits.data)

# Simulate partial labels: keep only 10%, mark the rest as -1
rng = np.random.default_rng(42)
y_partial = digits.target.copy()
y_partial[rng.random(len(y_partial)) > 0.1] = -1  # -1 means unlabeled

# Semi-supervised fit — pass partial labels to y
reducer = umap.UMAP(random_state=42)
emb_semi = reducer.fit_transform(X_scaled, y=y_partial)
print(f"Embedding shape: {emb_semi.shape}")  # (1797, 2)
```

---

## Working with Different Data Types

### Text Embeddings

```python
import umap
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import fetch_20newsgroups

# Load a subset of newsgroups
categories = ["sci.space", "rec.sport.baseball", "comp.graphics", "talk.politics.misc"]
newsgroups = fetch_20newsgroups(subset="train", categories=categories)

# Convert text to TF-IDF vectors
vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
X_tfidf = vectorizer.fit_transform(newsgroups.data)

# Use cosine metric for text data
reducer = umap.UMAP(
    n_neighbors=15,
    min_dist=0.1,
    metric="cosine",       # cosine similarity for text
    random_state=42
)
embedding = reducer.fit_transform(X_tfidf)

print(f"TF-IDF shape:   {X_tfidf.shape}")
print(f"Embedding shape: {embedding.shape}")
```

```
TF-IDF shape:   (2353, 5000)
Embedding shape: (2353, 2)
```

### Tabular Data

```python
import umap
import numpy as np
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler

# Wine dataset: 13 continuous features from chemical analysis
wine = load_wine()
X = wine.data
y = wine.target

# Scaling is important for tabular data with different units
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

reducer = umap.UMAP(
    n_neighbors=20,
    min_dist=0.1,
    metric="euclidean",
    random_state=42
)
embedding = reducer.fit_transform(X_scaled)

print(f"Wine features:   {wine.feature_names}")
print(f"Original shape:  {X.shape}")        # (178, 13)
print(f"Embedding shape: {embedding.shape}") # (178, 2)
```

```
Original shape:  (178, 13)
Embedding shape: (178, 2)
```

---

## Integration with scikit-learn

UMAP implements the scikit-learn transformer API, so it works seamlessly in pipelines.

### In a Classification Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.datasets import load_digits
import umap

digits = load_digits()
X, y = digits.data, digits.target
# UMAP as a dimensionality reduction step before classification
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("umap", umap.UMAP(n_components=10, random_state=42)),  # reduce 64 -> 10
    ("clf", RandomForestClassifier(n_estimators=100, random_state=42))
])

scores = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy")
print(f"Accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")
```

```
Accuracy: 0.9688 (+/- 0.0101)
```

### With GridSearchCV

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_digits
import umap

digits = load_digits()
X, y = digits.data, digits.target

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("umap", umap.UMAP(random_state=42)),
    ("svm", SVC())
])

# Use double underscore to reference nested parameters
param_grid = {
    "umap__n_components": [5, 10, 20],
    "umap__n_neighbors": [10, 15, 30],
    "svm__C": [1, 10],
}

search = GridSearchCV(pipeline, param_grid, cv=3, scoring="accuracy", n_jobs=-1)
search.fit(X, y)

print(f"Best params: {search.best_params_}")
print(f"Best score:  {search.best_score_:.4f}")
```

---

## Performance Tips

UMAP uses `pynndescent` by default for fast approximate nearest neighbor search. Install it with `pip install pynndescent` for best performance on large datasets.

### Precomputed Distances

If you already have a distance matrix, pass it directly to avoid redundant computation.

```python
import umap
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

# Compute distance matrix once
dist_matrix = pairwise_distances(X_scaled, metric="euclidean")

# Pass precomputed distances
reducer = umap.UMAP(
    metric="precomputed",          # tell UMAP distances are precomputed
    n_neighbors=15,
    random_state=42
)
embedding = reducer.fit_transform(dist_matrix)

print(f"Distance matrix shape: {dist_matrix.shape}")  # (150, 150)
print(f"Embedding shape:       {embedding.shape}")     # (150, 2)
```

```
Distance matrix shape: (150, 150)
Embedding shape:       (150, 2)
```

### General Performance Guidelines

```python
# Tip 1: Reduce dimensions with PCA first for very high-dimensional data
from sklearn.decomposition import PCA

# If features >> 100, PCA to ~50-100 dims first is often beneficial
pca = PCA(n_components=50)
X_pca = pca.fit_transform(X_scaled)   # fast linear reduction
embedding = umap.UMAP(random_state=42).fit_transform(X_pca)  # then non-linear

# Tip 2: Use init="pca" instead of "spectral" for faster initialization
reducer_pca_init = umap.UMAP(init="pca", random_state=42)

# Tip 3: Use lower n_epochs for faster (rougher) embeddings
reducer_fast = umap.UMAP(n_epochs=200, random_state=42)   # default is None (auto)

# Tip 4: Use larger n_neighbors for smoother, faster convergence
reducer_smooth = umap.UMAP(n_neighbors=50, random_state=42)

# Tip 5: Set low_memory=True for datasets that strain RAM
reducer_lowmem = umap.UMAP(low_memory=True, random_state=42)
```

---

## Practice Exercises

### Exercise 1: Compare Dimensionality Reduction Methods

```python
import umap
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

digits = load_digits()
X_scaled = StandardScaler().fit_transform(digits.data)
y = digits.target

# Apply three methods and plot results side by side
# 1. PCA
# 2. t-SNE
# 3. UMAP
# Compare cluster separation and runtime for each
```

### Exercise 2: Supervised vs. Unsupervised

```python
import umap
import numpy as np
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

digits = load_digits()
X_scaled = StandardScaler().fit_transform(digits.data)
y = digits.target

# 1. Run unsupervised UMAP
# 2. Run supervised UMAP
# 3. Run semi-supervised UMAP (label only 20% of data)
# 4. Compute silhouette scores for each embedding
# 5. Which approach gives the best-separated clusters?
```

### Exercise 3: UMAP in a Classification Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.datasets import load_digits
import umap

digits = load_digits()
X, y = digits.data, digits.target

# Build a pipeline: StandardScaler -> UMAP -> KNN
# Try n_components in [2, 5, 10, 20, 30]
# Find the n_components that maximizes cross-validated accuracy
# Compare to a pipeline without UMAP (just StandardScaler -> KNN)
```

---

## Summary

These notes cover the fundamental concepts and practical usage of UMAP:

1. **What UMAP Is**: A non-linear dimensionality reduction method based on manifold learning and topological data analysis, faster and more scalable than t-SNE
2. **Core Concepts**: Fuzzy simplicial set construction from nearest neighbors, followed by cross-entropy optimization in low dimensions
3. **Basic Usage**: `fit_transform()` for one-shot reduction, separate `fit()` / `transform()` for projecting new data
4. **Key Parameters**: `n_neighbors` (local vs. global), `min_dist` (cluster tightness), `n_components` (output dims), `metric` (distance function)
5. **Visualization**: 2D and 3D scatter plots colored by labels using matplotlib
6. **Supervised / Semi-Supervised**: Pass labels to `y` parameter to guide embedding; use `-1` for unlabeled points
7. **Data Types**: Text (cosine metric on TF-IDF), images (euclidean on pixels), tabular (euclidean on scaled features)
8. **scikit-learn Integration**: Drop-in transformer for `Pipeline`, compatible with `GridSearchCV`
9. **Performance**: PCA pre-reduction, `pynndescent` for approximate neighbors, precomputed distances, `low_memory` mode

### Next Steps

1. Apply UMAP to your own datasets and experiment with parameters
2. Combine UMAP with HDBSCAN for unsupervised cluster discovery
3. Explore `umap.AlignedUMAP` for embedding time-series or evolving datasets
4. Try `umap.ParametricUMAP` for neural-network-based embeddings with PyTorch or TensorFlow
5. Use UMAP embeddings as features for downstream classifiers and compare accuracy

### Additional Resources

- **UMAP Documentation**: https://umap-learn.readthedocs.io/
- **UMAP Paper**: McInnes, Healy, Melville — "UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction" (2018)
- **Understanding UMAP**: https://pair-code.github.io/understanding-umap/
- **UMAP GitHub Repository**: https://github.com/lmcinnes/umap
- **How UMAP Works (docs)**: https://umap-learn.readthedocs.io/en/latest/how_umap_works.html
