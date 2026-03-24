# Introduction to OpenCLIP

## Table of Contents

1. [What is OpenCLIP?](#what-is-openclip)
2. [Installation and Setup](#installation-and-setup)
3. [Core Concepts](#core-concepts)
4. [Loading Models](#loading-models)
5. [Image Encoding](#image-encoding)
6. [Text Encoding](#text-encoding)
7. [Zero-Shot Classification](#zero-shot-classification)
8. [Image-Text Similarity](#image-text-similarity)
9. [Image Search](#image-search)
10. [Fine-Tuning Basics](#fine-tuning-basics)
11. [Integration with HuggingFace](#integration-with-huggingface)
12. [Practice Exercises](#practice-exercises)
13. [Summary](#summary)

---

## What is OpenCLIP?

OpenCLIP is an open-source implementation of OpenAI's CLIP (Contrastive Language-Image Pre-training) model. CLIP learns to connect images and text by training on large-scale image-text pairs from the internet, producing a shared embedding space where images and their textual descriptions are close together.

Key ideas behind CLIP and OpenCLIP:

- **Contrastive learning**: The model learns by pulling matching image-text pairs together and pushing non-matching pairs apart in embedding space
- **Zero-shot transfer**: CLIP can classify images into categories it has never been explicitly trained on, using natural language descriptions as class labels
- **Shared embedding space**: Both images and text are projected into the same vector space, enabling direct comparison via cosine similarity
- **Open-source**: OpenCLIP provides community-trained models on open datasets (LAION-2B, LAION-400M, DataComp) with full reproducibility

Common use cases:

- Zero-shot image classification (no task-specific training needed)
- Image search and retrieval using text queries
- Content-based image recommendation
- Multimodal embeddings for downstream tasks
- Image captioning and visual question answering (as a backbone)

---

## Installation and Setup

```python
# Install OpenCLIP
# pip install open_clip_torch

# Additional dependencies for image handling
# pip install Pillow requests torch torchvision

import open_clip
import torch
from PIL import Image

# Verify installation and list available models
available = open_clip.list_pretrained()
print(f"Total available model-dataset combinations: {len(available)}")

# Print a sample of available models
for model_name, pretrained_dataset in available[:10]:
    print(f"  Model: {model_name:30s}  Pretrained on: {pretrained_dataset}")
```

```python
# Check device availability
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Check OpenCLIP version
print(f"OpenCLIP version: {open_clip.__version__}")
```

---

## Core Concepts

### Contrastive Learning

```python
# CLIP is trained with a contrastive objective:
# Given a batch of N image-text pairs:
# 1. Encode all N images into image embeddings
# 2. Encode all N texts into text embeddings
# 3. Compute an NxN similarity matrix (cosine similarity between all pairs)
# 4. The diagonal entries (matching pairs) should have high similarity
# 5. Off-diagonal entries (non-matching pairs) should have low similarity
#
# The loss (InfoNCE) pushes matching pairs together and
# non-matching pairs apart in the shared embedding space.
#
# After training, the model can compare ANY image to ANY text
# by computing cosine similarity between their embeddings.
```

### Embeddings and Cosine Similarity

```python
import torch.nn.functional as F

# Embeddings are dense vectors that represent images or text
# in a shared space. Typical dimensions: 512, 768, or 1024.

# Cosine similarity measures the angle between two vectors:
#   cos(a, b) = (a . b) / (||a|| * ||b||)
#   Range: -1 (opposite) to +1 (identical direction)

def cosine_similarity(a, b):
    # Normalize both vectors to unit length
    a_norm = F.normalize(a, dim=-1)
    b_norm = F.normalize(b, dim=-1)
    # Dot product of unit vectors = cosine similarity
    return (a_norm @ b_norm.T)

# In CLIP, a photo of a dog will have high cosine similarity
# with the text "a photo of a dog" and low similarity with
# "a photo of a car".
```

---

## Loading Models

```python
import open_clip

# Load a model, its associated transforms, and tokenizer
# model_name: architecture (e.g., ViT-B-32, ViT-L-14, ViT-H-14)
# pretrained: dataset it was trained on (e.g., laion2b_s34b_b79k)

model, _, preprocess = open_clip.create_model_and_transforms(
    model_name="ViT-B-32",          # Vision Transformer, Base, patch size 32
    pretrained="laion2b_s34b_b79k"  # trained on LAION-2B dataset
)
tokenizer = open_clip.get_tokenizer("ViT-B-32")

# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
model.eval()  # set to evaluation mode (disables dropout, etc.)

print(f"Model loaded on {device}")
print(f"Visual embedding dim: {model.visual.output_dim}")
```

```python
# Popular model choices and their tradeoffs:
#
# ViT-B-32  -- smallest and fastest, good for prototyping
#              ~400MB, 512-dim embeddings
#
# ViT-B-16  -- better accuracy than B-32, still relatively fast
#              ~600MB, 512-dim embeddings
#
# ViT-L-14  -- high accuracy, larger and slower
#              ~1.7GB, 768-dim embeddings
#
# ViT-H-14  -- highest accuracy in OpenCLIP, largest model
#              ~3.9GB, 1024-dim embeddings
#
# ViT-bigG-14 -- very large model trained on LAION-2B
#                ~10GB, 1280-dim embeddings

# List models trained on a specific dataset
laion_models = [
    (name, data) for name, data in open_clip.list_pretrained()
    if "laion" in data.lower()
]
print(f"Models trained on LAION variants: {len(laion_models)}")
```

---

## Image Encoding

```python
from PIL import Image
import requests
from io import BytesIO

# Load an image from a URL
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Cute_dog.jpg/320px-Cute_dog.jpg"
response = requests.get(url)
image = Image.open(BytesIO(response.content)).convert("RGB")

# Or load from a local file
# image = Image.open("photo.jpg").convert("RGB")

# Preprocess the image (resize, center crop, normalize)
# The preprocess function matches the transforms used during training
image_input = preprocess(image).unsqueeze(0).to(device)
# unsqueeze(0) adds a batch dimension: [C, H, W] -> [1, C, H, W]

print(f"Preprocessed image shape: {image_input.shape}")
# Typically: torch.Size([1, 3, 224, 224])

# Encode the image into an embedding vector
with torch.no_grad():                         # disable gradient computation
    image_embedding = model.encode_image(image_input)

print(f"Image embedding shape: {image_embedding.shape}")
# e.g., torch.Size([1, 512]) for ViT-B-32

# Normalize the embedding for cosine similarity
image_embedding = F.normalize(image_embedding, dim=-1)
```

```python
# Batch encoding: process multiple images at once for efficiency
from pathlib import Path

def encode_images(image_paths, model, preprocess, device):
    """Encode a list of images into normalized embeddings."""
    images = []
    for path in image_paths:
        img = Image.open(path).convert("RGB")
        images.append(preprocess(img))

    # Stack into a batch tensor
    image_batch = torch.stack(images).to(device)

    with torch.no_grad():
        embeddings = model.encode_image(image_batch)
        embeddings = F.normalize(embeddings, dim=-1)  # normalize for similarity

    return embeddings

# Usage:
# paths = list(Path("./images").glob("*.jpg"))
# embeddings = encode_images(paths, model, preprocess, device)
# print(f"Encoded {len(paths)} images, shape: {embeddings.shape}")
```

---

## Text Encoding

```python
# Tokenize text descriptions
texts = [
    "a photo of a dog",
    "a photo of a cat",
    "a photo of a car",
    "a beautiful sunset over the ocean",
]

# Tokenize: convert text strings to token IDs
text_tokens = tokenizer(texts).to(device)
print(f"Token shape: {text_tokens.shape}")
# e.g., torch.Size([4, 77]) -- 4 texts, each padded to 77 tokens

# Encode text into embeddings
with torch.no_grad():
    text_embeddings = model.encode_text(text_tokens)
    text_embeddings = F.normalize(text_embeddings, dim=-1)

print(f"Text embedding shape: {text_embeddings.shape}")
# e.g., torch.Size([4, 512]) -- 4 texts, each with 512-dim embedding
```

```python
# Prompt engineering: CLIP is sensitive to text phrasing
# Using multiple prompt templates and averaging their embeddings improves accuracy

prompt_templates = [
    "a photo of a {}.",
    "a close-up photo of a {}.",
    "a bright photo of a {}.",
    "a photo of a small {}.",
    "a photo of a large {}.",
]

def encode_class_with_templates(class_name, templates, tokenizer, model, device):
    """Encode a class using multiple prompt templates and average the embeddings."""
    prompts = [t.format(class_name) for t in templates]
    tokens = tokenizer(prompts).to(device)

    with torch.no_grad():
        embeddings = model.encode_text(tokens)
        embeddings = F.normalize(embeddings, dim=-1)

    # Average across templates for a more robust class representation
    mean_embedding = F.normalize(embeddings.mean(dim=0, keepdim=True), dim=-1)
    return mean_embedding
```

---

## Zero-Shot Classification

```python
# Zero-shot classification: classify images without any task-specific training
# CLIP compares the image embedding against text embeddings for each candidate class

def zero_shot_classify(image_path, class_names, model, preprocess, tokenizer, device):
    """Classify a single image into one of the given classes."""
    # Encode the image
    image = Image.open(image_path).convert("RGB")
    image_input = preprocess(image).unsqueeze(0).to(device)

    # Create text prompts for each class
    text_prompts = [f"a photo of a {cls}" for cls in class_names]
    text_tokens = tokenizer(text_prompts).to(device)

    with torch.no_grad():
        # Get normalized embeddings
        image_emb = F.normalize(model.encode_image(image_input), dim=-1)
        text_emb = F.normalize(model.encode_text(text_tokens), dim=-1)

        # Compute similarity between image and each class
        similarities = (image_emb @ text_emb.T).squeeze(0)  # shape: [num_classes]

        # Convert to probabilities with softmax (temperature-scaled)
        probs = (100.0 * similarities).softmax(dim=-1)

    # Return results sorted by probability
    results = list(zip(class_names, probs.cpu().numpy()))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

# Example usage
classes = ["dog", "cat", "bird", "fish", "horse", "car", "airplane", "tree"]
results = zero_shot_classify("photo.jpg", classes, model, preprocess, tokenizer, device)

for cls, prob in results:
    print(f"  {cls:15s} {prob:.4f}")
# Output might be:
#   dog             0.8523
#   cat             0.0712
#   horse           0.0301
#   ...
```

For batch classification, pre-compute text embeddings once and reuse them for each image. This avoids redundant text encoding and significantly speeds up processing over a directory of images.

---

## Image-Text Similarity

```python
# Compute similarity between a set of images and a set of text descriptions
# Returns an (N_images x N_texts) similarity matrix

def compute_similarity_matrix(image_paths, text_descriptions, model, preprocess, tokenizer, device):
    """Compute cosine similarity between all image-text pairs."""
    # Encode all images
    images = [preprocess(Image.open(p).convert("RGB")) for p in image_paths]
    image_batch = torch.stack(images).to(device)

    # Encode all texts
    text_tokens = tokenizer(text_descriptions).to(device)

    with torch.no_grad():
        image_emb = F.normalize(model.encode_image(image_batch), dim=-1)
        text_emb = F.normalize(model.encode_text(text_tokens), dim=-1)

        # Similarity matrix: each cell is cosine similarity between image i and text j
        similarity = image_emb @ text_emb.T

    return similarity.cpu().numpy()

# Example
image_files = ["dog.jpg", "car.jpg", "sunset.jpg"]
descriptions = ["a photo of a dog", "a red sports car", "a sunset over the ocean"]

sim_matrix = compute_similarity_matrix(
    image_files, descriptions, model, preprocess, tokenizer, device
)

# Print the similarity matrix
print("Similarity matrix (images=rows, texts=columns):")
for i, img in enumerate(image_files):
    scores = [f"{sim_matrix[i, j]:.3f}" for j in range(len(descriptions))]
    print(f"  {img:15s} -> [{', '.join(scores)}]")
# The diagonal should have the highest values (matching pairs)
```

The same approach can rank candidate captions for an image: encode the image and all candidate texts, compute cosine similarities, and sort by score.

---

## Image Search

```python
import numpy as np

# Build an image search index: encode all images, then query with text
class CLIPImageSearch:
    """Simple text-to-image search using CLIP embeddings."""

    def __init__(self, model, preprocess, tokenizer, device):
        self.model = model
        self.preprocess = preprocess
        self.tokenizer = tokenizer
        self.device = device
        self.image_paths = []
        self.image_embeddings = None  # stored as numpy array

    def index_images(self, image_dir, extensions=("*.jpg", "*.png", "*.jpeg")):
        """Encode and index all images in a directory."""
        paths = []
        for ext in extensions:
            paths.extend(Path(image_dir).glob(ext))
        self.image_paths = sorted(paths)

        # Encode images in batches to manage GPU memory
        all_embeddings = []
        batch_size = 32

        for i in range(0, len(self.image_paths), batch_size):
            batch_paths = self.image_paths[i:i + batch_size]
            images = [self.preprocess(Image.open(p).convert("RGB")) for p in batch_paths]
            image_batch = torch.stack(images).to(self.device)

            with torch.no_grad():
                emb = self.model.encode_image(image_batch)
                emb = F.normalize(emb, dim=-1)
                all_embeddings.append(emb.cpu().numpy())

        self.image_embeddings = np.concatenate(all_embeddings, axis=0)
        print(f"Indexed {len(self.image_paths)} images")

    def search(self, query_text, top_k=5):
        """Search for images matching a text query."""
        # Encode the query text
        tokens = self.tokenizer([query_text]).to(self.device)

        with torch.no_grad():
            text_emb = self.model.encode_text(tokens)
            text_emb = F.normalize(text_emb, dim=-1)
            text_emb = text_emb.cpu().numpy()

        # Compute cosine similarity against all indexed images
        similarities = (text_emb @ self.image_embeddings.T).squeeze(0)

        # Get top-k results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = [
            (self.image_paths[i], similarities[i])
            for i in top_indices
        ]
        return results

# Usage:
# searcher = CLIPImageSearch(model, preprocess, tokenizer, device)
# searcher.index_images("./my_photos")
# results = searcher.search("a dog playing in the snow", top_k=5)
# for path, score in results:
#     print(f"  {score:.4f}  {path}")
```

---

## Fine-Tuning Basics

```python
# Fine-tune CLIP on a custom dataset of image-text pairs
# This adapts the model to your specific domain

import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

class ImageTextDataset(Dataset):
    """Custom dataset of image-text pairs for fine-tuning CLIP."""

    def __init__(self, image_paths, captions, preprocess, tokenizer):
        self.image_paths = image_paths
        self.captions = captions
        self.preprocess = preprocess
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert("RGB")
        image_tensor = self.preprocess(image)
        text_tokens = self.tokenizer([self.captions[idx]])[0]  # tokenize single caption
        return image_tensor, text_tokens

def fine_tune_clip(model, dataset, device, epochs=5, lr=1e-5, batch_size=32):
    """Fine-tune a CLIP model on a custom image-text dataset."""
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Use a low learning rate to avoid catastrophic forgetting
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    loss_fn = open_clip.ClipLoss()  # contrastive loss function

    model.train()  # enable training mode

    for epoch in range(epochs):
        total_loss = 0.0

        for images, texts in dataloader:
            images = images.to(device)
            texts = texts.to(device)

            # Forward pass: get image and text features
            image_features = model.encode_image(images)
            text_features = model.encode_text(texts)

            # Normalize embeddings
            image_features = F.normalize(image_features, dim=-1)
            text_features = F.normalize(text_features, dim=-1)

            # Compute contrastive loss
            logit_scale = model.logit_scale.exp()
            loss = loss_fn(image_features, text_features, logit_scale)

            # Backward pass and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}")

    model.eval()  # switch back to eval mode
    return model
```

---

## Integration with HuggingFace

```python
# OpenCLIP models can also be loaded through HuggingFace Transformers
# pip install transformers

from transformers import CLIPModel, CLIPProcessor

# Load an OpenCLIP model from HuggingFace Hub
hf_model = CLIPModel.from_pretrained("laion/CLIP-ViT-B-32-laion2B-s34B-b79K")
hf_processor = CLIPProcessor.from_pretrained("laion/CLIP-ViT-B-32-laion2B-s34B-b79K")

# Process image and text together
image = Image.open("photo.jpg").convert("RGB")
inputs = hf_processor(
    text=["a photo of a dog", "a photo of a cat"],
    images=image,
    return_tensors="pt",
    padding=True
)

# Get similarity scores
with torch.no_grad():
    outputs = hf_model(**inputs)
    logits_per_image = outputs.logits_per_image  # image-text similarity
    probs = logits_per_image.softmax(dim=-1)     # convert to probabilities

print(f"Dog probability: {probs[0][0]:.4f}")
print(f"Cat probability: {probs[0][1]:.4f}")
```

OpenCLIP embeddings can also be combined with HuggingFace `datasets` for batch encoding of vision datasets like CIFAR-10 or ImageNet, then used for downstream tasks such as clustering, similarity search, or linear probe classification.

---

## Practice Exercises

### Exercise 1: Multi-Class Zero-Shot Classifier

Build a zero-shot image classifier for a custom set of categories.

```python
# 1. Choose 10-20 categories relevant to your domain (e.g., food types, animals)
# 2. Collect 5-10 test images per category
# 3. Implement zero-shot classification with prompt template ensembling
# 4. Compute and display a confusion matrix
# 5. Experiment with different prompt templates and compare accuracy
```

### Exercise 2: Image Search Engine

Build a local image search engine using CLIP embeddings.

```python
# 1. Index a folder of 100+ images using the CLIPImageSearch class
# 2. Implement text-to-image search with ranked results
# 3. Add image-to-image search (query with an image instead of text)
# 4. Save and load the index (embeddings + paths) to/from disk
# 5. Measure search latency for different index sizes
```

### Exercise 3: Model Comparison

Compare different OpenCLIP model sizes on a classification task.

```python
# 1. Pick a dataset (e.g., CIFAR-10, Oxford Pets, or your own)
# 2. Run zero-shot classification with ViT-B-32, ViT-B-16, and ViT-L-14
# 3. Record accuracy, inference time, and memory usage for each
# 4. Plot accuracy vs. speed tradeoff
# 5. Determine which model best fits your resource constraints
```

---

## Summary

OpenCLIP provides a powerful, open-source vision-language model for connecting images and text:

- **Contrastive learning** trains the model to align matching image-text pairs in a shared embedding space
- **Model selection** ranges from fast (ViT-B-32) to highly accurate (ViT-H-14, ViT-bigG-14)
- **Image and text encoding** produce normalized embeddings compared via cosine similarity
- **Zero-shot classification** works by comparing an image embedding against text embeddings for each class
- **Image search** indexes image embeddings and queries them with text to find relevant images
- **Fine-tuning** adapts the model to custom domains using image-text pair datasets
- **HuggingFace integration** enables using OpenCLIP models within the Transformers and Datasets ecosystem

---

## Next Steps

- Explore **SigLIP** and other CLIP variants for improved performance on specific tasks
- Build a **retrieval-augmented generation (RAG)** system using CLIP embeddings for image retrieval
- Combine CLIP with **generative models** (Stable Diffusion) for text-guided image editing
- Use CLIP embeddings for **multimodal clustering** and dataset analysis
- Investigate **linear probing**: train a simple classifier on top of frozen CLIP features
- Try **multilingual CLIP** variants for non-English text-image matching

---

## Additional Resources

- [OpenCLIP GitHub Repository](https://github.com/mlfoundations/open_clip)
- [Original CLIP Paper (Radford et al., 2021)](https://arxiv.org/abs/2103.00020)
- [LAION-5B Dataset](https://laion.ai/blog/laion-5b/)
- [HuggingFace OpenCLIP Models](https://huggingface.co/models?library=open_clip)
- [OpenCLIP Model Zoo](https://github.com/mlfoundations/open_clip/blob/main/docs/openclip_results.csv)
- [CLIP Prompt Engineering Tips](https://github.com/openai/CLIP/blob/main/notebooks/Prompt_Engineering_for_ImageNet.ipynb)
