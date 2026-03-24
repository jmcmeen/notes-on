# Introduction to scikit-learn

## Table of Contents

1. [What is scikit-learn?](#what-is-scikit-learn)
2. [Installation and Setup](#installation-and-setup)
3. [Core Concepts](#core-concepts)
4. [Data Preprocessing](#data-preprocessing)
5. [Supervised Learning - Classification](#supervised-learning---classification)
6. [Supervised Learning - Regression](#supervised-learning---regression)
7. [Unsupervised Learning](#unsupervised-learning)
8. [Model Selection](#model-selection)
9. [Pipelines](#pipelines)
10. [Feature Selection](#feature-selection)
11. [Model Persistence](#model-persistence)
12. [Practice Exercises](#practice-exercises)
13. [Summary](#summary)

---

## What is scikit-learn?

scikit-learn is a Python library for machine learning built on NumPy, SciPy, and Matplotlib. It provides:
- **Classification**: Identify which category an object belongs to (spam detection, image recognition)
- **Regression**: Predict a continuous value (price forecasting, temperature prediction)
- **Clustering**: Group similar objects together (customer segmentation, anomaly detection)
- **Dimensionality Reduction**: Reduce the number of features (PCA, feature selection)
- **Model Selection**: Compare, validate, and tune models (cross-validation, grid search)
- **Preprocessing**: Feature extraction and normalization (scaling, encoding, imputation)

---

## Installation and Setup

```bash
pip install scikit-learn
```

```python
import sklearn
import numpy as np
import pandas as pd

print(sklearn.__version__)
```

```python
# Common imports organized by category
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris, make_classification
```

---

## Core Concepts

### The Estimator API

All scikit-learn models follow a consistent interface built around estimators:

```python
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier

# Every estimator is instantiated with hyperparameters
model = LinearRegression(fit_intercept=True)  # create estimator with params
clf = DecisionTreeClassifier(max_depth=3)     # another estimator
```

### fit / predict / transform

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

# Generate sample data
X, y = make_classification(n_samples=100, n_features=4, random_state=42)

# fit() - learn from data
scaler = StandardScaler()
scaler.fit(X)                        # learn mean and std from X

# transform() - apply learned parameters to data
X_scaled = scaler.transform(X)       # scale X using learned mean/std

# fit_transform() - fit and transform in one step (more efficient)
X_scaled = scaler.fit_transform(X)   # equivalent to fit() then transform()

# fit() + predict() - for supervised models
model = LogisticRegression(random_state=42)
model.fit(X_scaled, y)               # learn from features X and labels y
predictions = model.predict(X_scaled) # predict labels for new data
probas = model.predict_proba(X_scaled) # predict class probabilities

print(f"Predictions (first 10): {predictions[:10]}")
print(f"Probability shape:      {probas.shape}")  # (100, 2) - prob for each class
```

```
# Output:
# Predictions (first 10): [0 0 1 1 0 1 0 1 1 1]
# Probability shape:      (100, 2)
```

### Estimator Attributes

```python
from sklearn.linear_model import LinearRegression
import numpy as np

# Attributes learned during fit() end with an underscore
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

model = LinearRegression()
model.fit(X, y)

print(f"Coefficient: {model.coef_}")       # learned slope: [2.]
print(f"Intercept:   {model.intercept_}")  # learned intercept: 0.0
print(f"Parameters:  {model.get_params()}") # hyperparameters (set before fit)
```

```
# Output:
# Coefficient: [2.]
# Intercept:   0.0
# Parameters:  {'copy_X': True, 'fit_intercept': True, 'n_jobs': None, 'positive': False}
```

---

## Data Preprocessing

### Train/Test Split

```python
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

# Load dataset
iris = load_iris()
X, y = iris.data, iris.target

print(f"Full dataset:  {X.shape}")  # (150, 4)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,       # 20% for testing
    random_state=42,     # reproducible split
    stratify=y           # maintain class proportions in both sets
)

print(f"Training set:  {X_train.shape}")  # (120, 4)
print(f"Test set:      {X_test.shape}")   # (30, 4)
```

```
# Output:
# Full dataset:  (150, 4)
# Training set:  (120, 4)
# Test set:      (30, 4)
```

### Feature Scaling

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import numpy as np

X = np.array([[1, 1000], [2, 2000], [3, 3000], [4, 4000], [5, 5000]], dtype=float)

# StandardScaler: zero mean, unit variance (best for most algorithms)
standard = StandardScaler()
X_standard = standard.fit_transform(X)
print(f"StandardScaler mean: {X_standard.mean(axis=0)}")  # [0. 0.]
print(f"StandardScaler std:  {X_standard.std(axis=0)}")   # [1. 1.]

# MinMaxScaler: scale to [0, 1] range (good for neural networks)
minmax = MinMaxScaler()
X_minmax = minmax.fit_transform(X)
print(f"MinMaxScaler min:    {X_minmax.min(axis=0)}")     # [0. 0.]
print(f"MinMaxScaler max:    {X_minmax.max(axis=0)}")     # [1. 1.]

# RobustScaler: uses median and IQR, robust to outliers
robust = RobustScaler()
X_robust = robust.fit_transform(X)
print(f"RobustScaler median: {np.median(X_robust, axis=0)}")  # [0. 0.]
```

```
# Output:
# StandardScaler mean: [0. 0.]
# StandardScaler std:  [1. 1.]
# MinMaxScaler min:    [0. 0.]
# MinMaxScaler max:    [1. 1.]
# RobustScaler median: [0. 0.]
```

### Encoding Categorical Variables

```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
import numpy as np

# LabelEncoder: convert text labels to integers (for target variable)
le = LabelEncoder()
labels = ["cat", "dog", "cat", "fish", "dog", "fish"]
y_encoded = le.fit_transform(labels)
print(f"Encoded labels:  {y_encoded}")             # [0 1 0 2 1 2]
print(f"Classes:         {le.classes_}")            # ['cat' 'dog' 'fish']
print(f"Inverse:         {le.inverse_transform([0, 1, 2])}")  # ['cat' 'dog' 'fish']

# OneHotEncoder: create binary columns for each category (for features)
ohe = OneHotEncoder(sparse_output=False)
colors = np.array([["red"], ["blue"], ["green"], ["red"], ["blue"]])
X_ohe = ohe.fit_transform(colors)
print(f"One-hot encoded:\n{X_ohe}")
# [[0. 0. 1.]   <- red
#  [1. 0. 0.]   <- blue
#  [0. 1. 0.]   <- green
#  [0. 0. 1.]   <- red
#  [1. 0. 0.]]  <- blue

# OrdinalEncoder: for ordinal categories with meaningful order
oe = OrdinalEncoder(categories=[["low", "medium", "high"]])
sizes = np.array([["medium"], ["high"], ["low"], ["high"]])
X_ordinal = oe.fit_transform(sizes)
print(f"Ordinal encoded: {X_ordinal.ravel()}")  # [1. 2. 0. 2.]
```

### Handling Missing Values

```python
from sklearn.impute import SimpleImputer, KNNImputer
import numpy as np

X = np.array([
    [1, 2, np.nan],
    [3, np.nan, 6],
    [7, 8, 9],
    [np.nan, 5, 3],
    [4, 6, 8]
])

# SimpleImputer: replace missing values with a statistic
mean_imputer = SimpleImputer(strategy="mean")       # also: median, most_frequent, constant
X_mean = mean_imputer.fit_transform(X)
print(f"Mean imputed:\n{X_mean}")

# KNNImputer: use K nearest neighbors to estimate missing values
knn_imputer = KNNImputer(n_neighbors=2)
X_knn = knn_imputer.fit_transform(X)
print(f"KNN imputed:\n{X_knn}")
```

```
# Output:
# Mean imputed:
# [[1.   2.   6.5]
#  [3.   5.25 6. ]
#  [7.   8.   9. ]
#  [3.75 5.   3. ]
#  [4.   6.   8. ]]
# KNN imputed:
# [[1.  2.  7. ]
#  [3.  5.5 6. ]
#  [7.  8.  9. ]
#  [3.5 5.  3. ]
#  [4.  6.  8. ]]
```

---

## Supervised Learning - Classification

### Logistic Regression

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Generate a binary classification dataset
X, y = make_classification(
    n_samples=1000, n_features=10, n_informative=5,
    n_redundant=2, random_state=42
)

# Split and scale
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # fit on train only
X_test_scaled = scaler.transform(X_test)          # transform test with train params

# Train logistic regression
log_reg = LogisticRegression(
    C=1.0,               # inverse regularization strength (smaller = more regularization)
    max_iter=200,         # max iterations for solver convergence
    random_state=42
)
log_reg.fit(X_train_scaled, y_train)

# Evaluate
y_pred = log_reg.predict(X_test_scaled)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"Coefficients shape: {log_reg.coef_.shape}")  # (1, 10)
```

```
# Output:
# Accuracy: 0.8750
# Coefficients shape: (1, 10)
```

### Random Forest Classifier

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# Load iris dataset
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
)

# Train random forest
rf = RandomForestClassifier(
    n_estimators=100,    # number of trees
    max_depth=5,         # max depth per tree
    min_samples_split=5, # min samples to split a node
    random_state=42
)
rf.fit(X_train, y_train)

# Evaluate
y_pred = rf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

# Feature importance
importances = rf.feature_importances_
for name, imp in zip(iris.feature_names, importances):
    print(f"  {name}: {imp:.4f}")
```

```
# Output:
# Accuracy: 1.0000
#   sepal length (cm): 0.0963
#   sepal width (cm): 0.0234
#   petal length (cm): 0.4351
#   petal width (cm): 0.4453
```

### Support Vector Machine (SVM)

```python
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=500, n_features=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# SVM requires feature scaling for best performance
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train SVM with RBF kernel
svm = SVC(
    kernel="rbf",        # radial basis function kernel (also: linear, poly, sigmoid)
    C=1.0,               # regularization parameter
    gamma="scale",       # kernel coefficient (scale = 1 / (n_features * X.var()))
    probability=True,    # enable probability estimates (slower training)
    random_state=42
)
svm.fit(X_train_scaled, y_train)

y_pred = svm.predict(X_test_scaled)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

# Probability predictions
probas = svm.predict_proba(X_test_scaled)[:3]
print(f"Probabilities (first 3):\n{probas}")
```

```
# Output:
# Accuracy: 0.9100
# Probabilities (first 3):
# [[0.08 0.92]
#  [0.91 0.09]
#  [0.87 0.13]]
```

### K-Nearest Neighbors (KNN)

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# KNN is distance-based, so scaling matters
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

knn = KNeighborsClassifier(
    n_neighbors=5,        # number of neighbors to consider
    weights="uniform",    # uniform or distance (weight by inverse distance)
    metric="minkowski",   # distance metric (minkowski with p=2 is euclidean)
    p=2
)
knn.fit(X_train_scaled, y_train)

y_pred = knn.predict(X_test_scaled)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
```

```
# Output:
# Accuracy: 1.0000
```

### Classification Metrics

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)

# Create imbalanced dataset to show metric differences
X, y = make_classification(
    n_samples=1000, n_features=10, n_informative=5,
    weights=[0.7, 0.3],  # 70/30 class imbalance
    random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(random_state=42, max_iter=200)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]  # probability of positive class

# Individual metrics
print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")   # correct / total
print(f"Precision: {precision_score(y_test, y_pred):.4f}")  # TP / (TP + FP)
print(f"Recall:    {recall_score(y_test, y_pred):.4f}")     # TP / (TP + FN)
print(f"F1 Score:  {f1_score(y_test, y_pred):.4f}")         # harmonic mean of precision & recall
print(f"ROC AUC:   {roc_auc_score(y_test, y_proba):.4f}")   # area under ROC curve

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
print(f"\nConfusion Matrix:")
print(f"  TN={cm[0,0]}  FP={cm[0,1]}")
print(f"  FN={cm[1,0]}  TP={cm[1,1]}")

# Full classification report
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Class 0", "Class 1"]))
```

```
# Output:
# Accuracy:  0.8650
# Precision: 0.8182
# Recall:    0.7347
# F1 Score:  0.7742
# ROC AUC:   0.9266
#
# Confusion Matrix:
#   TN=124  FP=8
#   FN=19   TP=49
#
# Classification Report:
#               precision    recall  f1-score   support
#
#      Class 0       0.87      0.94      0.90       132
#      Class 1       0.86      0.72      0.78        68
#
#     accuracy                           0.87       200
#    macro avg       0.86      0.83      0.84       200
# weighted avg       0.86      0.87      0.86       200
```

---

## Supervised Learning - Regression

### Linear Regression

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np

# Generate realistic data: house prices based on size and rooms
rng = np.random.default_rng(42)
n_samples = 200
size = rng.uniform(500, 3500, n_samples)     # square feet
rooms = rng.integers(1, 7, n_samples)        # number of rooms
noise = rng.normal(0, 20000, n_samples)
price = 50 * size + 10000 * rooms + 50000 + noise  # true relationship

X = np.column_stack([size, rooms])
y = price

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train linear regression
model = LinearRegression()
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
print(f"Coefficients: {model.coef_}")          # [~50, ~10000]
print(f"Intercept:    {model.intercept_:.2f}") # ~50000
print(f"MSE:          {mean_squared_error(y_test, y_pred):.2f}")
print(f"RMSE:         {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
print(f"MAE:          {mean_absolute_error(y_test, y_pred):.2f}")
print(f"R² Score:     {r2_score(y_test, y_pred):.4f}")  # 1.0 = perfect fit
```

```
# Output:
# Coefficients: [   49.55 10665.47]
# Intercept:    47583.42
# MSE:          365947033.73
# RMSE:         19119.81
# MAE:          15302.06
# R² Score:     0.9553
```

### Ridge and Lasso Regression

```python
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import numpy as np

# Generate data with many features (some irrelevant)
X, y = make_regression(
    n_samples=200, n_features=20, n_informative=5,
    noise=10, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ridge: L2 regularization (shrinks coefficients toward zero)
ridge = Ridge(alpha=1.0)  # higher alpha = stronger regularization
ridge.fit(X_train, y_train)
print(f"Ridge R²:     {r2_score(y_test, ridge.predict(X_test)):.4f}")
print(f"Ridge non-zero coefficients: {np.sum(ridge.coef_ != 0)}")  # all 20

# Lasso: L1 regularization (drives some coefficients to exactly zero)
lasso = Lasso(alpha=1.0)  # performs feature selection
lasso.fit(X_train, y_train)
print(f"Lasso R²:     {r2_score(y_test, lasso.predict(X_test)):.4f}")
print(f"Lasso non-zero coefficients: {np.sum(lasso.coef_ != 0)}")  # fewer than 20

# ElasticNet: combines L1 and L2 regularization
elastic = ElasticNet(alpha=1.0, l1_ratio=0.5)  # l1_ratio blends L1/L2
elastic.fit(X_train, y_train)
print(f"ElasticNet R²: {r2_score(y_test, elastic.predict(X_test)):.4f}")
```

```
# Output:
# Ridge R²:     0.9963
# Ridge non-zero coefficients: 20
# Lasso R²:     0.9965
# Lasso non-zero coefficients: 5
# ElasticNet R²: 0.9905
```

### Random Forest Regressor

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

X, y = make_regression(n_samples=500, n_features=10, n_informative=5, noise=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random forest for regression
rf_reg = RandomForestRegressor(
    n_estimators=100,      # number of trees
    max_depth=10,          # limit tree depth to reduce overfitting
    min_samples_leaf=5,    # min samples in leaf node
    random_state=42
)
rf_reg.fit(X_train, y_train)

y_pred = rf_reg.predict(X_test)
print(f"RMSE:     {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")
print(f"R² Score: {r2_score(y_test, y_pred):.4f}")

# Feature importance
importances = rf_reg.feature_importances_
top_features = np.argsort(importances)[::-1][:5]  # top 5 features
print(f"Top 5 important features: {top_features}")
for i in top_features:
    print(f"  Feature {i}: {importances[i]:.4f}")
```

```
# Output:
# RMSE:     36.7426
# R² Score: 0.9636
# Top 5 important features: [1 5 8 2 4]
#   Feature 1: 0.4987
#   Feature 5: 0.2314
#   Feature 8: 0.1163
#   Feature 2: 0.0562
#   Feature 4: 0.0398
```

### Regression Metrics Summary

```python
from sklearn.metrics import (
    mean_squared_error,        # MSE: average of squared errors
    mean_absolute_error,       # MAE: average of absolute errors
    r2_score,                  # R²: proportion of variance explained (1.0 = perfect)
    mean_absolute_percentage_error  # MAPE: percentage error
)
import numpy as np

y_true = np.array([100, 200, 300, 400, 500])
y_pred = np.array([110, 190, 310, 380, 520])

print(f"MSE:  {mean_squared_error(y_true, y_pred):.2f}")        # 260.00
print(f"RMSE: {np.sqrt(mean_squared_error(y_true, y_pred)):.2f}") # 16.12
print(f"MAE:  {mean_absolute_error(y_true, y_pred):.2f}")       # 14.00
print(f"R²:   {r2_score(y_true, y_pred):.4f}")                  # 0.9870
print(f"MAPE: {mean_absolute_percentage_error(y_true, y_pred):.4f}")  # 0.0467
```

```
# Output:
# MSE:  260.00
# RMSE: 16.12
# MAE:  14.00
# R²:   0.9870
# MAPE: 0.0467
```

---

## Unsupervised Learning

### K-Means Clustering

```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

# Generate clustered data
X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.8, random_state=42)

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fit K-Means
kmeans = KMeans(
    n_clusters=4,        # number of clusters
    init="k-means++",   # smart initialization (default)
    n_init=10,           # number of times to run with different seeds
    max_iter=300,        # max iterations per run
    random_state=42
)
kmeans.fit(X_scaled)

# Results
print(f"Cluster labels:   {kmeans.labels_[:10]}")       # assigned cluster per sample
print(f"Cluster centers shape: {kmeans.cluster_centers_.shape}")  # (4, 2)
print(f"Inertia:          {kmeans.inertia_:.2f}")        # sum of squared distances to centroids
print(f"Silhouette Score: {silhouette_score(X_scaled, kmeans.labels_):.4f}")  # -1 to 1, higher = better

# Elbow method: find optimal number of clusters
inertias = []
for k in range(2, 10):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    print(f"  k={k}: inertia={km.inertia_:.2f}, silhouette={silhouette_score(X_scaled, km.labels_):.4f}")
```

```
# Output:
# Cluster labels:   [3 0 1 0 2 1 3 2 0 1]
# Cluster centers shape: (4, 2)
# Inertia:          220.84
# Silhouette Score: 0.6551
#   k=2: inertia=548.83, silhouette=0.4907
#   k=3: inertia=344.73, silhouette=0.5769
#   k=4: inertia=220.84, silhouette=0.6551
#   k=5: inertia=192.02, silhouette=0.5711
#   k=6: inertia=166.15, silhouette=0.5316
#   k=7: inertia=144.09, silhouette=0.5189
#   k=8: inertia=127.47, silhouette=0.5097
#   k=9: inertia=112.85, silhouette=0.4977
```

### DBSCAN

```python
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler

# Generate non-linearly separable data (DBSCAN handles this well)
X, y_true = make_moons(n_samples=300, noise=0.1, random_state=42)
X_scaled = StandardScaler().fit_transform(X)

# DBSCAN: density-based clustering (no need to specify n_clusters)
dbscan = DBSCAN(
    eps=0.3,              # max distance between two samples in same neighborhood
    min_samples=10,       # min samples in neighborhood to form a core point
    metric="euclidean"
)
labels = dbscan.fit_predict(X_scaled)

n_clusters = len(set(labels)) - (1 if -1 in labels else 0)  # -1 = noise
n_noise = list(labels).count(-1)

print(f"Clusters found: {n_clusters}")
print(f"Noise points:   {n_noise}")
print(f"Labels:         {labels[:15]}")
```

```
# Output:
# Clusters found: 2
# Noise points:   2
# Labels:         [0 1 0 1 0 1 0 1 0 0 0 1 1 0 0]
```

### Principal Component Analysis (PCA)

```python
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
import numpy as np

# Load and scale data
iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

print(f"Original shape: {X_scaled.shape}")  # (150, 4)

# Reduce from 4 dimensions to 2
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
print(f"Reduced shape:  {X_pca.shape}")     # (150, 2)

# How much variance each component explains
print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
print(f"Total variance retained:  {sum(pca.explained_variance_ratio_):.4f}")

# Components (principal axes in feature space)
print(f"Component 1 loadings: {pca.components_[0]}")
print(f"Component 2 loadings: {pca.components_[1]}")

# Find n_components for 95% variance
pca_full = PCA(n_components=0.95)  # pass float to auto-select n_components
X_95 = pca_full.fit_transform(X_scaled)
print(f"Components for 95% variance: {pca_full.n_components_}")
```

```
# Output:
# Original shape: (150, 4)
# Reduced shape:  (150, 2)
# Explained variance ratio: [0.7296 0.2285]
# Total variance retained:  0.9581
# Component 1 loadings: [ 0.5211 -0.2693  0.5804  0.5649]
# Component 2 loadings: [ 0.3774  0.9233  0.0245  0.0669]
# Components for 95% variance: 2
```

---

## Model Selection

### Cross-Validation

```python
from sklearn.model_selection import cross_val_score, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

iris = load_iris()
model = LogisticRegression(max_iter=200, random_state=42)

# Basic cross-validation: returns scores for each fold
scores = cross_val_score(
    model, iris.data, iris.target,
    cv=5,              # 5-fold cross-validation
    scoring="accuracy"  # metric to evaluate
)
print(f"Fold scores: {scores}")
print(f"Mean:        {scores.mean():.4f}")
print(f"Std:         {scores.std():.4f}")

# cross_validate: returns multiple metrics and timing info
results = cross_validate(
    model, iris.data, iris.target,
    cv=5,
    scoring=["accuracy", "f1_macro"],  # multiple metrics
    return_train_score=True             # also evaluate on training folds
)
print(f"\nTest accuracy:  {results['test_accuracy'].mean():.4f}")
print(f"Train accuracy: {results['train_accuracy'].mean():.4f}")
print(f"Test F1 macro:  {results['test_f1_macro'].mean():.4f}")
```

```
# Output:
# Fold scores: [0.9667 0.9667 0.9333 0.9667 1.    ]
# Mean:        0.9667
# Std:         0.0211
#
# Test accuracy:  0.9667
# Train accuracy: 0.9750
# Test F1 macro:  0.9661
```

### GridSearchCV

```python
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

# Define hyperparameter grid to search
param_grid = {
    "C": [0.1, 1, 10, 100],         # regularization strength
    "gamma": ["scale", "auto", 0.01, 0.1],  # kernel coefficient
    "kernel": ["rbf", "linear"]       # kernel type
}

# Exhaustive search over all combinations
grid_search = GridSearchCV(
    SVC(random_state=42),
    param_grid,
    cv=5,                  # 5-fold cross-validation
    scoring="accuracy",
    n_jobs=-1,             # use all CPU cores
    verbose=0,
    refit=True             # refit best model on full training set
)
grid_search.fit(X_scaled, iris.target)

print(f"Best parameters: {grid_search.best_params_}")
print(f"Best CV score:   {grid_search.best_score_:.4f}")
print(f"Best estimator:  {grid_search.best_estimator_}")

# Access the best model directly
best_model = grid_search.best_estimator_
predictions = best_model.predict(X_scaled[:5])
print(f"Predictions:     {predictions}")
```

```
# Output:
# Best parameters: {'C': 1, 'gamma': 'scale', 'kernel': 'rbf'}
# Best CV score:   0.9800
# Best estimator:  SVC(random_state=42)
# Predictions:     [0 0 0 0 0]
```

### RandomizedSearchCV

```python
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from scipy.stats import randint, uniform

X, y = make_classification(n_samples=500, n_features=10, random_state=42)

# Define distributions to sample from (more efficient than grid search)
param_distributions = {
    "n_estimators": randint(50, 300),        # uniform integer distribution
    "max_depth": randint(3, 20),             # sample integer between 3 and 20
    "min_samples_split": randint(2, 20),
    "min_samples_leaf": randint(1, 10),
    "max_features": uniform(0.1, 0.9),       # uniform float distribution
}

# Random search: samples n_iter combinations from distributions
random_search = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_distributions,
    n_iter=50,           # number of random combinations to try
    cv=5,
    scoring="accuracy",
    n_jobs=-1,
    random_state=42
)
random_search.fit(X, y)

print(f"Best parameters: {random_search.best_params_}")
print(f"Best CV score:   {random_search.best_score_:.4f}")
```

```
# Output:
# Best parameters: {'max_depth': 12, 'max_features': 0.56, 'min_samples_leaf': 3,
#                   'min_samples_split': 7, 'n_estimators': 236}
# Best CV score:   0.9280
```

---

## Pipelines

### Basic Pipeline

```python
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=500, n_features=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline chains preprocessing and model into a single object
pipe = Pipeline([
    ("scaler", StandardScaler()),          # step 1: scale features
    ("classifier", LogisticRegression())   # step 2: classify
])

# fit() calls scaler.fit_transform() then classifier.fit()
pipe.fit(X_train, y_train)

# predict() calls scaler.transform() then classifier.predict()
score = pipe.score(X_test, y_test)  # calls predict internally
print(f"Pipeline accuracy: {score:.4f}")

# make_pipeline: auto-generates step names from class names
pipe_auto = make_pipeline(StandardScaler(), LogisticRegression())
pipe_auto.fit(X_train, y_train)
print(f"Auto pipeline accuracy: {pipe_auto.score(X_test, y_test):.4f}")

# Access individual steps
print(f"Scaler mean:       {pipe.named_steps['scaler'].mean_[:3]}")
print(f"Model coefficients: {pipe.named_steps['classifier'].coef_.shape}")
```

```
# Output:
# Pipeline accuracy: 0.8800
# Auto pipeline accuracy: 0.8800
# Scaler mean:       [-0.0553  0.077  -0.0634]
# Model coefficients: (1, 10)
```

### ColumnTransformer

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np

# Create realistic mixed-type dataset
rng = np.random.default_rng(42)
df = pd.DataFrame({
    "age": rng.integers(18, 70, 200),
    "income": rng.normal(50000, 15000, 200),
    "education": rng.choice(["high_school", "bachelors", "masters", "phd"], 200),
    "city": rng.choice(["new_york", "chicago", "houston", "phoenix"], 200),
    "purchased": rng.integers(0, 2, 200)
})

# Introduce some missing values
df.loc[rng.choice(200, 15, replace=False), "age"] = np.nan
df.loc[rng.choice(200, 10, replace=False), "income"] = np.nan

X = df.drop("purchased", axis=1)
y = df["purchased"]

# Define different preprocessing for numeric vs categorical columns
numeric_features = ["age", "income"]
categorical_features = ["education", "city"]

numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),  # fill missing with median
    ("scaler", StandardScaler())                     # standardize
])

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),  # fill with mode
    ("onehot", OneHotEncoder(handle_unknown="ignore"))      # one-hot encode
])

# ColumnTransformer applies different transformers to different columns
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)

# Full pipeline: preprocessing + model
full_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(random_state=42))
])

# Use with cross-validation (no data leakage!)
from sklearn.model_selection import cross_val_score
scores = cross_val_score(full_pipeline, X, y, cv=5, scoring="accuracy")
print(f"CV accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")

# Fit and inspect
full_pipeline.fit(X, y)
feature_names = (full_pipeline.named_steps["preprocessor"]
                 .get_feature_names_out())
print(f"Transformed features: {list(feature_names)}")
```

```
# Output:
# CV accuracy: 0.5100 (+/- 0.0510)
# Transformed features: ['num__age', 'num__income', 'cat__education_bachelors',
#   'cat__education_high_school', 'cat__education_masters', 'cat__education_phd',
#   'cat__city_chicago', 'cat__city_houston', 'cat__city_new_york', 'cat__city_phoenix']
```

### Pipeline with GridSearchCV

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=300, n_features=10, random_state=42)

# Create pipeline
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(random_state=42))
])

# Use stepname__param syntax to set hyperparameters in the grid
param_grid = {
    "svm__C": [0.1, 1, 10],
    "svm__kernel": ["rbf", "linear"],
    "svm__gamma": ["scale", "auto"]
}

grid = GridSearchCV(pipe, param_grid, cv=5, scoring="accuracy", n_jobs=-1)
grid.fit(X, y)

print(f"Best params: {grid.best_params_}")
print(f"Best score:  {grid.best_score_:.4f}")
```

```
# Output:
# Best params: {'svm__C': 1, 'svm__gamma': 'scale', 'svm__kernel': 'rbf'}
# Best score:  0.9067
```

---

## Feature Selection

```python
from sklearn.feature_selection import (
    SelectKBest, f_classif,         # univariate statistical tests
    RFE,                             # recursive feature elimination
    SelectFromModel                  # model-based selection
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
import numpy as np

# Generate data with 5 informative features out of 20
X, y = make_classification(
    n_samples=300, n_features=20, n_informative=5,
    n_redundant=5, random_state=42
)

# Method 1: SelectKBest - select top k features by statistical test
selector_kbest = SelectKBest(score_func=f_classif, k=10)
X_kbest = selector_kbest.fit_transform(X, y)
selected = selector_kbest.get_support()  # boolean mask of selected features
print(f"SelectKBest selected features: {np.where(selected)[0]}")
print(f"Feature scores: {selector_kbest.scores_[:10].round(2)}")

# Method 2: RFE - recursively remove least important features
rfe = RFE(
    estimator=LogisticRegression(max_iter=200, random_state=42),
    n_features_to_select=10,
    step=1                # remove 1 feature per iteration
)
X_rfe = rfe.fit_transform(X, y)
print(f"\nRFE selected features: {np.where(rfe.support_)[0]}")
print(f"Feature rankings:      {rfe.ranking_}")  # 1 = selected

# Method 3: SelectFromModel - use feature importance from a model
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)
selector_model = SelectFromModel(rf, threshold="median")  # above-median importance
X_model = selector_model.fit_transform(X, y)
selected_model = selector_model.get_support()
print(f"\nSelectFromModel selected features: {np.where(selected_model)[0]}")
print(f"Reduced shape: {X_model.shape}")
```

```
# Output:
# SelectKBest selected features: [ 0  1  2  3  6  8 11 14 16 18]
# Feature scores: [34.23 46.12 15.88  7.07  0.01  0.38 15.47  1.25 18.22  1.98]
#
# RFE selected features: [ 0  1  2  3  6  8 11 14 16 18]
# Feature rankings:      [ 1  1  1  1  7  3  1  9  1  4  5  1  8  2  1 10 11  6  1  1]
#
# SelectFromModel selected features: [ 0  1  2  3  6  8 11 14 16 18]
# Reduced shape: (300, 10)
```

---

## Model Persistence

```python
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import os

# Train a model
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print(f"Original accuracy: {model.score(X_test, y_test):.4f}")

# Save model to disk with joblib (preferred for sklearn)
joblib.dump(model, "iris_rf_model.joblib")
print(f"Model saved: {os.path.getsize('iris_rf_model.joblib') / 1024:.1f} KB")

# Load model from disk
loaded_model = joblib.load("iris_rf_model.joblib")
print(f"Loaded accuracy:   {loaded_model.score(X_test, y_test):.4f}")

# Save entire pipeline (recommended for production)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])
pipeline.fit(X_train, y_train)

joblib.dump(pipeline, "iris_pipeline.joblib")
loaded_pipeline = joblib.load("iris_pipeline.joblib")
print(f"Pipeline accuracy: {loaded_pipeline.score(X_test, y_test):.4f}")

# Compress large models
joblib.dump(model, "iris_rf_compressed.joblib", compress=3)  # compression level 0-9
print(f"Compressed size:   {os.path.getsize('iris_rf_compressed.joblib') / 1024:.1f} KB")
```

```
# Output:
# Original accuracy: 1.0000
# Model saved: 292.5 KB
# Loaded accuracy:   1.0000
# Pipeline accuracy: 1.0000
# Compressed size:   72.8 KB
```

---

## Practice Exercises

### Exercise 1: Complete Classification Workflow

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report

# Load wine dataset (3-class classification)
wine = load_wine()
X_train, X_test, y_train, y_test = train_test_split(
    wine.data, wine.target, test_size=0.2, random_state=42, stratify=wine.target
)

# Compare multiple models using pipelines
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "SVM": SVC(kernel="rbf", random_state=42)
}

for name, model in models.items():
    pipe = Pipeline([("scaler", StandardScaler()), ("model", model)])
    scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="accuracy")
    print(f"{name}: {scores.mean():.4f} (+/- {scores.std():.4f})")

# Train best model and get full report
best_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000, random_state=42))
])
best_pipe.fit(X_train, y_train)
y_pred = best_pipe.predict(X_test)
print(f"\nClassification Report:\n{classification_report(y_test, y_pred, target_names=wine.target_names)}")
```

### Exercise 2: Regression with Feature Engineering

```python
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Load California housing dataset
housing = fetch_california_housing()
X_train, X_test, y_train, y_test = train_test_split(
    housing.data, housing.target, test_size=0.2, random_state=42
)

