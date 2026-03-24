# Introduction to Keras

## Table of Contents

1. [What is Keras?](#what-is-keras)
2. [Installation and Setup](#installation-and-setup)
3. [Sequential API](#sequential-api)
4. [Functional API](#functional-api)
5. [Core Layers](#core-layers)
6. [Compiling Models](#compiling-models)
7. [Training Models](#training-models)
8. [Callbacks](#callbacks)
9. [Custom Layers and Models](#custom-layers-and-models)
10. [Data Preprocessing](#data-preprocessing)
11. [Saving and Loading](#saving-and-loading)
12. [Practice Exercises](#practice-exercises)
13. [Summary](#summary)

---

## What is Keras?

Keras is a high-level deep learning API that provides a clean, intuitive interface for building and training neural networks. Key characteristics:

- **High-Level API**: Abstracts away low-level tensor operations into readable, composable building blocks
- **Multi-Backend (Keras 3)**: Supports TensorFlow, PyTorch, and JAX as interchangeable backends
- **Eager and Graph Execution**: Works in both eager mode (debugging) and graph mode (performance)
- **Production-Ready**: Scales from laptop experiments to distributed multi-GPU training
- **Ecosystem Integration**: Works with TensorBoard, TensorFlow Serving, and the broader ML ecosystem

---

## Installation and Setup

```bash
# Install Keras 3 (multi-backend version)
pip install keras

# Install at least one backend
pip install tensorflow    # TensorFlow backend
pip install torch         # PyTorch backend
pip install jax jaxlib    # JAX backend
```

```python
# Set the backend before importing Keras (or use KERAS_BACKEND env var)
import os
os.environ["KERAS_BACKEND"] = "tensorflow"  # options: "tensorflow", "torch", "jax"

import keras
print(keras.__version__)  # verify installation
```

```python
# Common imports for building models
from keras import layers, models, optimizers, losses, metrics, callbacks
from keras.datasets import mnist, cifar10  # built-in datasets
import numpy as np
```

---

## Sequential API

The Sequential API is the simplest way to build models by stacking layers linearly, one after another. Best for straightforward architectures with a single input and single output.

```python
from keras import layers, models

# Build a simple feedforward network for classification
model = models.Sequential([
    layers.Dense(128, activation="relu", input_shape=(784,)),  # first layer needs input_shape
    layers.Dropout(0.3),                                       # regularization
    layers.Dense(64, activation="relu"),                        # hidden layer
    layers.Dropout(0.3),
    layers.Dense(10, activation="softmax"),                     # output: 10 classes
])

model.summary()  # print layer names, output shapes, and param counts
```

```python
# Build a CNN with Sequential API
cnn_model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)),  # 32 filters, 3x3 kernel
    layers.MaxPooling2D((2, 2)),                                            # downsample by 2x
    layers.Conv2D(64, (3, 3), activation="relu"),                           # more filters in deeper layers
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),          # convert 2D feature maps to 1D vector
    layers.Dense(64, activation="relu"),
    layers.Dense(10, activation="softmax"),
])
```

```python
# You can also add layers incrementally with model.add()
model = models.Sequential()
model.add(layers.Dense(256, activation="relu", input_shape=(100,)))
model.add(layers.BatchNormalization())
model.add(layers.Dense(128, activation="relu"))
model.add(layers.Dense(1, activation="sigmoid"))  # binary classification output
```

---

## Functional API

The Functional API allows you to build complex architectures with multiple inputs, multiple outputs, shared layers, and non-linear connectivity (skip connections, branching).

```python
from keras import layers, models

# Basic Functional API pattern: define inputs, chain layers, create model
inputs = layers.Input(shape=(784,))              # explicit input tensor
x = layers.Dense(128, activation="relu")(inputs) # call layer on tensor
x = layers.Dropout(0.3)(x)
x = layers.Dense(64, activation="relu")(x)
outputs = layers.Dense(10, activation="softmax")(x)

model = models.Model(inputs=inputs, outputs=outputs)  # define model with inputs/outputs
```

```python
# Multiple inputs: combine image features with tabular data
image_input = layers.Input(shape=(64, 64, 3), name="image_input")
x1 = layers.Conv2D(32, (3, 3), activation="relu")(image_input)
x1 = layers.MaxPooling2D((2, 2))(x1)
x1 = layers.Flatten()(x1)

metadata_input = layers.Input(shape=(10,), name="metadata_input")
x2 = layers.Dense(32, activation="relu")(metadata_input)

merged = layers.concatenate([x1, x2])           # merge branches along last axis
output = layers.Dense(1, activation="sigmoid")(layers.Dense(64, activation="relu")(merged))
model = models.Model(inputs=[image_input, metadata_input], outputs=output)
```

```python
# Multiple outputs: predict category and severity simultaneously
inputs = layers.Input(shape=(100,))
shared = layers.Dense(128, activation="relu")(inputs)  # shared representation

category_out = layers.Dense(64, activation="relu")(shared)              # classification head
category_out = layers.Dense(5, activation="softmax", name="category")(category_out)

severity_out = layers.Dense(64, activation="relu")(shared)              # regression head
severity_out = layers.Dense(1, activation="linear", name="severity")(severity_out)

model = models.Model(inputs=inputs, outputs=[category_out, severity_out])
model.compile(
    optimizer="adam",
    loss={"category": "categorical_crossentropy", "severity": "mse"},
    loss_weights={"category": 1.0, "severity": 0.5},  # weight classification more
    metrics={"category": "accuracy", "severity": "mae"},
)
```

```python
# Shared layers: reuse the same layer (same weights) on different inputs
shared_dense = layers.Dense(64, activation="relu")  # define once

input_a = layers.Input(shape=(50,))
input_b = layers.Input(shape=(50,))
processed_a = shared_dense(input_a)  # same weights applied to both
processed_b = shared_dense(input_b)

merged = layers.concatenate([processed_a, processed_b])
output = layers.Dense(1, activation="sigmoid")(merged)
siamese_model = models.Model(inputs=[input_a, input_b], outputs=output)
```

---

## Core Layers

```python
from keras import layers

# Dense (fully connected) — every neuron connects to every input
dense = layers.Dense(
    units=128,              # number of output neurons
    activation="relu",      # activation function (relu, sigmoid, tanh, softmax, etc.)
    kernel_initializer="he_normal",  # weight initialization strategy
    kernel_regularizer="l2",         # L2 weight penalty to reduce overfitting
)

# Conv2D — spatial feature extraction for images
conv = layers.Conv2D(
    filters=64,             # number of output filters
    kernel_size=(3, 3),     # size of the convolution window
    strides=(1, 1),         # step size of the convolution
    padding="same",         # "same" preserves spatial dims, "valid" shrinks them
    activation="relu",
)

# MaxPooling2D — downsample spatial dimensions by taking the max in each window
pool = layers.MaxPooling2D(
    pool_size=(2, 2),       # each 2x2 region becomes a single value
)

# Flatten — reshape multi-dimensional tensor into 1D (e.g., before Dense layers)
flatten = layers.Flatten()  # (batch, 8, 8, 64) -> (batch, 4096)
```

```python
# Dropout — randomly set a fraction of inputs to 0 during training (regularization)
dropout = layers.Dropout(
    rate=0.5,               # 50% of neurons are randomly deactivated per training step
)                           # automatically disabled during inference

# BatchNormalization — normalize layer inputs for faster, more stable training
bn = layers.BatchNormalization()  # learns scale and shift parameters
# Typically placed after Dense/Conv2D and before activation, or after activation

# LSTM — long short-term memory for sequence data (text, time series)
lstm = layers.LSTM(
    units=128,              # dimensionality of the output space
    return_sequences=True,  # True: return output at each timestep; False: only last
    dropout=0.2,            # dropout on inputs
    recurrent_dropout=0.2,  # dropout on recurrent connections
)

# Embedding — map integer tokens to dense vectors (first layer for NLP)
embedding = layers.Embedding(
    input_dim=10000,        # vocabulary size
    output_dim=128,         # dimensionality of embedding vectors
    input_length=200,       # length of input sequences (optional)
)
```

---

## Compiling Models

Compiling configures the model for training by specifying the loss function, optimizer, and metrics.

```python
from keras import optimizers, losses

# Basic compilation with string shortcuts
model.compile(
    optimizer="adam",                        # adaptive learning rate optimizer
    loss="sparse_categorical_crossentropy", # for integer labels (0, 1, 2, ...)
    metrics=["accuracy"],                   # track accuracy during training
)

# Detailed compilation with configured optimizer
model.compile(
    optimizer=optimizers.Adam(learning_rate=0.001, clipnorm=1.0),
    loss=losses.CategoricalCrossentropy(label_smoothing=0.1),  # soften hard labels
    metrics=["accuracy"],
)
```

```python
# Common loss functions by task type
# Binary classification (sigmoid output):   loss="binary_crossentropy"
# Multi-class (integer labels, softmax):    loss="sparse_categorical_crossentropy"
# Multi-class (one-hot labels, softmax):    loss="categorical_crossentropy"
# Regression (linear output):              loss="mse", "mae", or "huber"

# Common optimizers:
# "sgd"     — stochastic gradient descent (simple, needs tuning)
# "adam"    — adaptive moment estimation (good default)
# "rmsprop" — good for RNNs and recurrent models
# "adamw"  — adam with decoupled weight decay
```

---

## Training Models

```python
from keras.datasets import mnist
import numpy as np

# Load and preprocess data
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(-1, 784).astype("float32") / 255.0  # flatten and normalize
x_test = x_test.reshape(-1, 784).astype("float32") / 255.0

# Train the model with fit()
history = model.fit(
    x_train, y_train,
    epochs=20,               # number of passes through the full dataset
    batch_size=128,          # samples per gradient update
    validation_split=0.2,   # hold out 20% of training data for validation
    verbose=1,               # 1: progress bar, 2: one line per epoch, 0: silent
)
```

```python
# Access training history for plotting (history.history is a dict of per-epoch metrics)
import matplotlib.pyplot as plt

plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")
plt.xlabel("Epoch")
plt.legend()
plt.show()
```

```python
# Evaluate on test set — returns [loss, metric1, metric2, ...]
test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
print(f"Test accuracy: {test_accuracy:.4f}")

# Predict on new data — returns probabilities for each class
predictions = model.predict(x_test[:5])    # shape: (5, 10) for 10 classes
predicted_classes = np.argmax(predictions, axis=1)  # convert probabilities to class labels
print(f"Predicted classes: {predicted_classes}")
```

```python
# Handle class imbalance with class_weight
from sklearn.utils.class_weight import compute_class_weight

class_weights = compute_class_weight("balanced", classes=np.unique(y_train), y=y_train)
class_weight_dict = dict(enumerate(class_weights))  # {0: 1.2, 1: 0.8, ...}

model.fit(x_train, y_train, epochs=20, batch_size=128,
          class_weight=class_weight_dict, validation_split=0.2)
```

---

## Callbacks

Callbacks let you hook into the training loop to add custom behavior at each epoch or batch.

```python
from keras import callbacks

# ModelCheckpoint — save the best model during training
checkpoint = callbacks.ModelCheckpoint(
    filepath="best_model.keras",  # save path
    monitor="val_loss",           # metric to watch
    save_best_only=True,          # only overwrite if metric improves
    mode="min",                   # "min" for loss, "max" for accuracy
    verbose=1,
)

# EarlyStopping — stop training when validation metric stops improving
early_stop = callbacks.EarlyStopping(
    monitor="val_loss",
    patience=5,                   # wait 5 epochs before stopping
    restore_best_weights=True,    # revert to best weights when stopped
    min_delta=0.001,              # minimum change to count as improvement
)

# ReduceLROnPlateau — lower learning rate when metric plateaus
reduce_lr = callbacks.ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,                   # multiply LR by this factor
    patience=3,                   # epochs to wait before reducing
    min_lr=1e-7,                  # lower bound on learning rate
    verbose=1,
)
```

```python
# TensorBoard — log metrics and visualizations for the TensorBoard UI
tensorboard = callbacks.TensorBoard(
    log_dir="./logs",             # directory for log files
    histogram_freq=1,             # log weight histograms every epoch
)

# Use callbacks by passing a list to fit()
model.fit(x_train, y_train, epochs=100, batch_size=128, validation_split=0.2,
          callbacks=[checkpoint, early_stop, reduce_lr, tensorboard])
```

```python
# Custom callback — subclass keras.callbacks.Callback
class TrainingMonitor(callbacks.Callback):
    def on_train_begin(self, logs=None):
        self.best_loss = float("inf")

    def on_epoch_end(self, epoch, logs=None):
        current_loss = logs.get("val_loss")  # logs has loss, val_loss, accuracy, etc.
        if current_loss < self.best_loss:
            self.best_loss = current_loss
            print(f"\nEpoch {epoch + 1}: new best val_loss = {current_loss:.4f}")

    def on_train_end(self, logs=None):
        print(f"\nTraining complete. Best val_loss: {self.best_loss:.4f}")

# Use it like any other callback
model.fit(x_train, y_train, epochs=20, callbacks=[TrainingMonitor()])
```

---

## Custom Layers and Models

### Custom Layer

Subclass `keras.layers.Layer` to create reusable layers with learnable parameters.

```python
import keras
from keras import ops  # backend-agnostic operations (Keras 3)

class LinearWithConstraint(keras.layers.Layer):
    def __init__(self, units, **kwargs):
        super().__init__(**kwargs)
        self.units = units

    def build(self, input_shape):
        # Create trainable weights — called once when the layer first receives input
        self.w = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer="glorot_uniform",
            trainable=True,
            name="kernel",
        )
        self.b = self.add_weight(
            shape=(self.units,),
            initializer="zeros",
            trainable=True,
            name="bias",
        )

    def call(self, inputs):
        # Forward pass logic
        return ops.matmul(inputs, self.w) + self.b  # linear transformation

    def get_config(self):
        # Required for serialization (saving/loading)
        config = super().get_config()
        config.update({"units": self.units})
        return config

# Use it like any built-in layer
layer = LinearWithConstraint(64)
```

### Custom Model

Subclass `keras.Model` for full control over the forward pass.

```python
class Autoencoder(keras.Model):
    def __init__(self, latent_dim, **kwargs):
        super().__init__(**kwargs)
        self.latent_dim = latent_dim
        self.encoder_dense1 = keras.layers.Dense(128, activation="relu")   # encoder
        self.encoder_dense2 = keras.layers.Dense(latent_dim, activation="relu")
        self.decoder_dense1 = keras.layers.Dense(128, activation="relu")   # decoder
        self.decoder_dense2 = keras.layers.Dense(784, activation="sigmoid")

    def call(self, inputs):
        # Forward pass: encode then decode
        encoded = self.encoder_dense2(self.encoder_dense1(inputs))
        return self.decoder_dense2(self.decoder_dense1(encoded))

    def encode(self, inputs):
        # Expose encoder separately for inference
        return self.encoder_dense2(self.encoder_dense1(inputs))

# Instantiate and compile like any model
autoencoder = Autoencoder(latent_dim=32)
autoencoder.compile(optimizer="adam", loss="mse")
autoencoder.fit(x_train, x_train, epochs=10, batch_size=256)  # input == target for autoencoders
```

---

## Data Preprocessing

### Image Preprocessing

```python
from keras.preprocessing.image import ImageDataGenerator

# Augmentation for training — generates transformed versions of images on the fly
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,          # normalize pixel values to [0, 1]
    rotation_range=20,          # random rotation up to 20 degrees
    width_shift_range=0.2,      # horizontal shift up to 20% of width
    height_shift_range=0.2,     # vertical shift up to 20% of height
    horizontal_flip=True,       # randomly flip images horizontally
    fill_mode="nearest",        # fill strategy for new pixels after transforms
)

# Validation data should only be rescaled, not augmented
val_datagen = ImageDataGenerator(rescale=1.0 / 255)

# Load images from directory structure: base_dir/class_name/image.jpg
train_generator = train_datagen.flow_from_directory(
    "data/train", target_size=(150, 150), batch_size=32, class_mode="categorical",
)
val_generator = val_datagen.flow_from_directory(
    "data/validation", target_size=(150, 150), batch_size=32, class_mode="categorical",
)

# Train with generators
model.fit(train_generator, epochs=20, validation_data=val_generator)
```

### Text Preprocessing

```python
from keras.preprocessing.text import text_to_word_sequence, Tokenizer
from keras.utils import pad_sequences

# text_to_word_sequence — basic tokenization and lowercasing
text = "Keras makes deep learning accessible!"
tokens = text_to_word_sequence(text)  # ['keras', 'makes', 'deep', 'learning', 'accessible']

# Tokenizer — build a word-to-index mapping from a corpus
tokenizer = Tokenizer(
    num_words=10000,            # keep only the top 10,000 most frequent words
    oov_token="<OOV>",         # out-of-vocabulary token for unknown words
)

texts = ["I love deep learning", "Keras is great for beginners", "Neural networks learn patterns"]
tokenizer.fit_on_texts(texts)                       # build vocabulary from training texts
sequences = tokenizer.texts_to_sequences(texts)     # convert texts to integer sequences
word_index = tokenizer.word_index                    # vocabulary: {'i': 2, 'love': 3, ...}
print(f"Vocabulary size: {len(word_index)}")
```

```python
# pad_sequences — ensure all sequences have the same length
padded = pad_sequences(
    sequences,
    maxlen=20,               # pad or truncate to this length
    padding="post",          # add zeros at the end ("pre" adds at the beginning)
    truncating="post",       # remove tokens from the end if too long
)
print(padded.shape)          # (3, 20) — each sequence is now exactly 20 tokens
```

---

## Saving and Loading

```python
# Save the entire model (architecture + weights + optimizer state)
model.save("my_model.keras")  # recommended Keras 3 format

# Load the full model
loaded_model = keras.models.load_model("my_model.keras")
loaded_model.evaluate(x_test, y_test)  # immediately usable

# Save weights only (useful for custom models or fine-tuning)
model.save_weights("model_weights.weights.h5")

# Load weights into a model with the same architecture
new_model = build_model()                          # recreate architecture
new_model.load_weights("model_weights.weights.h5") # load saved weights
```

```python
# Save with custom objects (custom layers, losses, etc.)
model.save("custom_model.keras")

# Load with custom object scope
loaded = keras.models.load_model(
    "custom_model.keras",
    custom_objects={"LinearWithConstraint": LinearWithConstraint},  # register custom classes
)
```

---

## Practice Exercises

### Exercise 1: MNIST Classifier with Sequential API

```python
# Build a Dense network for MNIST digit classification
# Target: > 97% test accuracy
from keras.datasets import mnist
from keras import layers, models
import numpy as np

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(-1, 784).astype("float32") / 255.0
x_test = x_test.reshape(-1, 784).astype("float32") / 255.0

model = models.Sequential([
    layers.Dense(256, activation="relu", input_shape=(784,)),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    layers.Dense(128, activation="relu"),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    layers.Dense(10, activation="softmax"),
])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(x_train, y_train, epochs=15, batch_size=128, validation_split=0.15)
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"Test accuracy: {test_acc:.4f}")
```

### Exercise 2: CNN for CIFAR-10

```python
# Build a convolutional model for CIFAR-10 image classification
# Target: > 75% test accuracy with data augmentation
from keras.datasets import cifar10
from keras import layers, models, callbacks
from keras.preprocessing.image import ImageDataGenerator

(x_train, y_train), (x_test, y_test) = cifar10.load_data()
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation="relu", padding="same", input_shape=(32, 32, 3)),
    layers.BatchNormalization(),
    layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),
    layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
    layers.BatchNormalization(),
    layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.5),
    layers.Dense(10, activation="softmax"),
])

datagen = ImageDataGenerator(rotation_range=15, horizontal_flip=True, width_shift_range=0.1)
datagen.fit(x_train)

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(datagen.flow(x_train, y_train, batch_size=64), epochs=30,
          validation_data=(x_test, y_test),
          callbacks=[callbacks.EarlyStopping(patience=5, restore_best_weights=True)])
```

### Exercise 3: Functional API with Multiple Inputs

```python
# Build a model that takes both image features and metadata
from keras import layers, models
import numpy as np

image_data = np.random.rand(1000, 64, 64, 3).astype("float32")  # simulated images
metadata = np.random.rand(1000, 5).astype("float32")             # simulated tabular data
labels = np.random.randint(0, 3, size=(1000,))

img_input = layers.Input(shape=(64, 64, 3), name="image")
x1 = layers.Conv2D(16, (3, 3), activation="relu")(img_input)
x1 = layers.MaxPooling2D((2, 2))(x1)
x1 = layers.Flatten()(x1)

meta_input = layers.Input(shape=(5,), name="metadata")
x2 = layers.Dense(16, activation="relu")(meta_input)

merged = layers.concatenate([x1, x2])
output = layers.Dense(3, activation="softmax")(merged)

model = models.Model(inputs=[img_input, meta_input], outputs=output)
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit({"image": image_data, "metadata": metadata}, labels, epochs=10, batch_size=32)
```

---

## Summary

These notes cover the fundamental concepts of Keras for deep learning:

1. **What is Keras**: A high-level deep learning API, now multi-backend (Keras 3) supporting TensorFlow, PyTorch, and JAX
2. **Sequential API**: Simple layer stacking for linear architectures with `models.Sequential`
3. **Functional API**: Complex architectures with multiple inputs/outputs, shared layers, and skip connections
4. **Core Layers**: Dense, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization, LSTM, Embedding
5. **Compiling Models**: Configuring loss functions, optimizers, and metrics for training
6. **Training**: Using `fit`, `evaluate`, `predict`, `validation_split`, and `class_weight` for model training
7. **Callbacks**: ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard, and custom callbacks
8. **Custom Layers and Models**: Subclassing `Layer` and `Model` for custom architectures and operations
9. **Data Preprocessing**: ImageDataGenerator for augmentation, Tokenizer and pad_sequences for text
10. **Saving and Loading**: Full model persistence, weights-only saving, and JSON architecture export

### Next Steps

1. Work through the practice exercises with real datasets and experiment with hyperparameters
2. Explore transfer learning with pre-trained models (ResNet, EfficientNet, BERT) via `keras.applications`
3. Learn about custom training loops using `keras.Model.train_step` or GradientTape
4. Study distributed training across multiple GPUs with `keras.distribution`
5. Explore Keras-NLP and Keras-CV for domain-specific high-level components
6. Experiment with switching backends (TensorFlow, PyTorch, JAX) to compare performance

### Additional Resources

- **Keras Documentation**: https://keras.io/
- **Keras API Reference**: https://keras.io/api/
- **Keras Guides**: https://keras.io/guides/
- **Keras Code Examples**: https://keras.io/examples/
- **Keras GitHub Repository**: https://github.com/keras-team/keras
