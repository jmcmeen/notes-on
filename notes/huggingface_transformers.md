# Introduction to HuggingFace Transformers

## Table of Contents

1. [What is HuggingFace Transformers?](#what-is-huggingface-transformers)
2. [Installation](#installation)
3. [Pipeline API](#pipeline-api)
4. [Models and Tokenizers](#models-and-tokenizers)
5. [Fine-Tuning with Trainer API](#fine-tuning-with-trainer-api)
6. [Inference Optimization](#inference-optimization)
7. [Custom Training Loop](#custom-training-loop)
8. [Model Hub](#model-hub)
9. [Practice Exercises](#practice-exercises)
10. [Summary](#summary)

---

## What is HuggingFace Transformers?

HuggingFace Transformers is the most popular open-source library for working with pre-trained transformer models. It provides:

- **Thousands of Pre-Trained Models**: BERT, GPT-2, T5, LLaMA, Whisper, ViT, and more
- **Pipeline API**: Simple one-line inference for common tasks
- **Unified API**: `AutoModel` and `AutoTokenizer` work across all architectures
- **Multi-Framework Support**: Works with PyTorch, TensorFlow, and JAX/Flax
- **Fine-Tuning Tools**: `Trainer` API for easy model training and evaluation
- **Model Hub Integration**: Download, share, and version models on huggingface.co

---

## Installation

```bash
# Install transformers with PyTorch backend
pip install transformers torch

# Install with all optional dependencies
pip install transformers[torch,sentencepiece,tokenizers]

# Install datasets and accelerate for training
pip install datasets accelerate
```

```python
import transformers
import torch

print(transformers.__version__)  # e.g., 4.40.0
print(torch.__version__)        # e.g., 2.2.0
```

---

## Pipeline API

The `pipeline` function handles tokenization, inference, and post-processing automatically.

### Text Classification

```python
from transformers import pipeline

# Create a sentiment analysis pipeline (downloads default model on first use)
classifier = pipeline("text-classification")

result = classifier("I love using HuggingFace Transformers!")
print(result)  # [{'label': 'POSITIVE', 'score': 0.9998}]

# Classify multiple texts at once
results = classifier([
    "This movie was absolutely fantastic!",
    "The food was terrible and the service was slow.",
])
for r in results:
    print(f"{r['label']}: {r['score']:.4f}")
```

### Named Entity Recognition

```python
from transformers import pipeline

ner = pipeline("ner", aggregation_strategy="simple")  # group entity tokens

text = "Elon Musk founded SpaceX in Hawthorne, California in 2002."
entities = ner(text)

for entity in entities:
    print(f"{entity['word']:20s} | {entity['entity_group']:10s} | {entity['score']:.4f}")
```

### Question Answering

```python
from transformers import pipeline

# Extractive QA: finds the answer span within a given context
qa = pipeline("question-answering")

result = qa(
    question="When was HuggingFace founded?",
    context="HuggingFace was founded in 2016 by Clement Delangue and others."
)
print(f"Answer: {result['answer']}, Score: {result['score']:.4f}")
```

### Summarization

```python
from transformers import pipeline

summarizer = pipeline("summarization")

article = """
Machine learning is a subset of artificial intelligence that focuses on building
systems that learn from data. The field has grown rapidly due to increases in
computing power and availability of large datasets. Key applications include
natural language processing, computer vision, and recommendation systems.
"""

summary = summarizer(article, max_length=50, min_length=20, do_sample=False)
print(summary[0]["summary_text"])
```

### Translation

```python
from transformers import pipeline

# English to French
translator = pipeline("translation_en_to_fr")
result = translator("HuggingFace Transformers is an amazing library.")
print(result[0]["translation_text"])

# Specify a model for other language pairs
translator_de = pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-en-de")
result = translator_de("The weather is beautiful today.")
print(result[0]["translation_text"])
```

### Text Generation

```python
from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

result = generator(
    "The future of artificial intelligence",
    max_length=80,            # maximum total length
    num_return_sequences=2,   # generate 2 completions
    temperature=0.7,          # controls randomness (lower = more focused)
    top_k=50,                 # sample from top 50 tokens
    top_p=0.95,               # nucleus sampling threshold
    do_sample=True
)

for i, seq in enumerate(result):
    print(f"--- Sequence {i+1} ---")
    print(seq["generated_text"])
```

### Zero-Shot Classification

```python
from transformers import pipeline

# Classify text into custom labels without training
zero_shot = pipeline("zero-shot-classification")

text = "The stock market rallied today on positive earnings reports."
labels = ["politics", "business", "sports", "technology"]

result = zero_shot(text, labels)
for label, score in zip(result["labels"], result["scores"]):
    print(f"{label:15s}: {score:.4f}")
```

### Fill-Mask

```python
from transformers import pipeline

fill_mask = pipeline("fill-mask")

results = fill_mask("Paris is the [MASK] of France.")
for r in results:
    print(f"{r['token_str']:10s} | score: {r['score']:.4f}")
# capital    | score: 0.9478
```

### Image Classification

```python
from transformers import pipeline

image_classifier = pipeline("image-classification")

# Accepts file path, URL, or PIL Image
results = image_classifier("cat_photo.jpg")
for r in results:
    print(f"{r['label']:30s} | {r['score']:.4f}")
```

### Audio Classification

```python
from transformers import pipeline

audio_classifier = pipeline(
    "audio-classification",
    model="superb/wav2vec2-base-superb-ks"
)

results = audio_classifier("audio_sample.wav")
for r in results:
    print(f"{r['label']:15s} | {r['score']:.4f}")
```

---

## Models and Tokenizers

### AutoTokenizer

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

text = "HuggingFace Transformers makes NLP easy!"

# Tokenize step by step
tokens = tokenizer.tokenize(text)
print(tokens)  # ['hugging', '##face', 'transformers', 'makes', 'nl', '##p', 'easy', '!']

token_ids = tokenizer.convert_tokens_to_ids(tokens)
print(token_ids)

# Full encoding (adds special tokens, attention mask, padding)
encoded = tokenizer(
    text,
    padding=True,            # pad to max length
    truncation=True,         # truncate if too long
    max_length=128,          # maximum sequence length
    return_tensors="pt"      # return PyTorch tensors ("tf" for TensorFlow)
)

print(encoded.keys())  # dict_keys(['input_ids', 'token_type_ids', 'attention_mask'])

# Decode back to text
decoded = tokenizer.decode(encoded["input_ids"][0], skip_special_tokens=True)
print(decoded)
```

### Batch Tokenization

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

texts = ["First sentence.", "Second sentence is longer.", "Third."]

batch = tokenizer(
    texts,
    padding=True,       # pad shorter sequences to longest in batch
    truncation=True,
    max_length=32,
    return_tensors="pt"
)

print(batch["input_ids"].shape)       # (3, max_len)
print(batch["attention_mask"].shape)  # (3, max_len) - 1=real, 0=padding
```

### AutoModel

```python
from transformers import AutoModel, AutoTokenizer
import torch

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

inputs = tokenizer("HuggingFace makes AI accessible.", return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

last_hidden = outputs.last_hidden_state  # (batch, seq_len, hidden_dim)
print(last_hidden.shape)                 # torch.Size([1, 8, 768])

# Use the [CLS] token as a sentence embedding
cls_embedding = last_hidden[:, 0, :]     # (batch, 768)
```

### Task-Specific Models

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

inputs = tokenizer("This product is wonderful!", return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

probs = torch.softmax(outputs.logits, dim=-1)
predicted = torch.argmax(probs, dim=-1).item()
print(f"Label: {model.config.id2label[predicted]}, Confidence: {probs[0][predicted]:.4f}")

# Other AutoModel variants:
# AutoModelForTokenClassification   - NER, POS tagging
# AutoModelForQuestionAnswering     - extractive QA
# AutoModelForCausalLM              - text generation (GPT-style)
# AutoModelForSeq2SeqLM             - translation, summarization (T5, BART)
# AutoModelForImageClassification   - image classification (ViT)
```

---

## Fine-Tuning with Trainer API

### Preparing the Dataset

```python
from datasets import load_dataset
from transformers import AutoTokenizer

dataset = load_dataset("imdb")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=256)

tokenized = dataset.map(tokenize_function, batched=True)

# Use subsets for faster experimentation
train_dataset = tokenized["train"].shuffle(seed=42).select(range(2000))
eval_dataset  = tokenized["test"].shuffle(seed=42).select(range(500))
```

### Training with Trainer

```python
from transformers import (
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
import numpy as np

model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=2
)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_steps=100,
    eval_strategy="epoch",       # evaluate after each epoch
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    learning_rate=2e-5,
    fp16=True,                   # mixed precision (requires GPU)
)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {"accuracy": (predictions == labels).mean()}

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics,
)

trainer.train()
results = trainer.evaluate()
print(f"Accuracy: {results['eval_accuracy']:.4f}")

# Save the fine-tuned model
trainer.save_model("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")
```

### Data Collators

```python
from transformers import DataCollatorWithPadding

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# Dynamic padding: pads to the longest sequence in each batch (more efficient)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    data_collator=data_collator,  # handles dynamic padding
    compute_metrics=compute_metrics,
)

# Other collators:
# DataCollatorForTokenClassification  - NER tasks
# DataCollatorForSeq2Seq              - translation/summarization
# DataCollatorForLanguageModeling     - causal/masked LM training
```

---

## Inference Optimization

```python
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# 1. Set model to eval mode (disables dropout, batch norm uses running stats)
model.eval()

# 2. Disable gradient computation (saves memory and speeds up inference)
inputs = tokenizer("Great product!", return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=-1)

# 3. Half precision (FP16) - ~50% less memory, faster on modern GPUs
if torch.cuda.is_available():
    model_fp16 = model.half().to("cuda")
    inputs = {k: v.to("cuda") for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model_fp16(**inputs)

# 4. Batch inference for better throughput
texts = ["I love this!", "Terrible.", "It was okay.", "Best ever!"]
batch = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
with torch.no_grad():
    outputs = model(**batch)
    labels = [model.config.id2label[p.item()] for p in torch.argmax(outputs.logits, dim=-1)]
    print(labels)  # ['POSITIVE', 'NEGATIVE', 'POSITIVE', 'POSITIVE']
```

### BetterTransformer and ONNX

```python
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)

# BetterTransformer: fused attention kernels (PyTorch 2.0+)
model = model.to_bettertransformer()

# ONNX Runtime: even faster inference
# pip install optimum[onnxruntime]
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import pipeline

ort_model = ORTModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english", export=True
)
pipe = pipeline("text-classification", model=ort_model, tokenizer=tokenizer)
print(pipe("Fast inference with ONNX!"))
```

---

## Custom Training Loop

```python
import torch
from torch.utils.data import DataLoader
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    get_linear_schedule_with_warmup
)
from datasets import load_dataset

# Prepare data
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
dataset = load_dataset("imdb")

def tokenize_fn(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=256)

tokenized = dataset.map(tokenize_fn, batched=True)
tokenized = tokenized.remove_columns(["text"])
tokenized = tokenized.rename_column("label", "labels")
tokenized.set_format("torch")

train_loader = DataLoader(tokenized["train"].select(range(2000)), batch_size=16, shuffle=True)
eval_loader  = DataLoader(tokenized["test"].select(range(500)), batch_size=64)

# Setup model, optimizer, scheduler
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5, weight_decay=0.01)
num_epochs = 3
scheduler = get_linear_schedule_with_warmup(
    optimizer, num_warmup_steps=500, num_training_steps=len(train_loader) * num_epochs
)

# Training loop
for epoch in range(num_epochs):
    model.train()
    total_loss = 0

    for batch in train_loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss

        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()
        total_loss += loss.item()

    print(f"Epoch {epoch+1} - Loss: {total_loss / len(train_loader):.4f}")

    # Evaluation
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for batch in eval_loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            preds = torch.argmax(model(**batch).logits, dim=-1)
            correct += (preds == batch["labels"]).sum().item()
            total += len(batch["labels"])
    print(f"Epoch {epoch+1} - Accuracy: {correct / total:.4f}")

model.save_pretrained("./custom_model")
tokenizer.save_pretrained("./custom_model")
```

---

## Model Hub

### Pushing Models

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from huggingface_hub import login

login(token="hf_your_token_here")  # or use: huggingface-cli login

model = AutoModelForSequenceClassification.from_pretrained("./fine_tuned_model")
tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_model")

# Push to Hub (creates repo if it doesn't exist)
model.push_to_hub("my-username/my-sentiment-model")
tokenizer.push_to_hub("my-username/my-sentiment-model")

# Or push directly from Trainer
training_args = TrainingArguments(
    output_dir="./results",
    push_to_hub=True,
    hub_model_id="my-username/my-model",
    hub_strategy="every_save",
)
# trainer.push_to_hub("Training complete!")
```

### Model Cards

```python
from huggingface_hub import ModelCard

card_content = """
---
language: en
license: mit
tags:
  - text-classification
  - sentiment-analysis
datasets:
  - imdb
metrics:
  - accuracy
---
# My Sentiment Model
Fine-tuned DistilBERT for binary sentiment classification on IMDB.
**Accuracy**: 92.5% on the test set.
"""

card = ModelCard(card_content)
card.push_to_hub("my-username/my-sentiment-model")
```

---

## Practice Exercises

### Exercise 1: Multi-Label Classification

```python
# Fine-tune for multi-label classification (e.g., emotion detection)

from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import load_dataset
import torch
import numpy as np

dataset = load_dataset("go_emotions", "simplified")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize_fn(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)

tokenized = dataset.map(tokenize_fn, batched=True)

model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=28,
    problem_type="multi_label_classification"  # uses BCEWithLogitsLoss
)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = (torch.sigmoid(torch.tensor(logits)) > 0.5).int().numpy()
    return {"accuracy": (preds == labels).mean()}

# trainer = Trainer(model=model, ...)
# trainer.train()
```

### Exercise 2: Text Generation Strategies

```python
# Compare different decoding strategies

from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

prompt = "The key to a successful machine learning project is"
inputs = tokenizer(prompt, return_tensors="pt")

# Greedy (deterministic, may repeat)
greedy = model.generate(**inputs, max_new_tokens=50, do_sample=False)
print("Greedy:", tokenizer.decode(greedy[0], skip_special_tokens=True))

# Beam search (explores multiple hypotheses)
beam = model.generate(**inputs, max_new_tokens=50, num_beams=5,
                       no_repeat_ngram_size=2, early_stopping=True)
print("Beam:", tokenizer.decode(beam[0], skip_special_tokens=True))

# Top-k + top-p sampling (creative output)
sampled = model.generate(**inputs, max_new_tokens=50, do_sample=True,
                          temperature=0.8, top_k=50, top_p=0.92)
print("Sampled:", tokenizer.decode(sampled[0], skip_special_tokens=True))
```

### Exercise 3: Simple QA System

```python
# Question-answering over a knowledge base

from transformers import pipeline

qa = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

knowledge_base = [
    "Python was created by Guido van Rossum in 1991.",
    "PyTorch is an ML framework developed by Meta AI.",
    "The Transformer was introduced in 'Attention Is All You Need' by Vaswani et al. in 2017.",
]

def answer_question(question, docs):
    best_answer, best_score = None, 0
    for context in docs:
        result = qa(question=question, context=context)
        if result["score"] > best_score:
            best_score = result["score"]
            best_answer = result["answer"]
    return best_answer, best_score

answer, score = answer_question("Who created Python?", knowledge_base)
print(f"Answer: {answer} (confidence: {score:.4f})")
```

---

## Summary

These notes cover the key concepts of HuggingFace Transformers:

1. **Pipeline API**: One-line inference for text-classification, NER, QA, summarization, translation, text-generation, zero-shot-classification, fill-mask, image and audio classification
2. **Tokenizers**: `AutoTokenizer` for encoding text, handling padding, truncation, and special tokens
3. **Models**: `AutoModel` variants for different tasks; `from_pretrained` for loading weights
4. **Fine-Tuning**: `Trainer` API with `TrainingArguments` for training, evaluation, and checkpointing
5. **Data Collators**: Dynamic padding with `DataCollatorWithPadding` for efficient batching
6. **Inference Optimization**: `model.eval()`, `torch.no_grad()`, FP16, BetterTransformer, ONNX
7. **Custom Training**: PyTorch loops with HuggingFace models, schedulers, and gradient clipping
8. **Model Hub**: Push models, create model cards, share with the community

### Next Steps

1. Explore parameter-efficient fine-tuning: LoRA, QLoRA, and PEFT
2. Learn multi-GPU training with Accelerate
3. Study retrieval-augmented generation (RAG) patterns
4. Experiment with multimodal models (CLIP, LLaVA, Whisper)
5. Explore the Evaluate library for comprehensive model evaluation

### Additional Resources

- **HuggingFace Documentation**: <https://huggingface.co/docs/transformers/>
- **HuggingFace Course**: <https://huggingface.co/learn/nlp-course>
- **Model Hub**: <https://huggingface.co/models>
- **HuggingFace Blog**: <https://huggingface.co/blog>
