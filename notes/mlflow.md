# Introduction to MLflow

## Table of Contents

- [What is MLflow](#what-is-mlflow)
- [Installation](#installation)
- [Tracking](#tracking)
- [MLflow UI](#mlflow-ui)
- [Model Registry](#model-registry)
- [Projects](#projects)
- [Models](#models)
- [Serving](#serving)
- [Integration with ML Frameworks](#integration-with-ml-frameworks)
- [Search and Compare Runs](#search-and-compare-runs)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is MLflow

MLflow is an open-source platform for managing the end-to-end machine learning lifecycle. It provides tools for experiment tracking, model packaging, versioning, and deployment.

Key components:
- **Tracking**: Record and query experiments (parameters, metrics, artifacts)
- **Projects**: Package ML code for reproducible runs
- **Models**: Manage and deploy models from various ML libraries
- **Model Registry**: Centralized model store with versioning and stage transitions

---

## Installation

```python
# Install MLflow
# pip install mlflow

# Install with extras
# pip install mlflow[extras]         # includes scikit-learn, boto3, etc.

import mlflow
print(mlflow.__version__)  # prints the installed version
```

---

## Tracking

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

# Set the tracking URI (default is local ./mlruns directory)
mlflow.set_tracking_uri("http://localhost:5000")  # remote tracking server

# Create or set an experiment
mlflow.set_experiment("iris-classification")

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# Start a run to track an experiment
with mlflow.start_run(run_name="random_forest_v1"):
    n_estimators = 100
    max_depth = 5

    # Log parameters - the inputs to your model
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)

    # Train the model
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    model.fit(X_train, y_train)

    # Log metrics - the results
    predictions = model.predict(X_test)
    mlflow.log_metric("accuracy", accuracy_score(y_test, predictions))
    mlflow.log_metric("f1_score", f1_score(y_test, predictions, average="weighted"))

    # Log the model as an artifact
    mlflow.sklearn.log_model(model, "model")
    print(f"Run ID: {mlflow.active_run().info.run_id}")
```

```python
import mlflow

# Logging various types of data
with mlflow.start_run(run_name="artifact_examples"):
    # Log multiple parameters at once
    mlflow.log_params({"batch_size": 32, "epochs": 50, "optimizer": "adam"})

    # Log metrics over time (step parameter for tracking progress)
    for epoch in range(10):
        mlflow.log_metric("train_loss", 1.0 / (epoch + 1), step=epoch)

    # Log file artifacts
    with open("config.json", "w") as f:
        import json
        json.dump({"model_type": "transformer"}, f)
    mlflow.log_artifact("config.json")

    # Log an entire directory
    # mlflow.log_artifacts("output_dir/", artifact_path="results")

    # Set tags for organizing runs
    mlflow.set_tag("model_type", "random_forest")
    mlflow.set_tag("team", "ml-platform")
```

```python
import mlflow

# Autologging - automatically logs parameters, metrics, and models
mlflow.sklearn.autolog()  # enable for scikit-learn

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split

wine = load_wine()
X_train, X_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.2)

with mlflow.start_run():
    model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1)
    model.fit(X_train, y_train)
    # Autolog captures all params, metrics, model, feature importance, etc.

# Enable for all supported frameworks at once
mlflow.autolog()
# Supported: sklearn, pytorch, tensorflow, keras, xgboost, lightgbm, etc.
```

---

## MLflow UI

```python
# Start the MLflow UI
# mlflow ui                                 # default port 5000
# mlflow ui --port 8080                     # custom port
# mlflow ui --backend-store-uri sqlite:///mlflow.db

# UI Features:
# - Experiments page: list all experiments and their runs
# - Run details: view params, metrics, artifacts, metric history charts
# - Compare runs: parallel coordinates plot, scatter plots, table comparison
# - Search: filter runs by params/metrics/tags
#   Example: metrics.accuracy > 0.9 AND params.model_type = "random_forest"

# Starting a tracking server for team collaboration:
# mlflow server \
#   --backend-store-uri postgresql://user:pass@host/mlflow \
#   --default-artifact-root s3://my-bucket/artifacts \
#   --host 0.0.0.0 --port 5000
```

---

## Model Registry

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

mlflow.set_tracking_uri("http://localhost:5000")

# Register a model during logging
with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    mlflow.sklearn.log_model(
        model, "model",
        registered_model_name="iris-classifier"  # registers the model
    )

# Or register an existing run's model
result = mlflow.register_model("runs:/<run_id>/model", "iris-classifier")
```

```python
from mlflow import MlflowClient

client = MlflowClient()

# Transition model versions through stages
# Available: "None", "Staging", "Production", "Archived"
client.transition_model_version_stage(
    name="iris-classifier", version=1, stage="Staging"
)

client.transition_model_version_stage(
    name="iris-classifier", version=1, stage="Production",
    archive_existing_versions=True  # archive other Production versions
)

# Add descriptions and tags
client.update_model_version(
    name="iris-classifier", version=1,
    description="Random Forest, accuracy=0.95"
)

# Load a model by stage or version
model = mlflow.sklearn.load_model("models:/iris-classifier/Production")
model_v1 = mlflow.sklearn.load_model("models:/iris-classifier/1")
```

```python
from mlflow import MlflowClient

client = MlflowClient()

# Using aliases (MLflow 2.x) instead of stages
client.set_registered_model_alias("iris-classifier", "champion", version=1)
client.set_registered_model_alias("iris-classifier", "challenger", version=2)

# Load by alias
champion = mlflow.sklearn.load_model("models:/iris-classifier@champion")
challenger = mlflow.sklearn.load_model("models:/iris-classifier@challenger")

# Get alias details
info = client.get_model_version_by_alias("iris-classifier", "champion")
print(f"Champion is version {info.version}")
```

---

## Projects

```python
# MLflow Projects package code for reproducible runs

# MLproject file (YAML at project root):
# name: my-ml-project
# conda_env: conda.yaml
# entry_points:
#   main:
#     parameters:
#       learning_rate: {type: float, default: 0.01}
#       epochs: {type: int, default: 10}
#     command: "python train.py --lr {learning_rate} --epochs {epochs}"

# conda.yaml:
# name: my-ml-env
# dependencies:
#   - python=3.11
#   - pip:
#     - mlflow>=2.0
#     - scikit-learn>=1.3
```

```python
import mlflow

# Run a project locally
mlflow.projects.run(
    uri=".",                          # current directory
    entry_point="main",
    parameters={"learning_rate": 0.05, "epochs": 20},
    experiment_name="iris-classification"
)

# Run from a Git repository
mlflow.projects.run(
    uri="https://github.com/user/ml-project.git",
    entry_point="main",
    parameters={"learning_rate": 0.1},
    version="main"
)

# CLI equivalent:
# mlflow run . -P learning_rate=0.05 -P epochs=20
# mlflow run https://github.com/user/ml-project.git -P learning_rate=0.1
```

---

## Models

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from mlflow.models.signature import infer_signature

iris = load_iris()
model = RandomForestClassifier(n_estimators=100)
model.fit(iris.data[:120], iris.target[:120])
predictions = model.predict(iris.data[120:])

# Infer model signature (input/output schema)
signature = infer_signature(iris.data[120:], predictions)

with mlflow.start_run():
    mlflow.sklearn.log_model(
        model, "model",
        signature=signature,                 # defines expected input/output
        input_example=iris.data[120:123],   # example input for docs
        registered_model_name="iris-rf"
    )

# Load with framework-agnostic pyfunc flavor
pyfunc_model = mlflow.pyfunc.load_model("runs:/<run_id>/model")
predictions = pyfunc_model.predict(iris.data[120:])
```

```python
import mlflow
import mlflow.pyfunc

# Custom model with PythonModel
class CustomModel(mlflow.pyfunc.PythonModel):

    def __init__(self, multiplier=2.0):
        self.multiplier = multiplier

    def predict(self, context, model_input, params=None):
        return model_input * self.multiplier

with mlflow.start_run():
    mlflow.pyfunc.log_model(
        artifact_path="model",
        python_model=CustomModel(multiplier=3.0),
        registered_model_name="custom-model"
    )

# Load and use
import pandas as pd
loaded = mlflow.pyfunc.load_model("models:/custom-model/1")
result = loaded.predict(pd.DataFrame({"value": [1.0, 2.0, 3.0]}))
```

---

## Serving

```python
# Serve a model as a REST API
# mlflow models serve -m "models:/iris-classifier/Production" --port 5001
# mlflow models serve -m "runs:/<run_id>/model" --port 5001
# Options: --host 0.0.0.0, --no-conda, --env-manager local
```

```python
import requests

# Making predictions via the REST API
url = "http://localhost:5001/invocations"

# split-orient format
payload = {
    "dataframe_split": {
        "columns": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
        "data": [[5.1, 3.5, 1.4, 0.2], [6.7, 3.1, 4.7, 1.5]]
    }
}

response = requests.post(url, json=payload,
                         headers={"Content-Type": "application/json"})
print(response.json())  # {"predictions": [0, 1]}

# Build a Docker image for serving
# mlflow models build-docker -m "models:/iris-classifier/Production" \
#   -n "iris-image" --enable-mlserver
# docker run -p 5001:8080 iris-image
```

---

## Integration with ML Frameworks

```python
# scikit-learn
import mlflow
mlflow.sklearn.autolog()

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

with mlflow.start_run():
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=200))
    ])
    pipeline.fit(X_train, y_train)
    # Autolog captures params, metrics, model, confusion matrix
```

```python
# PyTorch
import mlflow
import mlflow.pytorch
import torch
import torch.nn as nn

mlflow.pytorch.autolog()

class SimpleNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        return self.fc2(self.relu(self.fc1(x)))

with mlflow.start_run():
    model = SimpleNet(4, 16, 3)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(50):
        X_batch = torch.randn(32, 4)
        y_batch = torch.randint(0, 3, (32,))
        loss = criterion(model(X_batch), y_batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        mlflow.log_metric("train_loss", loss.item(), step=epoch)

    mlflow.pytorch.log_model(model, "model")
```

```python
# TensorFlow / Keras (autolog captures architecture, params, per-epoch metrics)
import mlflow
mlflow.tensorflow.autolog()

# import tensorflow as tf
# model = tf.keras.Sequential([...])
# model.compile(optimizer="adam", loss="sparse_categorical_crossentropy")
# model.fit(X_train, y_train, epochs=50, validation_split=0.2)
```

---

## Search and Compare Runs

```python
import mlflow

# Search runs with filter expressions
runs = mlflow.search_runs(
    experiment_names=["iris-classification"],
    filter_string="metrics.accuracy > 0.9",
    order_by=["metrics.accuracy DESC"],
    max_results=10
)
# Returns a pandas DataFrame
print(runs[["run_id", "params.n_estimators", "metrics.accuracy"]])

# Complex filters
runs = mlflow.search_runs(
    experiment_names=["iris-classification"],
    filter_string=(
        "metrics.accuracy > 0.85 "
        "AND params.n_estimators = '100' "
        "AND tags.model_type = 'random_forest'"
    )
)

# Find the best run
best = runs.loc[runs["metrics.accuracy"].idxmax()]
print(f"Best run: {best['run_id']}, accuracy: {best['metrics.accuracy']}")
```

```python
from mlflow import MlflowClient

client = MlflowClient()

# Detailed run information
run = client.get_run("<run_id>")
print(f"Status: {run.info.status}")
print(f"Params: {run.data.params}")
print(f"Metrics: {run.data.metrics}")

# Metric history for step-logged metrics
history = client.get_metric_history("<run_id>", "train_loss")
for m in history:
    print(f"Step {m.step}: {m.value}")

# List and download artifacts
artifacts = client.list_artifacts("<run_id>")
client.download_artifacts("<run_id>", "model", dst_path="./downloaded")
```

---

## Practice Exercises

1. **Experiment Tracking**: Train multiple models on the same dataset, log parameters, metrics, and models. Compare in the UI.

2. **Hyperparameter Search**: Perform grid or random search, logging each combination as a separate run. Find the best config with `search_runs`.

3. **Model Registry Workflow**: Train, register, transition through stages (Staging -> Production), and load the Production model.

4. **Custom Model**: Create a `PythonModel` wrapping an ensemble with custom preprocessing in `predict`.

5. **Model Serving**: Deploy a model as a REST API and write a client that sends prediction requests.

---

## Summary

MLflow is a comprehensive platform for managing the machine learning lifecycle. Key takeaways:

- **Tracking** records experiments with parameters, metrics, artifacts, and tags
- **Autologging** captures training details automatically for supported frameworks
- **Model Registry** provides centralized management with versioning, stages, and aliases
- **Projects** package ML code with environments for reproducible execution
- **Models** support multiple flavors (sklearn, pytorch, tensorflow, pyfunc) with signatures
- **Serving** deploys models as REST APIs via CLI, Docker, or cloud platforms
- **Search API** enables programmatic querying and comparison of runs

---

## Next Steps

- Explore MLflow Evaluate for model quality assessment
- Learn about MLflow Recipes for structured ML workflows
- Study integration with feature stores (Feast, Tecton)
- Investigate MLflow on Databricks for managed experiences
- Look into A/B testing patterns with the Model Registry

---

## Additional Resources

- [MLflow Official Documentation](https://mlflow.org/docs/latest/)
- [MLflow GitHub Repository](https://github.com/mlflow/mlflow)
- [MLflow Tutorials](https://mlflow.org/docs/latest/tutorials-and-examples/)
- [MLflow Model Registry Guide](https://mlflow.org/docs/latest/model-registry.html)
- [Databricks MLflow Guide](https://docs.databricks.com/mlflow/index.html)