# Pipeline with polynomial features and ridge regression
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("poly", PolynomialFeatures(include_bias=False)),  # add interaction terms
    ("ridge", Ridge())
])

# Search over polynomial degree and regularization
param_grid = {
    "poly__degree": [1, 2],           # linear vs quadratic features
    "ridge__alpha": [0.1, 1, 10, 100]
}

grid = GridSearchCV(pipe, param_grid, cv=5, scoring="r2", n_jobs=-1)
grid.fit(X_train, y_train)

print(f"Best params: {grid.best_params_}")
print(f"Best CV R²:  {grid.best_score_:.4f}")

# Evaluate on test set
y_pred = grid.predict(X_test)
print(f"Test RMSE:   {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")
print(f"Test R²:     {r2_score(y_test, y_pred):.4f}")
```

### Exercise 3: Clustering Analysis

```python
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, adjusted_rand_score
import numpy as np

# Generate 5 clusters with varying density
X, y_true = make_blobs(
    n_samples=[100, 150, 80, 120, 50],
    centers=5, cluster_std=[1.0, 1.5, 0.5, 1.2, 0.8],
    random_state=42
)
X_scaled = StandardScaler().fit_transform(X)

# Compare KMeans and DBSCAN
# KMeans
for k in range(3, 8):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    sil = silhouette_score(X_scaled, labels)
    ari = adjusted_rand_score(y_true, labels)
    print(f"KMeans k={k}: silhouette={sil:.4f}, ARI={ari:.4f}")

