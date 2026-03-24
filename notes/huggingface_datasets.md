# Introduction to HuggingFace Datasets

## Table of Contents

1. [What is HuggingFace Datasets?](#what-is-huggingface-datasets)
2. [Installation](#installation)
3. [Loading Datasets](#loading-datasets)
4. [Exploring Datasets](#exploring-datasets)
5. [Data Processing](#data-processing)
6. [Streaming](#streaming)
7. [Creating Datasets](#creating-datasets)
8. [Data Formatting](#data-formatting)
9. [Combining Datasets](#combining-datasets)
10. [Pushing to Hub](#pushing-to-hub)
11. [Metrics and Evaluation](#metrics-and-evaluation)
12. [Practice Exercises](#practice-exercises)
13. [Summary](#summary)

---

## What is HuggingFace Datasets?

HuggingFace Datasets is an efficient library for loading, processing, and sharing datasets. It provides:

- **Thousands of Datasets**: Access datasets from the HuggingFace Hub with a single line
- **Apache Arrow Backend**: Memory-mapped storage for fast, memory-efficient data access
- **Smart Caching**: Processed datasets are cached to avoid redundant computation
- **Streaming Mode**: Process datasets too large to fit in memory
- **Interoperability**: Convert to/from Pandas, PyTorch, TensorFlow, and NumPy
- **Hub Integration**: Upload and share datasets with the community

---

## Installation

```bash
# Install the datasets library
pip install datasets

# Install with audio/vision support
pip install datasets[audio,vision]

# Install the evaluate library (successor to load_metric)
pip install evaluate
```

```python
import datasets

print(datasets.__version__)  # e.g., 2.18.0
```

---

## Loading Datasets

### From the HuggingFace Hub

```python
from datasets import load_dataset

# Load a popular dataset by name
dataset = load_dataset("imdb")
print(dataset)
# DatasetDict({
#     train: Dataset({features: ['text', 'label'], num_rows: 25000}),
#     test:  Dataset({features: ['text', 'label'], num_rows: 25000})
# })

# Load a specific split
train_data = load_dataset("imdb", split="train")

# Load a subset of rows (useful for quick testing)
small_train = load_dataset("imdb", split="train[:100]")   # first 100 rows
percentage  = load_dataset("imdb", split="train[:10%]")    # first 10%
last_500    = load_dataset("imdb", split="train[-500:]")   # last 500 rows
```

### From Local Files

```python
from datasets import load_dataset

# Load from CSV, JSON, or Parquet files
csv_dataset     = load_dataset("csv", data_files="data.csv")
json_dataset    = load_dataset("json", data_files="data.jsonl")
parquet_dataset = load_dataset("parquet", data_files="data.parquet")

# Load multiple files into train/test splits
csv_dataset = load_dataset("csv", data_files={"train": "train.csv", "test": "test.csv"})

# Load from a directory of text files
text_dataset = load_dataset("text", data_files="texts/*.txt")

# Load from a private Hub dataset (requires authentication)
dataset = load_dataset("my-org/private-dataset", token="hf_your_token")
```

---

## Exploring Datasets

```python
from datasets import load_dataset

dataset = load_dataset("imdb", split="train")

# Basic properties
print(len(dataset))           # 25000
print(dataset.column_names)   # ['text', 'label']
print(dataset.shape)          # (25000, 2)
print(dataset.features)
# {'text': Value(dtype='string'), 'label': ClassLabel(names=['neg', 'pos'])}
```

### Indexing and Slicing

```python
from datasets import load_dataset

dataset = load_dataset("imdb", split="train")

# Single row (returns a dict)
row = dataset[0]             # {'text': 'I rented...', 'label': 0}

# Single column (returns a list)
labels = dataset["label"]    # [0, 0, 0, 1, ...]

# Slice multiple rows (returns dict of lists)
batch = dataset[10:15]       # 5 rows
print(batch["text"])

# Select by index list
selected = dataset[[0, 42, 999]]

# Iterate over rows
for i, row in enumerate(dataset):
    if i >= 3:
        break
    print(f"Label: {row['label']}, Text: {row['text'][:50]}...")
```

### Class Labels

```python
from datasets import load_dataset

dataset = load_dataset("imdb", split="train")

label_feature = dataset.features["label"]
print(label_feature.names)       # ['neg', 'pos']
print(label_feature.num_classes) # 2
print(label_feature.int2str(0))  # 'neg'
print(label_feature.str2int("pos"))  # 1
```

---

## Data Processing

### Map

```python
from datasets import load_dataset

dataset = load_dataset("imdb", split="train")

# Apply a function to each row
def add_length(example):
    example["text_length"] = len(example["text"])  # add a new column
    return example

dataset = dataset.map(add_length)

# Batched mapping (much faster for tokenization)
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize_batch(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)

tokenized = dataset.map(tokenize_batch, batched=True, batch_size=1000)

# Parallel processing with num_proc
tokenized = dataset.map(tokenize_batch, batched=True, num_proc=4)

# Remove columns during map
tokenized = dataset.map(tokenize_batch, batched=True, remove_columns=["text"])
```

### Filter

```python
from datasets import load_dataset

dataset = load_dataset("imdb", split="train")

# Keep only positive reviews
positive = dataset.filter(lambda x: x["label"] == 1)
print(len(positive))  # ~12500

# Filter by text length
long_reviews = dataset.filter(lambda x: len(x["text"]) > 500)

# Batched filtering
positive_batched = dataset.filter(
    lambda batch: [label == 1 for label in batch["label"]],
    batched=True
)
```

### Select, Sort, Shuffle

```python
from datasets import load_dataset

dataset = load_dataset("imdb", split="train")

subset  = dataset.select(range(100))              # first 100 rows
specific = dataset.select([0, 42, 999, 5000])     # specific indices
sorted_ds = dataset.sort("label")                 # sort ascending
shuffled = dataset.shuffle(seed=42)                # shuffle with seed
sample   = dataset.shuffle(seed=42).select(range(1000))  # random sample
```

### Rename, Remove, Flatten

```python
from datasets import load_dataset

dataset = load_dataset("imdb", split="train")

# Rename and remove columns
renamed = dataset.rename_column("label", "sentiment")
trimmed = dataset.remove_columns(["text"])

# Flatten nested features
squad = load_dataset("squad", split="train")
flat = squad.flatten()
print(flat.column_names)
# ['id', 'title', 'context', 'question', 'answers.text', 'answers.answer_start']
```

### Train/Test Split

```python
from datasets import load_dataset

dataset = load_dataset("imdb", split="train")

split = dataset.train_test_split(test_size=0.2, seed=42)
print(split)
# DatasetDict({ train: 20000 rows, test: 5000 rows })

# Stratified split (preserves label distribution)
split = dataset.train_test_split(test_size=0.2, seed=42, stratify_by_column="label")
```

---

## Streaming

```python
from datasets import load_dataset, Dataset

# Stream a large dataset without downloading entirely
stream = load_dataset("c4", "en", split="train", streaming=True)

# Iterate one example at a time
for i, example in enumerate(stream):
    print(example["text"][:80])
    if i >= 4:
        break

# Transformations on streams (map, filter, take, skip, shuffle)
filtered = stream.filter(lambda x: len(x["text"]) > 100)
mapped   = stream.map(lambda x: {"upper": x["text"].upper()})
first_1k = stream.take(1000)
after_100 = stream.skip(100)
shuffled = stream.shuffle(seed=42, buffer_size=10000)  # approximate shuffle

# Convert streamed examples to a regular Dataset
examples = list(stream.take(500))
small_ds = Dataset.from_list(examples)
```

---

## Creating Datasets

### From Dictionaries and Lists

```python
from datasets import Dataset

# From a dict of lists
data = {"text": ["Hello", "Goodbye", "Hi"], "label": [1, 0, 1]}
dataset = Dataset.from_dict(data)
print(dataset[0])  # {'text': 'Hello', 'label': 1}

# From a list of dicts (each dict = one row)
records = [
    {"text": "First", "label": 0},
    {"text": "Second", "label": 1},
]
dataset = Dataset.from_list(records)
```

### From Pandas

```python
import pandas as pd
from datasets import Dataset

df = pd.DataFrame({
    "sentence": ["The cat sat.", "Dogs are great.", "Birds fly."],
    "sentiment": [0.5, 0.9, 0.7]
})

dataset = Dataset.from_pandas(df)
df_back = dataset.to_pandas()  # convert back
```

### From a Generator

```python
from datasets import Dataset

def my_generator():
    for i in range(10000):
        yield {"id": i, "text": f"Example {i}", "value": i * 0.1}

dataset = Dataset.from_generator(my_generator)
print(len(dataset))  # 10000
```

---

## Data Formatting

```python
from datasets import load_dataset

dataset = load_dataset("imdb", split="train[:100]")

# Set output format: "torch", "tensorflow", "numpy", "pandas"
dataset.set_format(type="torch", columns=["label"])
print(type(dataset[0]["label"]))  # <class 'torch.Tensor'>

# Reset to default Python format
dataset.reset_format()

# with_format returns a new view without modifying the original
torch_ds = dataset.with_format("torch", columns=["label"])
print(type(torch_ds[0]["label"]))  # torch.Tensor
print(type(dataset[0]["label"]))   # int (original unchanged)
```

### Using with PyTorch DataLoader

```python
from datasets import load_dataset
from torch.utils.data import DataLoader
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
dataset = load_dataset("imdb", split="train[:1000]")

def tokenize_fn(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)

tokenized = dataset.map(tokenize_fn, batched=True, remove_columns=["text"])
tokenized = tokenized.rename_column("label", "labels")
tokenized.set_format("torch")

loader = DataLoader(tokenized, batch_size=16, shuffle=True)

for batch in loader:
    print(batch["input_ids"].shape)  # torch.Size([16, 128])
    print(batch["labels"].shape)     # torch.Size([16])
    break
```

---

## Combining Datasets

```python
from datasets import load_dataset, concatenate_datasets, interleave_datasets

train = load_dataset("imdb", split="train")
test  = load_dataset("imdb", split="test")

# Concatenate along rows (must have same columns)
combined = concatenate_datasets([train, test])
print(len(combined))  # 50000

# Interleave rows from multiple datasets (round-robin)
ds1 = load_dataset("imdb", split="train[:1000]")
ds2 = load_dataset("imdb", split="test[:1000]")
interleaved = interleave_datasets([ds1, ds2])

# Weighted interleaving
weighted = interleave_datasets(
    [ds1, ds2],
    probabilities=[0.7, 0.3],  # 70% from ds1, 30% from ds2
    seed=42
)
```

---

## Pushing to Hub

```python
from datasets import Dataset, DatasetDict, load_from_disk
from huggingface_hub import login

login(token="hf_your_token_here")

# Push a dataset to the Hub
dataset = Dataset.from_dict({"text": ["a", "b"], "label": [0, 1]})
dataset.push_to_hub("my-username/my-dataset")

# Push with train/test splits
ds_dict = DatasetDict({
    "train": Dataset.from_dict({"text": ["a", "b"], "label": [0, 1]}),
    "test":  Dataset.from_dict({"text": ["c"], "label": [1]})
})
ds_dict.push_to_hub("my-username/my-dataset-splits")

# Make it private
dataset.push_to_hub("my-username/private-data", private=True)
```

### Saving and Loading Locally

```python
from datasets import load_dataset, load_from_disk

dataset = load_dataset("imdb", split="train")

# Save to disk (Arrow format, fast reload)
dataset.save_to_disk("./saved_imdb")
reloaded = load_from_disk("./saved_imdb")

# Export to common formats
dataset.to_csv("imdb.csv")
dataset.to_json("imdb.jsonl")
dataset.to_parquet("imdb.parquet")
```

---

## Metrics and Evaluation

### Using the Evaluate Library

```python
import evaluate

# Load and compute accuracy
accuracy = evaluate.load("accuracy")
result = accuracy.compute(predictions=[0, 1, 1, 0, 1], references=[0, 1, 0, 0, 1])
print(result)  # {'accuracy': 0.8}

# F1, precision, recall
f1 = evaluate.load("f1")
print(f1.compute(predictions=[0, 1, 1, 0], references=[0, 1, 0, 0], average="binary"))

precision = evaluate.load("precision")
recall    = evaluate.load("recall")
print(precision.compute(predictions=[0, 1, 1], references=[0, 1, 0]))
print(recall.compute(predictions=[0, 1, 1], references=[0, 1, 0]))
```

### Combining Metrics

```python
import evaluate

clf_metrics = evaluate.combine(["accuracy", "f1", "precision", "recall"])
results = clf_metrics.compute(
    predictions=[0, 1, 1, 0, 1, 0, 1, 1],
    references=[0, 1, 0, 0, 1, 1, 1, 1]
)
print(results)  # {'accuracy': 0.75, 'f1': 0.8, ...}
```

### NLP-Specific Metrics

```python
import evaluate

# BLEU (translation)
bleu = evaluate.load("bleu")
result = bleu.compute(
    predictions=["the cat sat on the mat"],
    references=[["the cat is on the mat"]]
)
print(f"BLEU: {result['bleu']:.4f}")

# ROUGE (summarization)
rouge = evaluate.load("rouge")
result = rouge.compute(
    predictions=["the cat sat on the mat"],
    references=["the cat is sitting on the mat"]
)
print(f"ROUGE-1: {result['rouge1']:.4f}, ROUGE-L: {result['rougeL']:.4f}")

# SQuAD metric (question answering)
squad_metric = evaluate.load("squad")
result = squad_metric.compute(
    predictions=[{"id": "1", "prediction_text": "Paris"}],
    references=[{"id": "1", "answers": {"text": ["Paris"], "answer_start": [0]}}]
)
print(f"EM: {result['exact_match']}, F1: {result['f1']}")
```

---

## Practice Exercises

### Exercise 1: Data Pipeline

```python
# Build a complete data pipeline for model training

from datasets import load_dataset
from transformers import AutoTokenizer
from torch.utils.data import DataLoader

# Load and explore
dataset = load_dataset("rotten_tomatoes")
print(dataset["train"][0])

# Clean: remove very short reviews
cleaned = dataset["train"].filter(lambda x: len(x["text"].split()) >= 5)

# Tokenize
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)

tokenized = cleaned.map(tokenize, batched=True, remove_columns=["text"])
tokenized = tokenized.rename_column("label", "labels")

# Split and format
split = tokenized.train_test_split(test_size=0.1, seed=42)
split["train"].set_format("torch")
split["test"].set_format("torch")

# Create DataLoaders
train_loader = DataLoader(split["train"], batch_size=32, shuffle=True)
for batch in train_loader:
    print({k: v.shape for k, v in batch.items()})
    break
```

### Exercise 2: Custom Dataset

```python
# Create a synthetic dataset and push to Hub

from datasets import Dataset, DatasetDict, Features, Value, ClassLabel
import random

random.seed(42)
categories = ["sports", "technology", "health"]

def generate_examples(n):
    texts, labels = [], []
    for _ in range(n):
        cat = random.choice(categories)
        if cat == "sports":
            texts.append(f"The team won the {random.choice(['game', 'match'])}.")
        elif cat == "technology":
            texts.append(f"The new {random.choice(['app', 'device'])} was released.")
        else:
            texts.append(f"A study found that {random.choice(['exercise', 'diet'])} helps.")
        labels.append(categories.index(cat))
    return {"text": texts, "label": labels}

features = Features({"text": Value("string"), "label": ClassLabel(names=categories)})

ds = DatasetDict({
    "train": Dataset.from_dict(generate_examples(1000), features=features),
    "test":  Dataset.from_dict(generate_examples(200), features=features)
})

print(ds)
print(ds["train"].features["label"].names)

ds.save_to_disk("./my_custom_dataset")
# ds.push_to_hub("my-username/synthetic-news")  # uncomment to push
```

---

## Summary

These notes cover the key concepts of HuggingFace Datasets:

1. **Loading**: `load_dataset` from Hub, CSV, JSON, Parquet, or custom scripts
2. **Exploring**: Features, splits, column names, indexing, slicing, and iteration
3. **Processing**: `map` (batched, parallel), `filter`, `select`, `sort`, `shuffle`, `rename_column`, `remove_columns`, `flatten`
4. **Streaming**: `streaming=True` for large datasets with `take`, `skip`, `shuffle` buffer
5. **Creating**: `from_dict`, `from_list`, `from_pandas`, `from_generator`
6. **Formatting**: `set_format` / `with_format` for PyTorch, TensorFlow, NumPy output
7. **Combining**: `concatenate_datasets` for merging, `interleave_datasets` for mixing
8. **Hub**: `push_to_hub` for sharing, `save_to_disk` / `load_from_disk` for local storage
9. **Metrics**: `evaluate.load` for accuracy, F1, BLEU, ROUGE, and SQuAD metrics

### Next Steps

1. Create custom dataset loading scripts for complex data formats
2. Explore audio and image dataset support
3. Study the `evaluate` library for comprehensive evaluation pipelines
4. Experiment with very large datasets using streaming and sharding
5. Build end-to-end pipelines combining Datasets with Transformers Trainer

### Additional Resources

- **Datasets Documentation**: <https://huggingface.co/docs/datasets/>
- **Dataset Hub**: <https://huggingface.co/datasets>
- **Evaluate Documentation**: <https://huggingface.co/docs/evaluate/>
- **HuggingFace Course - Datasets**: <https://huggingface.co/learn/nlp-course/chapter5>
