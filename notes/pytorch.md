# Introduction to PyTorch

## Table of Contents

1. [What is PyTorch?](#what-is-pytorch)
2. [Installation and Setup](#installation-and-setup)
3. [Tensors](#tensors)
4. [Autograd](#autograd)
5. [Building Neural Networks](#building-neural-networks)
6. [Training Loop](#training-loop)
7. [Datasets and DataLoaders](#datasets-and-dataloaders)
8. [Saving and Loading Models](#saving-and-loading-models)
9. [Transfer Learning](#transfer-learning)
10. [GPU Training](#gpu-training)
11. [Practice Exercises](#practice-exercises)
12. [Summary](#summary)

---

## What is PyTorch?

PyTorch is an open-source deep learning framework developed by Meta AI (formerly Facebook AI Research). It provides:
- **Dynamic computation graphs**: Graphs are built on-the-fly during execution, not ahead of time
- **Eager execution**: Operations run immediately, making debugging natural with standard Python tools
- **GPU acceleration**: Seamless tensor computation on NVIDIA GPUs via CUDA
- **Automatic differentiation**: Built-in gradient computation for training neural networks
- **Rich ecosystem**: torchvision, torchaudio, torchtext, Hugging Face integration, and more
- **Pythonic design**: Feels like standard Python and NumPy, with a gentle learning curve
- **Production ready**: TorchScript and ONNX export for deployment

---

## Installation and Setup

```bash
# CPU only
pip install torch torchvision torchaudio

# CUDA 12.1 (check https://pytorch.org/get-started for latest)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Conda installation
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

```python
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

print(torch.__version__)             # e.g. 2.2.0
print(torch.cuda.is_available())     # True if GPU is available
print(torch.cuda.device_count())     # number of GPUs
```

---

## Tensors

Tensors are the fundamental data structure in PyTorch -- multi-dimensional arrays similar to NumPy ndarrays but with GPU support and automatic differentiation.

### Creating Tensors

```python
import torch

# From Python lists
a = torch.tensor([1, 2, 3, 4, 5])
print(a)          # tensor([1, 2, 3, 4, 5])
print(a.dtype)    # torch.int64

# 2D tensor (matrix)
b = torch.tensor([[1, 2, 3],
                  [4, 5, 6]])
print(b.shape)    # torch.Size([2, 3])

# Specifying dtype
c = torch.tensor([1, 2, 3], dtype=torch.float32)
print(c)          # tensor([1., 2., 3.])

# Common creation functions
zeros = torch.zeros(3, 4)            # 3x4 matrix of zeros
ones = torch.ones(2, 3)              # 2x3 matrix of ones
rand = torch.rand(2, 3)              # uniform random [0, 1)
randn = torch.randn(2, 3)            # standard normal distribution
arange = torch.arange(0, 10, 2)      # tensor([0, 2, 4, 6, 8])
linspace = torch.linspace(0, 1, 5)   # tensor([0.00, 0.25, 0.50, 0.75, 1.00])
empty = torch.empty(3, 3)            # uninitialized memory
full = torch.full((2, 3), 7.0)       # filled with 7.0
eye = torch.eye(3)                   # 3x3 identity matrix

# Like functions -- create tensors with the same shape/dtype as another
x = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
zeros_like = torch.zeros_like(x)     # same shape and dtype as x
ones_like = torch.ones_like(x)       # same shape and dtype as x
rand_like = torch.rand_like(x)       # same shape and dtype as x
```

### Tensor Operations

```python
import torch

a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([4.0, 5.0, 6.0])

# Arithmetic (element-wise)
print(a + b)         # tensor([5., 7., 9.])
print(a * b)         # tensor([4., 10., 18.])
print(a / b)         # tensor([0.2500, 0.4000, 0.5000])
print(a ** 2)        # tensor([1., 4., 9.])

# In-place operations (suffix with underscore)
c = torch.tensor([1.0, 2.0, 3.0])
c.add_(10)           # modifies c in place -> tensor([11., 12., 13.])
c.mul_(2)            # modifies c in place -> tensor([22., 24., 26.])

# Matrix operations
m1 = torch.rand(2, 3)
m2 = torch.rand(3, 4)
result = torch.matmul(m1, m2)    # matrix multiplication -> (2, 4)
result = m1 @ m2                 # shorthand for matmul

# Aggregations
x = torch.tensor([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0]])
print(x.sum())          # tensor(21.) -- sum of all elements
print(x.mean())         # tensor(3.5000)
print(x.max())          # tensor(6.)
print(x.sum(dim=0))     # tensor([5., 7., 9.]) -- sum along rows
print(x.sum(dim=1))     # tensor([6., 15.]) -- sum along columns
print(x.argmax(dim=1))  # tensor([2, 2]) -- index of max in each row

# Comparison
print(x > 3)     # tensor([[False, False, False], [True, True, True]])
print(x[x > 3])  # tensor([4., 5., 6.]) -- boolean indexing
```

### Shapes and Reshaping

```python
import torch

x = torch.arange(12, dtype=torch.float32)
print(x.shape)          # torch.Size([12])

# Reshape
y = x.reshape(3, 4)    # reshape to 3x4
print(y.shape)          # torch.Size([3, 4])

# View -- returns a tensor sharing the same underlying data
z = x.view(4, 3)       # must be contiguous in memory
print(z.shape)          # torch.Size([4, 3])

# -1 infers the dimension
w = x.reshape(2, -1)   # shape becomes (2, 6)

# Squeeze and unsqueeze
a = torch.rand(1, 3, 1, 4)
print(a.squeeze().shape)        # torch.Size([3, 4]) -- removes all dim=1
print(a.squeeze(0).shape)       # torch.Size([3, 1, 4]) -- removes dim 0 only

b = torch.rand(3, 4)
print(b.unsqueeze(0).shape)     # torch.Size([1, 3, 4]) -- add dim at position 0
print(b.unsqueeze(-1).shape)    # torch.Size([3, 4, 1]) -- add dim at end

# Transpose and permute
m = torch.rand(2, 3, 4)
print(m.transpose(0, 2).shape)  # torch.Size([4, 3, 2]) -- swap dims 0 and 2
print(m.permute(2, 0, 1).shape) # torch.Size([4, 2, 3]) -- reorder all dims

# Concatenation and stacking
t1 = torch.rand(2, 3)
t2 = torch.rand(2, 3)
cat = torch.cat([t1, t2], dim=0)    # torch.Size([4, 3]) -- along rows
stack = torch.stack([t1, t2], dim=0) # torch.Size([2, 2, 3]) -- new dimension

# Flatten
x = torch.rand(2, 3, 4)
flat = x.flatten()                # torch.Size([24])
partial = x.flatten(1)           # torch.Size([2, 12]) -- flatten from dim 1 onward
```

### Data Types

```python
import torch

# Common dtypes
x_f32 = torch.tensor([1.0], dtype=torch.float32)   # default float
x_f64 = torch.tensor([1.0], dtype=torch.float64)   # double precision
x_f16 = torch.tensor([1.0], dtype=torch.float16)   # half precision
x_bf16 = torch.tensor([1.0], dtype=torch.bfloat16) # brain floating point
x_i32 = torch.tensor([1], dtype=torch.int32)        # 32-bit integer
x_i64 = torch.tensor([1], dtype=torch.int64)        # default integer
x_bool = torch.tensor([True, False])                # boolean

# Type casting
a = torch.tensor([1, 2, 3])         # int64
b = a.float()                       # convert to float32
c = a.to(torch.float16)             # convert to float16
d = a.type(torch.DoubleTensor)      # convert to float64

print(b.dtype)   # torch.float32
```

### GPU Support

```python
import torch

# Check GPU availability
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)    # cuda or cpu

# Move tensors to GPU
x = torch.rand(3, 3)
x_gpu = x.to(device)                # move to GPU (or stay on CPU)
x_gpu = x.cuda()                    # explicitly move to GPU (fails if no GPU)
x_cpu = x_gpu.cpu()                 # move back to CPU

# Create tensor directly on GPU
y = torch.rand(3, 3, device=device)

# GPU tensors must be moved to CPU before converting to NumPy
numpy_array = x_gpu.cpu().numpy()

# NumPy to tensor
import numpy as np
np_arr = np.array([1.0, 2.0, 3.0])
tensor_from_np = torch.from_numpy(np_arr)     # shares memory with np array
tensor_copy = torch.tensor(np_arr)            # copies the data
```

---

## Autograd

PyTorch's automatic differentiation engine powers neural network training. It records operations on tensors and computes gradients automatically.

### Basic Gradient Computation

```python
import torch

# requires_grad tells PyTorch to track operations for gradient computation
x = torch.tensor([2.0, 3.0], requires_grad=True)

# Perform operations -- PyTorch builds a computation graph
y = x ** 2 + 3 * x + 1   # y = x^2 + 3x + 1
z = y.sum()               # scalar output needed for backward()

# Compute gradients
z.backward()              # computes dz/dx for all tensors with requires_grad=True

# Access gradients
print(x.grad)   # tensor([7., 9.]) -- dy/dx = 2x + 3, evaluated at x=[2, 3]
```

### Gradient Control

```python
import torch

x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)

# Detach from computation graph
y = x.detach()             # y shares data but has no gradient tracking
print(y.requires_grad)    # False

# Stop tracking in a block (useful during inference)
with torch.no_grad():
    y = x * 2             # no gradient tracking here
    print(y.requires_grad) # False

# Zero gradients before each backward pass (gradients accumulate by default)
x = torch.tensor([1.0], requires_grad=True)
y = x * 2
y.backward()
print(x.grad)   # tensor([2.])

y = x * 3
y.backward()
print(x.grad)   # tensor([5.]) -- accumulated! (2 + 3)

x.grad.zero_()  # reset gradients to zero
print(x.grad)   # tensor([0.])
```

---

## Building Neural Networks

PyTorch provides the `torch.nn` module for building neural networks using an object-oriented approach centered on `nn.Module`.

### Basic nn.Module

```python
import torch
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        # Define layers
        self.fc1 = nn.Linear(input_size, hidden_size)    # fully connected layer
        self.relu = nn.ReLU()                             # activation function
        self.fc2 = nn.Linear(hidden_size, num_classes)    # output layer

    def forward(self, x):
        # Define forward pass -- how data flows through the network
        x = self.fc1(x)     # linear transformation
        x = self.relu(x)    # non-linear activation
        x = self.fc2(x)     # output logits
        return x

# Instantiate the model
model = SimpleNet(input_size=784, hidden_size=128, num_classes=10)

# Check model structure
print(model)

# Count parameters
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Total params: {total_params}")
print(f"Trainable params: {trainable_params}")
```

### Common Layers

```python
import torch
import torch.nn as nn

# Linear (fully connected) layer
linear = nn.Linear(in_features=784, out_features=256)   # weight: (256, 784), bias: (256,)

# Convolutional layers
conv2d = nn.Conv2d(in_channels=3, out_channels=16,      # 3 input channels (RGB), 16 filters
                   kernel_size=3, stride=1, padding=1)   # 3x3 kernel, same padding

# Activation functions
relu = nn.ReLU()                    # max(0, x)
leaky_relu = nn.LeakyReLU(0.01)    # small slope for negative values
sigmoid = nn.Sigmoid()              # squash to [0, 1]
tanh = nn.Tanh()                    # squash to [-1, 1]
softmax = nn.Softmax(dim=1)         # probability distribution

# Normalization
batch_norm1d = nn.BatchNorm1d(256)        # for fully connected layers
batch_norm2d = nn.BatchNorm2d(16)         # for conv layers (per channel)
layer_norm = nn.LayerNorm(256)            # alternative to batch norm

# Regularization
dropout = nn.Dropout(p=0.5)              # randomly zero 50% of elements during training
dropout2d = nn.Dropout2d(p=0.25)         # drop entire channels in conv layers

# Pooling
max_pool = nn.MaxPool2d(kernel_size=2, stride=2)     # downsample by 2x
avg_pool = nn.AdaptiveAvgPool2d((1, 1))               # global average pooling
```

### CNN Example

```python
import torch
import torch.nn as nn

class ConvNet(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        # Convolutional feature extractor
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),   # (B, 3, 32, 32) -> (B, 32, 32, 32)
            nn.BatchNorm2d(32),                            # normalize activations
            nn.ReLU(inplace=True),                         # activation
            nn.MaxPool2d(2, 2),                            # (B, 32, 32, 32) -> (B, 32, 16, 16)

            nn.Conv2d(32, 64, kernel_size=3, padding=1),   # (B, 32, 16, 16) -> (B, 64, 16, 16)
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),                            # (B, 64, 16, 16) -> (B, 64, 8, 8)

            nn.Conv2d(64, 128, kernel_size=3, padding=1),  # (B, 64, 8, 8) -> (B, 128, 8, 8)
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1)),                  # (B, 128, 8, 8) -> (B, 128, 1, 1)
        )
        # Classifier head
        self.classifier = nn.Sequential(
            nn.Flatten(),                      # (B, 128, 1, 1) -> (B, 128)
            nn.Dropout(0.5),                   # regularization
            nn.Linear(128, num_classes),       # output logits
        )

    def forward(self, x):
        x = self.features(x)       # extract features
        x = self.classifier(x)     # classify
        return x

model = ConvNet(num_classes=10)
dummy_input = torch.randn(4, 3, 32, 32)     # batch of 4 RGB 32x32 images
output = model(dummy_input)
print(output.shape)   # torch.Size([4, 10])
```

---

## Training Loop

The training loop is where the model learns. PyTorch gives you full control over every step.

### Loss Functions

```python
import torch
import torch.nn as nn

# Classification losses
ce_loss = nn.CrossEntropyLoss()          # multi-class (expects raw logits)
bce_loss = nn.BCEWithLogitsLoss()        # binary classification (expects raw logits)
nll_loss = nn.NLLLoss()                  # negative log likelihood (expects log probs)

# Regression losses
mse_loss = nn.MSELoss()                  # mean squared error
l1_loss = nn.L1Loss()                    # mean absolute error
smooth_l1 = nn.SmoothL1Loss()            # Huber loss

# Example usage
logits = torch.randn(4, 10)             # batch of 4, 10 classes
targets = torch.tensor([3, 7, 1, 9])    # target class indices
loss = ce_loss(logits, targets)          # scalar loss value
print(loss.item())                       # get Python number from scalar tensor
```

### Optimizers

```python
import torch.optim as optim

model = SimpleNet(784, 128, 10)    # from earlier example

# Common optimizers
sgd = optim.SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay=1e-4)
adam = optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999))
adamw = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)

# Learning rate schedulers
scheduler = optim.lr_scheduler.StepLR(adam, step_size=10, gamma=0.1)       # decay every 10 epochs
scheduler = optim.lr_scheduler.CosineAnnealingLR(adam, T_max=50)           # cosine decay
scheduler = optim.lr_scheduler.ReduceLROnPlateau(adam, patience=5)         # reduce on plateau
```

### Complete Training Loop

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Create dummy data
X_train = torch.randn(1000, 784)               # 1000 samples, 784 features
y_train = torch.randint(0, 10, (1000,))         # 10 classes
X_val = torch.randn(200, 784)
y_val = torch.randint(0, 10, (200,))

# Create data loaders
train_dataset = TensorDataset(X_train, y_train)
val_dataset = TensorDataset(X_val, y_val)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleNet(784, 128, 10).to(device)       # move model to device
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 20
for epoch in range(num_epochs):
    # --- Training phase ---
    model.train()                                # set model to training mode
    train_loss = 0.0
    correct = 0
    total = 0

    for batch_X, batch_y in train_loader:
        batch_X, batch_y = batch_X.to(device), batch_y.to(device)   # move data to device

        optimizer.zero_grad()                    # clear previous gradients
        outputs = model(batch_X)                 # forward pass
        loss = criterion(outputs, batch_y)       # compute loss
        loss.backward()                          # backward pass (compute gradients)
        optimizer.step()                         # update weights

        train_loss += loss.item() * batch_X.size(0)
        _, predicted = outputs.max(1)            # get predicted class
        correct += predicted.eq(batch_y).sum().item()
        total += batch_y.size(0)

    train_loss /= total
    train_acc = 100.0 * correct / total

    # --- Validation phase ---
    model.eval()                                 # set model to evaluation mode
    val_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():                        # disable gradient computation
        for batch_X, batch_y in val_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)

            val_loss += loss.item() * batch_X.size(0)
            _, predicted = outputs.max(1)
            correct += predicted.eq(batch_y).sum().item()
            total += batch_y.size(0)

    val_loss /= total
    val_acc = 100.0 * correct / total

    print(f"Epoch [{epoch+1}/{num_epochs}] "
          f"Train Loss: {train_loss:.4f} Acc: {train_acc:.2f}% | "
          f"Val Loss: {val_loss:.4f} Acc: {val_acc:.2f}%")
```

---

## Datasets and DataLoaders

PyTorch provides utilities for efficient data loading with batching, shuffling, and parallel workers.

### Custom Dataset

```python
import torch
from torch.utils.data import Dataset, DataLoader

class CustomDataset(Dataset):
    def __init__(self, data, labels, transform=None):
        self.data = data            # store the input data
        self.labels = labels        # store the labels
        self.transform = transform  # optional transform

    def __len__(self):
        return len(self.data)       # total number of samples

    def __getitem__(self, idx):
        sample = self.data[idx]     # get one sample
        label = self.labels[idx]

        if self.transform:
            sample = self.transform(sample)   # apply transform if provided

        return sample, label        # return (input, target) pair

# Usage
X = torch.randn(500, 3, 32, 32)    # 500 images, 3 channels, 32x32
y = torch.randint(0, 10, (500,))    # 500 labels

dataset = CustomDataset(X, y)
print(len(dataset))                 # 500
sample, label = dataset[0]         # get first sample
print(sample.shape, label)         # torch.Size([3, 32, 32]) tensor(...)
```

### DataLoader

```python
from torch.utils.data import DataLoader

loader = DataLoader(
    dataset,
    batch_size=32,          # samples per batch
    shuffle=True,           # randomize order each epoch
    num_workers=4,          # parallel data loading processes
    pin_memory=True,        # faster GPU transfer
    drop_last=False,        # keep incomplete last batch
)

# Iterate over batches
for batch_X, batch_y in loader:
    print(batch_X.shape)    # torch.Size([32, 3, 32, 32])
    print(batch_y.shape)    # torch.Size([32])
    break                   # just show first batch
```

### Torchvision Datasets and Transforms

```python
import torchvision
import torchvision.transforms as transforms

# Define image transforms (preprocessing pipeline)
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),          # data augmentation
    transforms.RandomCrop(32, padding=4),       # random crop with padding
    transforms.ColorJitter(brightness=0.2),     # color augmentation
    transforms.ToTensor(),                      # convert PIL Image to tensor [0, 1]
    transforms.Normalize(                       # normalize with ImageNet stats
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

# Download and load CIFAR-10 dataset
train_dataset = torchvision.datasets.CIFAR10(
    root="./data",
    train=True,
    download=True,
    transform=train_transform,
)

test_dataset = torchvision.datasets.CIFAR10(
    root="./data",
    train=False,
    download=True,
    transform=test_transform,
)

# Create data loaders
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True, num_workers=2)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False, num_workers=2)

print(f"Training samples: {len(train_dataset)}")   # 50000
print(f"Test samples: {len(test_dataset)}")         # 10000
```

---

## Saving and Loading Models

### Saving and Loading state_dict (Recommended)

```python
import torch

# Save model weights only (recommended approach)
torch.save(model.state_dict(), "model_weights.pth")

# Load model weights
model = SimpleNet(784, 128, 10)                  # create model with same architecture
model.load_state_dict(torch.load("model_weights.pth", weights_only=True))
model.eval()                                     # set to evaluation mode
```

### Saving Complete Checkpoints

```python
import torch

# Save everything needed to resume training
checkpoint = {
    "epoch": epoch,
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict(),
    "train_loss": train_loss,
    "val_loss": val_loss,
}
torch.save(checkpoint, "checkpoint.pth")

# Load checkpoint and resume training
checkpoint = torch.load("checkpoint.pth", weights_only=False)
model.load_state_dict(checkpoint["model_state_dict"])
optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
start_epoch = checkpoint["epoch"] + 1
print(f"Resuming from epoch {start_epoch}")
```

---

## Transfer Learning

Transfer learning uses a model pretrained on a large dataset (like ImageNet) and adapts it for a new task, saving time and improving performance especially with limited data.

### Feature Extraction (Freeze All Layers)

```python
import torch
import torch.nn as nn
from torchvision import models

model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# Freeze all pretrained layers -- no gradient updates
for param in model.parameters():
    param.requires_grad = False

# Replace the final classification layer for our task
num_classes = 5
model.fc = nn.Linear(model.fc.in_features, num_classes)  # new layer is trainable

# Only the new fc layer will be updated during training
optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.001)
```

### Fine-Tuning (Unfreeze Some Layers)

```python
import torch
import torch.nn as nn
from torchvision import models

model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# Freeze early layers (low-level features)
for name, param in model.named_parameters():
    if "layer3" not in name and "layer4" not in name and "fc" not in name:
        param.requires_grad = False    # freeze everything except layer3, layer4, fc

# Replace final layer
model.fc = nn.Linear(model.fc.in_features, 5)

# Use different learning rates for pretrained vs new layers
optimizer = torch.optim.Adam([
    {"params": model.layer3.parameters(), "lr": 1e-4},    # lower LR for pretrained
    {"params": model.layer4.parameters(), "lr": 1e-4},
    {"params": model.fc.parameters(), "lr": 1e-3},        # higher LR for new layer
])
```

---

## GPU Training

### Device Management

```python
import torch

# Detect available device
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Memory: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB")
elif torch.backends.mps.is_available():
    device = torch.device("mps")        # Apple Silicon GPU
else:
    device = torch.device("cpu")

print(f"Using device: {device}")

# Monitor GPU memory
print(f"Allocated: {torch.cuda.memory_allocated(0) / 1e6:.1f} MB")
print(f"Cached: {torch.cuda.memory_reserved(0) / 1e6:.1f} MB")
torch.cuda.empty_cache()                # free unused cached memory
```

### Multi-GPU with DataParallel

```python
import torch
import torch.nn as nn

model = ConvNet(num_classes=10)

# Wrap model with DataParallel for multi-GPU training
if torch.cuda.device_count() > 1:
    print(f"Using {torch.cuda.device_count()} GPUs")
    model = nn.DataParallel(model)       # splits batches across GPUs

model = model.to(device)

# Access the underlying model when wrapped in DataParallel
if isinstance(model, nn.DataParallel):
    base_model = model.module            # original model without DataParallel
else:
    base_model = model
```

### Mixed Precision Training

```python
import torch
from torch.cuda.amp import autocast, GradScaler

model = ConvNet(num_classes=10).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = torch.nn.CrossEntropyLoss()
scaler = GradScaler()                   # scales loss to prevent underflow in fp16

for batch_X, batch_y in train_loader:
    batch_X, batch_y = batch_X.to(device), batch_y.to(device)

    optimizer.zero_grad()

    # Forward pass in mixed precision (fp16 where safe, fp32 where needed)
    with autocast():
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)

    # Backward pass with gradient scaling
    scaler.scale(loss).backward()        # scale loss to prevent gradient underflow
    scaler.step(optimizer)               # unscale gradients and step
    scaler.update()                      # adjust scale factor
```

---

## Practice Exercises

### Exercise 1: Tensor Manipulation

```python
# Create a 5x5 tensor of random integers between 1 and 100
# 1. Extract the diagonal elements
# 2. Compute the row-wise mean
# 3. Find the index of the maximum value in each column
# 4. Reshape it to (1, 25) and then back to (5, 5)
```

### Exercise 2: Simple Linear Regression

```python
# Implement linear regression from scratch using PyTorch tensors and autograd:
# 1. Generate synthetic data: y = 3x + 2 + noise
# 2. Initialize weight and bias as tensors with requires_grad=True
# 3. Write a training loop that computes MSE loss and updates parameters
# 4. Plot the learned line against the data points
```

### Exercise 3: MNIST Classifier

```python
# Build and train a neural network to classify MNIST handwritten digits:
# 1. Load MNIST dataset using torchvision
# 2. Define a network with at least 2 hidden layers and dropout
# 3. Train for 10 epochs with Adam optimizer
# 4. Evaluate on the test set and print accuracy
# 5. Save the trained model weights
```

### Exercise 4: CNN on CIFAR-10

```python
# Build a convolutional neural network for CIFAR-10:
# 1. Use at least 3 convolutional layers with batch normalization
# 2. Add data augmentation transforms for training
# 3. Implement the full training loop with validation
# 4. Track and plot training/validation loss and accuracy
# 5. Achieve at least 80% test accuracy
```

### Exercise 5: Transfer Learning

```python
# Use a pretrained model to classify a custom dataset:
# 1. Load a pretrained ResNet-18
# 2. Freeze the feature extractor layers
# 3. Replace the classification head for your number of classes
# 4. Train only the new layers for 5 epochs
# 5. Unfreeze the last residual block, fine-tune for 5 more epochs, and compare accuracy
```

---

## Summary

These notes cover the fundamental concepts of PyTorch:

1. **Tensors**: Creation, operations, shapes, dtypes, and GPU placement with `.to(device)`
2. **Autograd**: `requires_grad`, `.backward()`, gradient accumulation, and `torch.no_grad()`
3. **nn.Module**: Defining networks with layers, `forward()` method, and `nn.Sequential`
4. **Common Layers**: `Linear`, `Conv2d`, `ReLU`, `BatchNorm2d`, `Dropout`, pooling
5. **Training Loop**: Forward pass, loss computation, backward pass, optimizer step, train/eval modes
6. **Data Loading**: Custom `Dataset`, `DataLoader`, transforms, torchvision datasets
7. **Saving/Loading**: `state_dict()` for weights, full checkpoints for resuming training
8. **Transfer Learning**: Pretrained models, freezing layers, fine-tuning with differential LRs
9. **GPU Training**: Device management, `DataParallel`, mixed precision with `autocast`

### Next Steps

1. Explore `DistributedDataParallel` for efficient multi-GPU and multi-node training
2. Learn TorchScript and ONNX export for model deployment
3. Study advanced architectures: Transformers, GANs, autoencoders
4. Experiment with learning rate scheduling and hyperparameter tuning
5. Explore PyTorch Lightning or Hugging Face Trainer for simplified training workflows

### Additional Resources

- **PyTorch Documentation**: https://pytorch.org/docs/stable/
- **PyTorch Tutorials**: https://pytorch.org/tutorials/
- **Deep Learning with PyTorch (book)**: https://pytorch.org/assets/deep-learning/Deep-Learning-with-PyTorch.pdf
- **PyTorch Examples**: https://github.com/pytorch/examples
- **Torchvision Models**: https://pytorch.org/vision/stable/models.html