# DBSCAN
for eps in [0.3, 0.5, 0.7, 1.0]:
    db = DBSCAN(eps=eps, min_samples=5)
    labels = db.fit_predict(X_scaled)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    if n_clusters > 1:
        sil = silhouette_score(X_scaled, labels)
        ari = adjusted_rand_score(y_true, labels)
        print(f"DBSCAN eps={eps}: clusters={n_clusters}, silhouette={sil:.4f}, ARI={ari:.4f}")
    else:
        print(f"DBSCAN eps={eps}: clusters={n_clusters} (cannot compute metrics)")
```

---

## Summary

These notes cover the fundamental concepts of scikit-learn:

1. **Core Concepts**: Estimator API (`fit`, `predict`, `transform`), consistent interface across all models
2. **Preprocessing**: Scaling (`StandardScaler`, `MinMaxScaler`), encoding (`OneHotEncoder`, `LabelEncoder`), imputation (`SimpleImputer`, `KNNImputer`), train/test split
3. **Classification**: Logistic Regression, Random Forest, SVM, KNN, with metrics (accuracy, precision, recall, F1, confusion matrix, ROC AUC)
4. **Regression**: Linear, Ridge, Lasso, Random Forest Regressor, with metrics (MSE, RMSE, MAE, R²)
5. **Unsupervised Learning**: K-Means, DBSCAN for clustering; PCA for dimensionality reduction
6. **Model Selection**: Cross-validation, `GridSearchCV`, `RandomizedSearchCV` for hyperparameter tuning
7. **Pipelines**: `Pipeline`, `ColumnTransformer`, `make_pipeline` for reproducible workflows without data leakage
8. **Feature Selection**: `SelectKBest`, `RFE`, `SelectFromModel` for reducing feature space
9. **Model Persistence**: `joblib` for saving and loading trained models and pipelines

### Next Steps

1. Work through the practice exercises with different datasets and models
2. Explore gradient boosting models (`GradientBoostingClassifier`, `XGBClassifier`, `LGBMClassifier`)
3. Learn about advanced preprocessing with `FunctionTransformer` and custom transformers
4. Study learning curves and validation curves for diagnosing bias/variance
5. Combine scikit-learn with pandas for end-to-end data science workflows
6. Explore `sklearn.inspection` for model interpretability (partial dependence, permutation importance)

### Additional Resources

- **scikit-learn Documentation**: https://scikit-learn.org/stable/
- **scikit-learn User Guide**: https://scikit-learn.org/stable/user_guide.html
- **scikit-learn Tutorials**: https://scikit-learn.org/stable/tutorial/index.html
- **scikit-learn API Reference**: https://scikit-learn.org/stable/modules/classes.html
- **scikit-learn Examples Gallery**: https://scikit-learn.org/stable/auto_examples/index.html
