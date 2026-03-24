# Introduction to HDBSCAN

## Table of Contents

1. [What is HDBSCAN?](#what-is-hdbscan)
2. [Installation and Setup](#installation-and-setup)
3. [Core Concepts](#core-concepts)
4. [Basic Usage](#basic-usage)
5. [Key Parameters](#key-parameters)
6. [Understanding Results](#understanding-results)
7. [Visualization](#visualization)
8. [Comparison with Other Clustering Methods](#comparison-with-other-clustering-methods)
9. [Working with UMAP+HDBSCAN Pipeline](#working-with-umaphdbscan-pipeline)
10. [Soft Clustering and Prediction](#soft-clustering-and-prediction)
11. [Practice Exercises](#practice-exercises)
12. [Summary](#summary)

---

## What is HDBSCAN?

HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise) is a clustering algorithm that extends DBSCAN by converting it into a hierarchical clustering algorithm and then extracting a flat clustering based on cluster stability:

- **Density-based**: Finds clusters as regions of high density separated by regions of low density
- **Hierarchical**: Builds a hierarchy of clusters at varying density levels, then selects the most stable clusters
- **No k required**: Unlike KMeans, you do not need to specify the number of clusters in advance
- **Noise-aware**: Points that do not belong to any cluster are labeled as noise (`-1`)
- **Varying density**: Handles clusters of different densities, which KMeans and DBSCAN struggle with

### How it compares to other algorithms

| Feature                  | KMeans              | DBSCAN          | HDBSCAN             |
|--------------------------|---------------------|-----------------|---------------------|
| Must specify k           | Yes                 | No              | No                  |
| Handles noise            | No                  | Yes             | Yes                 |
| Cluster shape            | Spherical only      | Arbitrary       | Arbitrary           |
| Varying density clusters | No                  | No (single eps) | Yes                 |
| Deterministic            | No (init-dependent) | Yes             | Yes                 |
| Soft clustering          | No                  | No              | Yes (probabilities) |

---

## Installation and Setup

```bash
# Install hdbscan (pulls in numpy, scipy, scikit-learn)
pip install hdbscan

# For visualization support
pip install matplotlib seaborn
```

```python
import hdbscan
import numpy as np
from sklearn.datasets import make_blobs, make_moons
import matplotlib.pyplot as plt

print(hdbscan.__version__)
```

```text
# Output:
# 0.8.38
```

---

## Core Concepts

### Density-Based Clustering

HDBSCAN treats clusters as connected regions of high point density. Instead of assuming clusters are spherical (like KMeans), it discovers clusters of arbitrary shape by following the density landscape of the data.

### Core Distance and Mutual Reachability

The **core distance** of a point is the distance to its k-th nearest neighbor (where k = `min_samples`). The **mutual reachability distance** between two points is:

```text
mutual_reachability(a, b) = max(core_dist(a), core_dist(b), dist(a, b))
```

This smooths out density variations and makes the algorithm robust to noise.

### Cluster Hierarchy and Stability

HDBSCAN builds a minimum spanning tree from mutual reachability distances, then constructs a cluster hierarchy by progressively removing the longest edges. Each cluster is scored by its **stability** — how long it persists across density thresholds. The algorithm selects the set of clusters that maximizes total stability.

### Noise Points

Points that do not belong to any stable cluster are labeled as `-1`. This is a key advantage over KMeans, which forces every point into a cluster even if it is an outlier.

---

## Basic Usage

### Generating Sample Data

```python
import numpy as np
from sklearn.datasets import make_blobs

# Create clusters with varying density
# Cluster 0: tight (std=0.5), Cluster 1: medium (std=1.5), Cluster 2: loose (std=3.0)
np.random.seed(42)
centers = [[-5, -5], [0, 0], [7, 7]]
n_samples = [200, 300, 200]
cluster_std = [0.5, 1.5, 3.0]

X, y_true = make_blobs(
    n_samples=n_samples,
    centers=centers,
    cluster_std=cluster_std,
    random_state=42
)

# Add some noise points scattered across the space
noise = np.random.uniform(-15, 15, size=(50, 2))
X = np.vstack([X, noise])

print(f"Data shape: {X.shape}")
```

```text
# Output:
# Data shape: (750, 2)
```

### Fitting the Model

```python
import hdbscan

# Create and fit the clusterer
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=15,   # minimum number of points to form a cluster
    min_samples=5           # controls how conservative clustering is
)

# Fit the model to the data
clusterer.fit(X)

# Get cluster labels (-1 means noise)
labels = clusterer.labels_

# Get the probability of each point belonging to its assigned cluster
probabilities = clusterer.probabilities_

print(f"Cluster labels found: {np.unique(labels)}")
print(f"Number of clusters:   {len(set(labels)) - (1 if -1 in labels else 0)}")
print(f"Noise points:         {np.sum(labels == -1)}")
```

```text
# Output:
# Cluster labels found: [-1  0  1  2]
# Number of clusters:   3
# Noise points:         68
```

### Quick Plot of Results

```python
import matplotlib.pyplot as plt

# Color each point by its cluster; noise points in gray
fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(
    X[:, 0], X[:, 1],
    c=labels,
    cmap="viridis",
    s=10,
    alpha=0.7
)

# Mark noise points with red x markers
noise_mask = labels == -1
ax.scatter(
    X[noise_mask, 0], X[noise_mask, 1],
    c="red", marker="x", s=20, label="Noise"
)

ax.set_title("HDBSCAN Clustering Result")
ax.legend()
plt.colorbar(scatter, ax=ax, label="Cluster Label")
plt.tight_layout()
plt.show()
```

---

## Key Parameters

### min_cluster_size

The most important parameter. Sets the smallest grouping you wish to consider a cluster:

```python
import hdbscan

# Smaller value: more clusters, smaller clusters allowed
clusterer_small = hdbscan.HDBSCAN(min_cluster_size=5)
clusterer_small.fit(X)
print(f"min_cluster_size=5  -> {len(set(clusterer_small.labels_)) - 1} clusters")

# Larger value: fewer clusters, only large groupings kept
clusterer_large = hdbscan.HDBSCAN(min_cluster_size=50)
clusterer_large.fit(X)
print(f"min_cluster_size=50 -> {len(set(clusterer_large.labels_)) - 1} clusters")
```

```text
# Output:
# min_cluster_size=5  -> 6 clusters
# min_cluster_size=50 -> 3 clusters
```

### min_samples

Controls how conservative the clustering is. Higher values make the algorithm more conservative (more points become noise):

```python
# Less conservative: fewer noise points
c1 = hdbscan.HDBSCAN(min_cluster_size=15, min_samples=1).fit(X)
print(f"min_samples=1  -> noise points: {np.sum(c1.labels_ == -1)}")

# More conservative: more noise points
c2 = hdbscan.HDBSCAN(min_cluster_size=15, min_samples=15).fit(X)
print(f"min_samples=15 -> noise points: {np.sum(c2.labels_ == -1)}")
```

```text
# Output:
# min_samples=1  -> noise points: 32
# min_samples=15 -> noise points: 112
```

### cluster_selection_epsilon

Merges clusters that are closer than epsilon. Useful when you want DBSCAN-like behavior for nearby clusters but still want HDBSCAN's varying-density support:

```python
# Without epsilon: may split nearby dense regions
c_no_eps = hdbscan.HDBSCAN(min_cluster_size=15).fit(X)

# With epsilon: merges clusters closer than 0.5 apart
c_eps = hdbscan.HDBSCAN(
    min_cluster_size=15,
    cluster_selection_epsilon=0.5
).fit(X)

print(f"No epsilon:    {len(set(c_no_eps.labels_)) - 1} clusters")
print(f"epsilon=0.5:   {len(set(c_eps.labels_)) - 1} clusters")
```

### cluster_selection_method

Controls how flat clusters are extracted from the hierarchy:

```python
# 'eom' (Excess of Mass) - default, selects variable-size clusters
c_eom = hdbscan.HDBSCAN(
    min_cluster_size=15,
    cluster_selection_method='eom'    # favors larger clusters with subclusters
).fit(X)

# 'leaf' - selects the leaves of the condensed tree (smaller, more homogeneous)
c_leaf = hdbscan.HDBSCAN(
    min_cluster_size=15,
    cluster_selection_method='leaf'   # favors smaller, tighter clusters
).fit(X)

print(f"EOM method:  {len(set(c_eom.labels_)) - 1} clusters")
print(f"Leaf method: {len(set(c_leaf.labels_)) - 1} clusters")
```

```text
# Output:
# EOM method:  3 clusters
# Leaf method: 5 clusters
```

---

## Understanding Results

### Cluster Labels

```python
clusterer = hdbscan.HDBSCAN(min_cluster_size=15).fit(X)

# labels_: integer array, -1 = noise
labels = clusterer.labels_
print(f"Labels shape: {labels.shape}")
print(f"Unique labels: {np.unique(labels)}")

# Count points per cluster
for label in np.unique(labels):
    count = np.sum(labels == label)
    name = "Noise" if label == -1 else f"Cluster {label}"
    print(f"  {name}: {count} points")
```

```text
# Output:
# Labels shape: (750,)
# Unique labels: [-1  0  1  2]
#   Noise: 68 points
#   Cluster 0: 198 points
#   Cluster 1: 290 points
#   Cluster 2: 194 points
```

### Membership Probabilities

```python
# probabilities_: float array in [0, 1], how strongly a point belongs to its cluster
probs = clusterer.probabilities_

print(f"Mean probability:   {probs.mean():.3f}")
print(f"Median probability: {np.median(probs):.3f}")

# Points near cluster cores have high probability
# Points near cluster edges have lower probability
# Noise points have probability 0
print(f"Noise point probabilities (all zero): {probs[labels == -1].sum()}")

# Find borderline points (assigned but with low confidence)
borderline = (labels != -1) & (probs < 0.5)
print(f"Borderline points (prob < 0.5): {borderline.sum()}")
```

```text
# Output:
# Mean probability:   0.721
# Median probability: 0.862
# Noise point probabilities (all zero): 0.0
# Borderline points (prob < 0.5): 45
```

### Cluster Persistence

```python
# cluster_persistence_: how persistent each cluster is in the hierarchy
# Higher values = more stable, well-separated cluster
persistence = clusterer.cluster_persistence_

for i, p in enumerate(persistence):
    print(f"Cluster {i}: persistence = {p:.4f}")
```

```text
# Output:
# Cluster 0: persistence = 0.6821
# Cluster 1: persistence = 0.3145
# Cluster 2: persistence = 0.1287
```

### Outlier Scores

```python
# outlier_scores_: higher = more anomalous
outlier_scores = clusterer.outlier_scores_
print(f"Mean outlier score: {outlier_scores.mean():.4f}")
print(f"Max outlier score:  {outlier_scores.max():.4f}")

# Top 5 most anomalous points
top_outliers = np.argsort(outlier_scores)[-5:]
print(f"Top outlier indices: {top_outliers}")
```

---

## Visualization

### Condensed Tree

The condensed tree shows the cluster hierarchy and how clusters split as the density threshold changes:

```python
import hdbscan

clusterer = hdbscan.HDBSCAN(min_cluster_size=15).fit(X)

# Plot the condensed tree - selected clusters are highlighted
clusterer.condensed_tree_.plot(
    select_clusters=True,      # highlight selected clusters
    selection_palette=['blue', 'green', 'orange', 'red', 'purple']
)
plt.title("HDBSCAN Condensed Tree")
plt.show()
```

### Cluster Plot with Probabilities

```python
import matplotlib.pyplot as plt
import numpy as np

labels = clusterer.labels_
probs = clusterer.probabilities_
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: clusters colored by label
axes[0].scatter(X[:, 0], X[:, 1], c=labels, cmap="Spectral", s=10, alpha=0.7)
axes[0].set_title("Cluster Assignments")

# Right: shade by membership probability (noise in gray)
mask = labels != -1
axes[1].scatter(X[mask, 0], X[mask, 1], c=probs[mask], cmap="YlOrRd", s=10, alpha=0.8)
axes[1].scatter(X[~mask, 0], X[~mask, 1], c="lightgray", s=5, alpha=0.4, label="Noise")
axes[1].set_title("Membership Probabilities")
axes[1].legend()

plt.tight_layout()
plt.show()
```

### Minimum Spanning Tree

```python
# Visualize the mutual reachability minimum spanning tree
clusterer.minimum_spanning_tree_.plot(
    edge_cmap="viridis",
    edge_alpha=0.6,
    node_size=10,
    edge_linewidth=1
)
plt.title("Mutual Reachability Minimum Spanning Tree")
plt.show()
```

---

## Comparison with Other Clustering Methods

This example shows why HDBSCAN outperforms KMeans on clusters of varying density:

```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans, DBSCAN
import hdbscan
import matplotlib.pyplot as plt

# Create data with three clusters of very different densities
np.random.seed(42)
tight = np.random.normal(loc=[-5, -5], scale=0.3, size=(200, 2))   # very dense
medium = np.random.normal(loc=[0, 0], scale=1.5, size=(300, 2))    # moderate density
loose = np.random.normal(loc=[8, 8], scale=3.5, size=(200, 2))     # sparse
noise = np.random.uniform(-15, 20, size=(50, 2))                   # random noise
X = np.vstack([tight, medium, loose, noise])

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# KMeans: forces all points into 3 spherical clusters, no noise handling
km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)
axes[0].scatter(X[:, 0], X[:, 1], c=km.labels_, cmap="viridis", s=10)
axes[0].set_title(f"KMeans (k=3)\nSplits loose cluster, no noise detection")

# DBSCAN: single epsilon cannot handle varying densities
db = DBSCAN(eps=1.0, min_samples=5).fit(X)
axes[1].scatter(X[:, 0], X[:, 1], c=db.labels_, cmap="viridis", s=10)
n_clusters_db = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
axes[1].set_title(f"DBSCAN (eps=1.0)\n{n_clusters_db} clusters, misses sparse cluster")

# HDBSCAN: handles varying density naturally
hdb = hdbscan.HDBSCAN(min_cluster_size=15).fit(X)
axes[2].scatter(X[:, 0], X[:, 1], c=hdb.labels_, cmap="viridis", s=10)
n_clusters_hdb = len(set(hdb.labels_)) - (1 if -1 in hdb.labels_ else 0)
axes[2].set_title(f"HDBSCAN\n{n_clusters_hdb} clusters, varying density handled")

plt.suptitle("Varying Density Clusters: KMeans vs DBSCAN vs HDBSCAN", fontsize=14)
plt.tight_layout()
plt.show()
```

```text
# Key observations:
# - KMeans splits the sparse cluster to balance sizes, assigns noise to clusters
# - DBSCAN with eps=1.0 finds the tight cluster but merges or loses the sparse one
# - HDBSCAN correctly identifies all three clusters AND labels noise as -1
```

---

## Working with UMAP+HDBSCAN Pipeline

UMAP (Uniform Manifold Approximation and Projection) reduces high-dimensional data to a low-dimensional space while preserving local structure. Pairing UMAP with HDBSCAN is a common pattern for clustering high-dimensional data:

```bash
pip install umap-learn
```

```python
import umap
import hdbscan
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer

# Example: cluster text documents
newsgroups = fetch_20newsgroups(
    subset='train',
    categories=['sci.space', 'rec.sport.baseball', 'comp.graphics'],
    remove=('headers', 'footers', 'quotes')
)

# Convert text to TF-IDF features (high-dimensional)
tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
X_tfidf = tfidf.fit_transform(newsgroups.data)
print(f"TF-IDF shape: {X_tfidf.shape}")   # (n_docs, 5000)

# Step 1: Reduce dimensions with UMAP
reducer = umap.UMAP(
    n_components=5,          # reduce to 5 dimensions for clustering
    n_neighbors=15,          # local neighborhood size
    min_dist=0.0,            # pack points together (good for clustering)
    metric='cosine',         # cosine similarity for text data
    random_state=42
)
X_umap = reducer.fit_transform(X_tfidf)
print(f"UMAP shape:  {X_umap.shape}")     # (n_docs, 5)

# Step 2: Cluster with HDBSCAN
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=20,
    min_samples=10,
    cluster_selection_method='eom'
)
clusterer.fit(X_umap)

labels = clusterer.labels_
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
n_noise = np.sum(labels == -1)
print(f"Clusters found: {n_clusters}")
print(f"Noise points:   {n_noise}")
```

```text
# Output:
# TF-IDF shape: (1774, 5000)
# UMAP shape:  (1774, 5)
# Clusters found: 3
# Noise points:   87
```

### Visualize the Pipeline

```python
# Reduce to 2D for visualization (separate embedding from the clustering one)
X_2d = umap.UMAP(n_components=2, metric='cosine', random_state=42).fit_transform(X_tfidf)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].scatter(X_2d[:, 0], X_2d[:, 1], c=newsgroups.target, cmap="tab10", s=5, alpha=0.6)
axes[0].set_title("True Categories")
axes[1].scatter(X_2d[:, 0], X_2d[:, 1], c=labels, cmap="tab10", s=5, alpha=0.6)
axes[1].set_title(f"HDBSCAN Clusters ({n_clusters} found)")
plt.tight_layout()
plt.show()
```

---

## Soft Clustering and Prediction

### Soft Clustering

HDBSCAN can provide probability vectors showing how much each point belongs to each cluster:

```python
import hdbscan
import numpy as np

# Enable prediction data at fit time
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=15,
    prediction_data=True       # required for soft clustering and prediction
).fit(X)

# Get soft cluster membership vectors
soft_clusters = hdbscan.all_points_membership_vectors(clusterer)
print(f"Soft cluster shape: {soft_clusters.shape}")  # (n_points, n_clusters)

# Each row sums to ~1 and shows membership across all clusters
print(f"First point memberships: {soft_clusters[0].round(3)}")
print(f"Sum of memberships:      {soft_clusters[0].sum():.3f}")

# Find points that are ambiguous (belong to multiple clusters)
max_prob = soft_clusters.max(axis=1)
ambiguous = max_prob < 0.6
print(f"Ambiguous points (max prob < 0.6): {ambiguous.sum()}")
```

```text
# Output:
# Soft cluster shape: (750, 3)
# First point memberships: [0.002 0.996 0.002]
# Sum of memberships:      1.000
# Ambiguous points (max prob < 0.6): 42
```

### Predicting Clusters for New Points

```python
from hdbscan import approximate_predict

# Generate new unseen data points
new_points = np.array([
    [-5, -5],     # should fall in the tight cluster
    [0, 1],       # near the medium cluster
    [15, 15],     # far from everything (likely noise)
])

# Predict cluster labels and probabilities for new points
new_labels, new_probs = approximate_predict(clusterer, new_points)

for i, (label, prob) in enumerate(zip(new_labels, new_probs)):
    status = "Noise" if label == -1 else f"Cluster {label}"
    print(f"Point {new_points[i]} -> {status} (prob={prob:.3f})")
```

```text
# Output:
# Point [-5. -5.] -> Cluster 0 (prob=0.912)
# Point [0. 1.] -> Cluster 1 (prob=0.754)
# Point [15. 15.] -> Noise (prob=0.000)
```

### Soft Prediction for New Points

```python
from hdbscan import membership_vector

# Get full membership vectors for new points
new_membership = membership_vector(clusterer, new_points)
for i, memb in enumerate(new_membership):
    print(f"Point {new_points[i]} -> memberships: {memb.round(3)}")
```

```text
# Output:
# Point [-5. -5.] -> memberships: [0.952 0.032 0.016]
# Point [0. 1.] -> memberships: [0.041 0.897 0.062]
# Point [15. 15.] -> memberships: [0.112 0.224 0.664]
```

---

## Practice Exercises

### Exercise 1: Moon-Shaped Clusters

Use `sklearn.datasets.make_moons` to generate crescent-shaped clusters. Compare KMeans and HDBSCAN results.

```python
from sklearn.datasets import make_moons

X_moons, y_moons = make_moons(n_samples=500, noise=0.08, random_state=42)

# Your code here:
# 1. Fit KMeans with k=2 and plot the result
# 2. Fit HDBSCAN and plot the result
# 3. Which algorithm correctly separates the two crescents?
```

### Exercise 2: Parameter Sensitivity

Generate blob data and explore how `min_cluster_size` affects the number of clusters found:

```python
from sklearn.datasets import make_blobs

X_blobs, _ = make_blobs(n_samples=1000, centers=5, cluster_std=1.0, random_state=42)

# Your code here:
# 1. Run HDBSCAN with min_cluster_size values: 5, 10, 25, 50, 100
# 2. Record the number of clusters and noise points for each
# 3. Plot the results as a line chart
```

### Exercise 3: Anomaly Detection

Use HDBSCAN's `outlier_scores_` to build a simple anomaly detector:

```python
# Your code here:
# 1. Generate normal data with make_blobs
# 2. Inject 5% anomalous points using np.random.uniform
# 3. Fit HDBSCAN and use outlier_scores_ to rank points
# 4. Check if the top-scoring outliers correspond to the injected anomalies
```

### Exercise 4: UMAP+HDBSCAN on Digits

```python
from sklearn.datasets import load_digits
from sklearn.metrics import adjusted_rand_score
digits = load_digits()

# Your code here:
# 1. Reduce digits.data from 64 dimensions to 5 with UMAP
# 2. Cluster with HDBSCAN
# 3. Compute adjusted_rand_score(digits.target, labels)
# 4. Visualize with a 2D UMAP projection colored by HDBSCAN labels
```

---

## Summary

HDBSCAN is a powerful density-based clustering algorithm that addresses major limitations of KMeans and DBSCAN:

- **No need to specify k**: the number of clusters is determined automatically from the data
- **Handles varying density**: unlike DBSCAN's fixed epsilon, HDBSCAN adapts to different density levels
- **Noise detection**: outlier points are labeled as `-1` rather than forced into a cluster
- **Soft clustering**: membership probabilities give confidence scores for each assignment
- **Hierarchical view**: the condensed tree reveals the structure of the data at multiple scales
- **Prediction**: new points can be assigned to existing clusters with `approximate_predict`
- **Pairs well with UMAP**: for high-dimensional data, UMAP dimensionality reduction followed by HDBSCAN is a standard and effective pipeline

### Next Steps

- Explore `cluster_selection_epsilon` to fine-tune cluster granularity
- Use `hdbscan.validity.validity_index` to evaluate clustering quality (DBCV score)
- Try HDBSCAN with different distance metrics (`metric` parameter): euclidean, manhattan, cosine
- Combine with UMAP for text, image, or genomic data clustering
- Investigate the `BranchDetector` for finding sub-clusters within existing clusters
- Scale to large datasets using `core_dist_n_jobs` for parallel core distance computation

### Additional Resources

- [HDBSCAN Documentation](https://hdbscan.readthedocs.io/)
- [How HDBSCAN Works (theory)](https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html)
- [Parameter Selection Guide](https://hdbscan.readthedocs.io/en/latest/parameter_selection.html)
- [Comparing Clustering Algorithms (scikit-learn)](https://scikit-learn.org/stable/modules/clustering.html)
- [UMAP Documentation](https://umap-learn.readthedocs.io/)
- [McInnes, L., Healy, J., & Astels, S. (2017). "hdbscan: Hierarchical density based clustering." JOSS.](https://doi.org/10.21105/joss.00205)
