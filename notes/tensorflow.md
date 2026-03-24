# Introduction to TensorFlow

## Table of Contents

1. [What is TensorFlow?](#what-is-tensorflow)
2. [Installation and Setup](#installation-and-setup)
3. [Tensors](#tensors)
4. [Keras API](#keras-api)
5. [Building Models](#building-models)
6. [Compiling and Training](#compiling-and-training)
7. [Datasets with tf.data](#datasets-with-tfdata)
8. [Callbacks](#callbacks)
9. [Saving and Loading Models](#saving-and-loading-models)
10. [Transfer Learning](#transfer-learning)
11. [TensorBoard](#tensorboard)
12. [Practice Exercises](#practice-exercises)
13. [Summary](#summary)

---

## What is TensorFlow?

TensorFlow is an open-source machine learning framework developed by Google. It provides a comprehensive ecosystem for building, training, and deploying ML models at scale.

- **Eager Execution**: TensorFlow 2 runs operations immediately (like NumPy), making debugging and prototyping intuitive
- **TF2 vs TF1**: TF1 relied on static computation graphs and `tf.Session()`; TF2 uses eager execution by default with `tf.function` for graph optimization when needed
- **Keras Integration**: `tf.keras` is the official high-level API, built directly into TensorFlow 2
- **Hardware Acceleration**: Native support for GPU and TPU training
- **Production Ready**: Tools for deployment (TF Serving, TF Lite, TensorFlow.js)

```python
import tensorflow as tf

# Verify installation and check for GPU
print(f"TensorFlow version: {tf.__version__}")
print(f"Eager execution:    {tf.executing_eagerly()}")  # True by default in TF2
print(f"GPU available:      {len(tf.config.list_physical_devices('GPU')) > 0}")
print(f"Num GPUs:           {len(tf.config.list_physical_devices('GPU'))}")
```

---

## Installation and Setup

```bash
# CPU-only installation
pip install tensorflow

# GPU support (requires CUDA and cuDNN)
pip install tensorflow[and-cuda]

# Verify installation
python -c "import tensorflow as tf; print(tf.__version__)"
```

```python
import tensorflow as tf
import numpy as np

# GPU memory management (optional, prevents TF from allocating all GPU memory)
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)  # allocate memory as needed

# Set random seed for reproducibility
tf.random.set_seed(42)
np.random.seed(42)

# Common imports
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.datasets import mnist, cifar10
```

---

## Tensors

Tensors are the fundamental data structure in TensorFlow, similar to NumPy arrays but with GPU support and automatic differentiation.

### Creating Tensors

```python
import tensorflow as tf
import numpy as np

# Constants (immutable)
scalar = tf.constant(7)                              # rank-0 tensor (scalar)
vector = tf.constant([1, 2, 3])                      # rank-1 tensor (vector)
matrix = tf.constant([[1, 2], [3, 4]])               # rank-2 tensor (matrix)
tensor_3d = tf.constant([[[1, 2], [3, 4]],
                          [[5, 6], [7, 8]]])         # rank-3 tensor

print(f"Scalar: {scalar}, shape: {scalar.shape}, dtype: {scalar.dtype}")
print(f"Vector: {vector}, shape: {vector.shape}")
print(f"Matrix shape: {matrix.shape}, ndim: {matrix.ndim}")

# Variables (mutable, used for model parameters)
var = tf.Variable([1.0, 2.0, 3.0])         # trainable by default
var.assign([4.0, 5.0, 6.0])                # update values in-place
var[0].assign(10.0)                         # update single element
print(f"Variable: {var.numpy()}")

# Special tensors
zeros = tf.zeros([3, 4])                    # 3x4 matrix of zeros
ones = tf.ones([2, 3])                      # 2x3 matrix of ones
eye = tf.eye(3)                             # 3x3 identity matrix
rand_normal = tf.random.normal([3, 3], mean=0.0, stddev=1.0)   # normal distribution
rand_uniform = tf.random.uniform([2, 4], minval=0, maxval=10)  # uniform distribution
linspace = tf.linspace(0.0, 1.0, 5)        # [0.0, 0.25, 0.5, 0.75, 1.0]
range_t = tf.range(0, 10, delta=2)          # [0, 2, 4, 6, 8]
```

### Tensor Operations

```python
import tensorflow as tf

a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
b = tf.constant([[5.0, 6.0], [7.0, 8.0]])

# Element-wise operations
add = tf.add(a, b)              # or a + b
sub = tf.subtract(a, b)         # or a - b
mul = tf.multiply(a, b)         # or a * b (element-wise)
div = tf.divide(a, b)           # or a / b

# Matrix multiplication
matmul = tf.matmul(a, b)        # or a @ b
print(f"Matrix multiply:\n{matmul.numpy()}")

# Reduction operations
print(f"Sum all:    {tf.reduce_sum(a).numpy()}")         # 10.0
print(f"Sum axis=0: {tf.reduce_sum(a, axis=0).numpy()}")  # [4.0, 6.0] (column sums)
print(f"Sum axis=1: {tf.reduce_sum(a, axis=1).numpy()}")  # [3.0, 7.0] (row sums)
print(f"Mean:       {tf.reduce_mean(a).numpy()}")          # 2.5
print(f"Max:        {tf.reduce_max(a).numpy()}")           # 4.0
print(f"Argmax:     {tf.argmax(a, axis=1).numpy()}")       # [1, 1] (index of max per row)

# Reshape and transpose
c = tf.constant([[1, 2, 3], [4, 5, 6]])
reshaped = tf.reshape(c, [3, 2])       # reshape to 3x2
transposed = tf.transpose(c)           # swap rows and columns
expanded = tf.expand_dims(c, axis=0)   # add batch dimension: [1, 2, 3]
squeezed = tf.squeeze(expanded)        # remove dimensions of size 1
print(f"Original:   {c.shape}")        # (2, 3)
print(f"Reshaped:   {reshaped.shape}") # (3, 2)
print(f"Transposed: {transposed.shape}") # (3, 2)
print(f"Expanded:   {expanded.shape}") # (1, 2, 3)
```

### Data Types and Casting

```python
import tensorflow as tf

# Specifying dtype
float_tensor = tf.constant([1, 2, 3], dtype=tf.float32)  # explicit float32
int_tensor = tf.constant([1, 2, 3], dtype=tf.int64)       # explicit int64

# Casting between types
casted = tf.cast(int_tensor, dtype=tf.float32)    # int64 -> float32
to_int = tf.cast(float_tensor, dtype=tf.int32)    # float32 -> int32

# Convert between TF tensors and NumPy
import numpy as np
np_array = np.array([1.0, 2.0, 3.0])
tf_from_np = tf.constant(np_array)          # NumPy -> TensorFlow
np_from_tf = float_tensor.numpy()           # TensorFlow -> NumPy
print(f"NumPy array: {np_from_tf}, type: {type(np_from_tf)}")
```

### GPU Operations

```python
import tensorflow as tf

# Check device placement
tensor_a = tf.constant([[1.0, 2.0]])
print(f"Device: {tensor_a.device}")  # e.g., /job:localhost/replica:0/task:0/device:CPU:0

# Explicit device placement
with tf.device('/CPU:0'):
    cpu_tensor = tf.constant([1.0, 2.0])

if tf.config.list_physical_devices('GPU'):
    with tf.device('/GPU:0'):
        gpu_tensor = tf.constant([1.0, 2.0])  # created on GPU
        result = gpu_tensor * 2                 # computed on GPU
        print(f"GPU result: {result.numpy()}")
```

---

## Keras API

### Sequential Model

```python
import tensorflow as tf
from tensorflow.keras import layers, models

# Sequential: stack layers linearly, one after another
model = models.Sequential([
    layers.Dense(128, activation='relu', input_shape=(784,)),  # first layer needs input_shape
    layers.Dropout(0.2),                                        # regularization
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')                      # output: 10 classes
])

# Alternative: add layers one at a time
model_alt = models.Sequential()
model_alt.add(layers.Dense(128, activation='relu', input_shape=(784,)))
model_alt.add(layers.Dropout(0.2))
model_alt.add(layers.Dense(64, activation='relu'))
model_alt.add(layers.Dense(10, activation='softmax'))

# View model architecture
model.summary()

# Output:
# Model: "sequential"
# ┌─────────────────────────────────┬────────────────────────┬───────────────┐
# │ Layer (type)                    │ Output Shape           │       Param # │
# ├─────────────────────────────────┼────────────────────────┼───────────────┤
# │ dense (Dense)                   │ (None, 128)            │       100480  │
# │ dropout (Dropout)               │ (None, 128)            │             0 │
# │ dense_1 (Dense)                 │ (None, 64)             │         8256  │
# │ dense_2 (Dense)                 │ (None, 10)             │          650  │
# └─────────────────────────────────┴────────────────────────┴───────────────┘
# Total params: 109,386
```

### Functional API

```python
import tensorflow as tf
from tensorflow.keras import layers, models

# Functional API: supports complex architectures (multi-input, multi-output, shared layers)
inputs = layers.Input(shape=(784,))                     # define input tensor
x = layers.Dense(256, activation='relu')(inputs)        # chain layers together
x = layers.BatchNormalization()(x)                      # normalize activations
x = layers.Dropout(0.3)(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.3)(x)
outputs = layers.Dense(10, activation='softmax')(x)

model = models.Model(inputs=inputs, outputs=outputs)    # define model with inputs/outputs
model.summary()

# Multi-input model example
input_text = layers.Input(shape=(100,), name='text_input')
input_meta = layers.Input(shape=(5,), name='meta_input')

# Process text branch
text_branch = layers.Dense(64, activation='relu')(input_text)
text_branch = layers.Dropout(0.2)(text_branch)

# Process metadata branch
meta_branch = layers.Dense(16, activation='relu')(input_meta)

# Combine branches
combined = layers.concatenate([text_branch, meta_branch])  # merge along last axis
combined = layers.Dense(32, activation='relu')(combined)
output = layers.Dense(1, activation='sigmoid')(combined)   # binary classification

multi_model = models.Model(
    inputs=[input_text, input_meta],
    outputs=output,
    name='multi_input_model'
)
multi_model.summary()
```

---

## Building Models

### Common Layer Types

```python
import tensorflow as tf
from tensorflow.keras import layers

# Dense (fully connected) layer
dense = layers.Dense(
    units=64,                    # number of neurons
    activation='relu',           # activation function
    kernel_initializer='he_normal',  # weight initialization
    bias_initializer='zeros',
    kernel_regularizer=tf.keras.regularizers.l2(0.01)  # L2 regularization
)

# Conv2D (2D convolution) for image data
conv = layers.Conv2D(
    filters=32,                  # number of output filters
    kernel_size=(3, 3),          # filter size
    strides=(1, 1),              # step size
    padding='same',              # 'same' preserves spatial dims, 'valid' shrinks
    activation='relu'
)

# MaxPooling2D: downsample spatial dimensions
pool = layers.MaxPooling2D(pool_size=(2, 2))  # halves height and width

# LSTM (Long Short-Term Memory) for sequential data
lstm = layers.LSTM(
    units=64,                    # number of hidden units
    return_sequences=True,       # True: output at every timestep; False: only last
    dropout=0.2,                 # dropout on inputs
    recurrent_dropout=0.2        # dropout on recurrent connections
)

# Dropout: randomly set fraction of inputs to 0 during training
dropout = layers.Dropout(rate=0.5)  # 50% of inputs dropped

# BatchNormalization: normalize layer inputs for faster, more stable training
batchnorm = layers.BatchNormalization()

# Flatten: convert multi-dim tensor to 1D (e.g., after Conv2D before Dense)
flatten = layers.Flatten()

# Embedding: map integer indices to dense vectors (for NLP)
embedding = layers.Embedding(
    input_dim=10000,             # vocabulary size
    output_dim=128               # embedding dimension
)
```

### CNN for Image Classification

```python
import tensorflow as tf
from tensorflow.keras import layers, models

# Convolutional Neural Network for 32x32 RGB images (e.g., CIFAR-10)
cnn_model = models.Sequential([
    # First convolutional block
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    layers.BatchNormalization(),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),

    # Second convolutional block
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.BatchNormalization(),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),

    # Classification head
    layers.Flatten(),                    # flatten feature maps to 1D vector
    layers.Dense(512, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')  # 10 output classes
])

cnn_model.summary()
```

### RNN for Sequence Data

```python
import tensorflow as tf
from tensorflow.keras import layers, models

# LSTM model for sequence classification
rnn_model = models.Sequential([
    layers.Embedding(input_dim=10000, output_dim=128, input_length=200),  # word embeddings
    layers.LSTM(64, return_sequences=True),   # first LSTM returns full sequence
    layers.Dropout(0.2),
    layers.LSTM(32, return_sequences=False),  # second LSTM returns last output only
    layers.Dropout(0.2),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')     # binary classification
])

rnn_model.summary()

# Bidirectional LSTM: processes sequence in both directions
bidir_model = models.Sequential([
    layers.Embedding(10000, 128, input_length=200),
    layers.Bidirectional(layers.LSTM(64, return_sequences=True)),  # forward + backward
    layers.Bidirectional(layers.LSTM(32)),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])
```

---

## Compiling and Training

### Compile

```python
import tensorflow as tf
from tensorflow.keras import layers, models

model = models.Sequential([
    layers.Dense(128, activation='relu', input_shape=(784,)),
    layers.Dense(10, activation='softmax')
])

# Compile: configure the model for training
model.compile(
    optimizer='adam',                                # optimization algorithm
    loss='sparse_categorical_crossentropy',          # loss function (integer labels)
    metrics=['accuracy']                             # metrics to track
)

# Common optimizers
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse')
model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9), loss='mse')
model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001), loss='mse')

# Common loss functions
# 'sparse_categorical_crossentropy'   -> multi-class, integer labels (y = [0, 2, 1])
# 'categorical_crossentropy'          -> multi-class, one-hot labels (y = [[1,0,0], [0,0,1]])
# 'binary_crossentropy'               -> binary classification
# 'mse' / 'mean_squared_error'        -> regression
# 'mae' / 'mean_absolute_error'       -> regression

# Common metrics
# 'accuracy'           -> classification
# 'AUC'                -> area under ROC curve
# 'Precision'          -> precision
# 'Recall'             -> recall
# tf.keras.metrics.F1Score(average='macro')  -> F1 score
```

### Fit, Evaluate, Predict

```python
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
import numpy as np

# Load and preprocess MNIST
(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(-1, 784).astype('float32') / 255.0  # flatten and normalize
X_test = X_test.reshape(-1, 784).astype('float32') / 255.0

# Build and compile
model = models.Sequential([
    layers.Dense(128, activation='relu', input_shape=(784,)),
    layers.Dropout(0.2),
    layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(
    X_train, y_train,
    epochs=10,                    # number of full passes through the data
    batch_size=32,                # samples per gradient update
    validation_split=0.2,         # use 20% of training data for validation
    verbose=1                     # 0=silent, 1=progress bar, 2=one line per epoch
)

# Access training history
print(f"Final train accuracy: {history.history['accuracy'][-1]:.4f}")
print(f"Final val accuracy:   {history.history['val_accuracy'][-1]:.4f}")
print(f"Final train loss:     {history.history['loss'][-1]:.4f}")

# Evaluate on test set
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test accuracy: {test_accuracy:.4f}")
print(f"Test loss:     {test_loss:.4f}")

# Make predictions
predictions = model.predict(X_test[:5])          # returns probabilities for each class
predicted_classes = np.argmax(predictions, axis=1)  # convert to class labels
print(f"Predicted: {predicted_classes}")
print(f"Actual:    {y_test[:5]}")
```

---

## Datasets with tf.data

### Creating and Transforming Datasets

```python
import tensorflow as tf
import numpy as np

# Create dataset from tensors
X = np.random.randn(1000, 10).astype(np.float32)
y = np.random.randint(0, 2, 1000).astype(np.float32)

dataset = tf.data.Dataset.from_tensor_slices((X, y))  # pair features with labels
print(f"Dataset element spec: {dataset.element_spec}")

# Inspect elements
for features, label in dataset.take(2):  # take first 2 elements
    print(f"Features shape: {features.shape}, Label: {label.numpy()}")

# Build an efficient input pipeline
train_dataset = (
    tf.data.Dataset.from_tensor_slices((X, y))
    .shuffle(buffer_size=1000)       # randomize order (buffer_size >= dataset size for full shuffle)
    .batch(32)                       # group into batches of 32
    .prefetch(tf.data.AUTOTUNE)      # prefetch next batch while training on current
)

# Iterate over batched dataset
for batch_x, batch_y in train_dataset.take(1):
    print(f"Batch features: {batch_x.shape}")  # (32, 10)
    print(f"Batch labels:   {batch_y.shape}")   # (32,)
```

### Common Dataset Operations

```python
import tensorflow as tf
import numpy as np

# Create sample dataset
dataset = tf.data.Dataset.from_tensor_slices(np.arange(20))

# map: apply a transformation to each element
dataset_squared = dataset.map(lambda x: x ** 2)

# filter: keep only elements matching condition
dataset_even = dataset.filter(lambda x: x % 2 == 0)

# batch: group elements into fixed-size batches
dataset_batched = dataset.batch(5)                       # [0,1,2,3,4], [5,6,7,8,9], ...
dataset_batched_drop = dataset.batch(6, drop_remainder=True)  # drop last incomplete batch

# repeat: repeat the dataset for multiple epochs
dataset_repeated = dataset.batch(5).repeat(3)  # iterate 3 times

# cache: cache dataset in memory or on disk after first epoch
dataset_cached = dataset.cache()               # in memory
dataset_cached_disk = dataset.cache('/tmp/cache')  # on disk

# Full efficient pipeline pattern
def preprocess(features, label):
    features = tf.cast(features, tf.float32) / 255.0   # normalize pixel values
    return features, label

(X_train, y_train), _ = tf.keras.datasets.mnist.load_data()

train_ds = (
    tf.data.Dataset.from_tensor_slices((X_train, y_train))
    .map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)  # parallelize preprocessing
    .cache()                                                  # cache after preprocessing
    .shuffle(10000)
    .batch(64)
    .prefetch(tf.data.AUTOTUNE)                              # overlap data loading and training
)

# Use dataset directly in model.fit
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# model.fit(train_ds, epochs=5)  # pass dataset directly instead of NumPy arrays
```

### Loading Data from Files

```python
import tensorflow as tf

# From CSV files
csv_dataset = tf.data.experimental.make_csv_dataset(
    'data.csv',                    # file pattern (supports glob: 'data/*.csv')
    batch_size=32,
    label_name='target',           # column name to use as label
    num_epochs=1,
    shuffle=True
)

# From TFRecord files (TensorFlow's efficient binary format)
def parse_tfrecord(serialized):
    features = tf.io.parse_single_example(serialized, {
        'image': tf.io.FixedLenFeature([], tf.string),
        'label': tf.io.FixedLenFeature([], tf.int64)
    })
    image = tf.io.decode_raw(features['image'], tf.float32)
    return image, features['label']

# tfrecord_dataset = (
#     tf.data.TFRecordDataset('data.tfrecord')
#     .map(parse_tfrecord)
#     .batch(32)
#     .prefetch(tf.data.AUTOTUNE)
# )

# From image directories (common for image classification)
# Expected structure: root/class_a/img1.jpg, root/class_b/img2.jpg
# train_ds = tf.keras.utils.image_dataset_from_directory(
#     'data/train',
#     image_size=(224, 224),         # resize images
#     batch_size=32,
#     label_mode='categorical'       # one-hot labels
# )
```

---

## Callbacks

Callbacks hook into the training loop to add custom behavior at different stages.

```python
import tensorflow as tf
from tensorflow.keras import callbacks

# ModelCheckpoint: save model at regular intervals
checkpoint_cb = callbacks.ModelCheckpoint(
    filepath='best_model.keras',        # save path
    monitor='val_loss',                  # metric to monitor
    save_best_only=True,                 # only save when val_loss improves
    save_weights_only=False,             # save full model (not just weights)
    verbose=1
)

# EarlyStopping: stop training when metric stops improving
early_stop_cb = callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5,                          # number of epochs with no improvement before stopping
    restore_best_weights=True,           # restore weights from best epoch
    min_delta=0.001,                     # minimum change to qualify as improvement
    verbose=1
)

# TensorBoard: log metrics for visualization
tensorboard_cb = callbacks.TensorBoard(
    log_dir='./logs',                    # directory for log files
    histogram_freq=1,                    # log weight histograms every epoch
    write_graph=True,                    # visualize model graph
    update_freq='epoch'                  # log metrics per epoch
)

# LearningRateScheduler: adjust learning rate during training
def lr_schedule(epoch, lr):
    if epoch < 10:
        return lr                        # keep initial learning rate
    else:
        return lr * tf.math.exp(-0.1)    # exponential decay after epoch 10

lr_scheduler_cb = callbacks.LearningRateScheduler(lr_schedule, verbose=1)

# ReduceLROnPlateau: reduce learning rate when metric plateaus
reduce_lr_cb = callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,                          # multiply lr by this factor
    patience=3,                          # epochs to wait before reducing
    min_lr=1e-6,                         # minimum learning rate
    verbose=1
)

# Use callbacks during training
# history = model.fit(
#     X_train, y_train,
#     epochs=50,
#     validation_split=0.2,
#     callbacks=[checkpoint_cb, early_stop_cb, tensorboard_cb, lr_scheduler_cb]
# )
```

### Custom Callback

```python
import tensorflow as tf
from tensorflow.keras import callbacks

class TrainingMonitor(callbacks.Callback):
    def on_train_begin(self, logs=None):
        print("Training started")
        self.best_loss = float('inf')

    def on_epoch_end(self, epoch, logs=None):
        current_loss = logs.get('val_loss', logs.get('loss'))
        if current_loss < self.best_loss:
            self.best_loss = current_loss
            print(f"  Epoch {epoch+1}: new best loss = {current_loss:.4f}")

    def on_train_end(self, logs=None):
        print(f"Training complete. Best loss: {self.best_loss:.4f}")

# monitor = TrainingMonitor()
# model.fit(X_train, y_train, epochs=10, callbacks=[monitor])
```

---

## Saving and Loading Models

### SavedModel Format (Recommended)

```python
import tensorflow as tf
from tensorflow.keras import layers, models

# Build and train a model
model = models.Sequential([
    layers.Dense(64, activation='relu', input_shape=(10,)),
    layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# SavedModel format: saves architecture, weights, optimizer state, and computation graph
model.save('my_model')                       # saves as directory
# Creates: my_model/saved_model.pb, my_model/variables/, my_model/assets/

# Load the full model
loaded_model = tf.keras.models.load_model('my_model')
print(f"Loaded model type: {type(loaded_model)}")

# Keras format (.keras, recommended for Keras models)
model.save('my_model.keras')                 # single file
loaded_keras = tf.keras.models.load_model('my_model.keras')
```

### HDF5 Format (Legacy)

```python
import tensorflow as tf

# HDF5 format: single file, widely compatible
model.save('my_model.h5')                    # legacy format
loaded_h5 = tf.keras.models.load_model('my_model.h5')

# Save and load weights only (useful for custom architectures)
model.save_weights('model_weights.weights.h5')

# Rebuild the same architecture, then load weights
new_model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(10,)),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
new_model.load_weights('model_weights.weights.h5')
```

### Exporting for Production

```python
import tensorflow as tf

# Export with specific input signature for TF Serving
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(10,)),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy')

# Define the serving signature
@tf.function(input_signature=[tf.TensorSpec(shape=[None, 10], dtype=tf.float32)])
def serve(inputs):
    return {'predictions': model(inputs, training=False)}

# Save with signatures
tf.saved_model.save(model, 'serving_model', signatures={'serving_default': serve})

# Load and use
loaded = tf.saved_model.load('serving_model')
serving_fn = loaded.signatures['serving_default']
sample_input = tf.constant([[1.0] * 10])
result = serving_fn(sample_input)
print(f"Prediction: {result['predictions'].numpy()}")
```

---

## Transfer Learning

### Using Pretrained Models

```python
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2, ResNet50, VGG16

# Load pretrained model (downloads weights on first use)
base_model = MobileNetV2(
    weights='imagenet',         # pretrained on ImageNet (1000 classes)
    include_top=False,          # exclude the classification head
    input_shape=(224, 224, 3)
)

# Available pretrained models in tf.keras.applications:
# MobileNetV2, MobileNetV3Large, MobileNetV3Small  -> lightweight, mobile-friendly
# ResNet50, ResNet101, ResNet152                     -> deep residual networks
# VGG16, VGG19                                       -> classic architectures
# EfficientNetB0-B7                                  -> scalable and efficient
# InceptionV3, Xception                              -> inception-based architectures
# DenseNet121, DenseNet169, DenseNet201              -> densely connected

print(f"Base model layers: {len(base_model.layers)}")
print(f"Base model output: {base_model.output_shape}")  # (None, 7, 7, 1280)
```

### Feature Extraction

```python
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2

# Feature extraction: freeze pretrained layers and add custom head
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # freeze all pretrained weights

# Add custom classification layers on top
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),    # reduce spatial dims to single vector per filter
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(5, activation='softmax')  # 5 custom classes
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()
# Note: only the new layers have trainable parameters
# base_model params are frozen (non-trainable)

# Preprocess inputs to match pretrained model's expected format
# preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input
# X_train_processed = preprocess_input(X_train)
```

### Fine-Tuning

```python
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2

base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Step 1: Train with frozen base (feature extraction)
base_model.trainable = False
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(5, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
# model.fit(train_ds, epochs=5, validation_data=val_ds)

# Step 2: Unfreeze top layers of base model for fine-tuning
base_model.trainable = True
fine_tune_at = 100  # freeze all layers before this index

for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False  # keep early layers frozen (general features)

# Recompile with lower learning rate to avoid destroying pretrained weights
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),  # much lower lr for fine-tuning
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
# model.fit(train_ds, epochs=10, validation_data=val_ds)

print(f"Total layers:     {len(base_model.layers)}")
print(f"Trainable layers: {sum(1 for l in base_model.layers if l.trainable)}")
print(f"Frozen layers:    {sum(1 for l in base_model.layers if not l.trainable)}")
```

---

## TensorBoard

### Logging Metrics

```python
import tensorflow as tf
import numpy as np
import datetime

# Create log directory with timestamp
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# TensorBoard callback for Keras training
tensorboard_cb = tf.keras.callbacks.TensorBoard(
    log_dir=log_dir,
    histogram_freq=1,             # log weight histograms every epoch
    write_graph=True,             # visualize computation graph
    write_images=False,
    update_freq='epoch',
    profile_batch=0               # disable profiling (set to '2,5' to profile batches 2-5)
)

# Use during training
# model.fit(X_train, y_train, epochs=20, validation_split=0.2, callbacks=[tensorboard_cb])

# Custom scalar logging with tf.summary
log_dir_custom = "logs/custom/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
writer = tf.summary.create_file_writer(log_dir_custom)

with writer.as_default():
    for step in range(100):
        # Log custom scalars
        tf.summary.scalar('custom_loss', np.random.random(), step=step)
        tf.summary.scalar('custom_metric', np.sin(step * 0.1), step=step)

        # Log histograms
        tf.summary.histogram('weight_dist', tf.random.normal([100]), step=step)

        # Log images (expects [batch, height, width, channels])
        if step % 10 == 0:
            random_image = tf.random.uniform([1, 28, 28, 1])
            tf.summary.image('sample_image', random_image, step=step)

writer.close()
```

### Launching TensorBoard

```bash
# Launch TensorBoard (run in terminal)
tensorboard --logdir=logs/

# Access at http://localhost:6006

# Compare multiple runs
tensorboard --logdir=logs/ --port=6006

# In Jupyter notebooks
# %load_ext tensorboard
# %tensorboard --logdir logs/
```

---

## Practice Exercises

### Exercise 1: MNIST Classifier with CNN

```python
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
import numpy as np

# Load and preprocess MNIST
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
X_train = X_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0  # add channel dim
X_test = X_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0

# Build CNN
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train with callbacks
history = model.fit(
    X_train, y_train,
    epochs=10,
    batch_size=64,
    validation_split=0.1,
    callbacks=[
        callbacks.EarlyStopping(patience=3, restore_best_weights=True),
        callbacks.ReduceLROnPlateau(factor=0.5, patience=2)
    ]
)

# Evaluate
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"Test accuracy: {test_acc:.4f}")
```

### Exercise 2: Text Classification with LSTM

```python
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load IMDB reviews (top 10000 words)
vocab_size = 10000
max_length = 200

(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=vocab_size)
X_train = pad_sequences(X_train, maxlen=max_length, padding='post')  # pad to fixed length
X_test = pad_sequences(X_test, maxlen=max_length, padding='post')

print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")

# Build LSTM model
model = models.Sequential([
    layers.Embedding(vocab_size, 64, input_length=max_length),  # learn word embeddings
    layers.Bidirectional(layers.LSTM(32)),                        # process both directions
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')                        # binary sentiment
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

# Train
# history = model.fit(
#     X_train, y_train,
#     epochs=5,
#     batch_size=128,
#     validation_split=0.2,
#     callbacks=[tf.keras.callbacks.EarlyStopping(patience=2, restore_best_weights=True)]
# )
```

### Exercise 3: Transfer Learning on Custom Dataset

```python
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.applications import MobileNetV2

# Simulate loading a custom image dataset
# In practice, use tf.keras.utils.image_dataset_from_directory
num_classes = 5
img_size = (224, 224)

# train_ds = tf.keras.utils.image_dataset_from_directory(
#     'data/train',
#     image_size=img_size,
#     batch_size=32,
#     label_mode='categorical'
# )

# Data augmentation layer (applied during training only)
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),         # randomly flip images
    layers.RandomRotation(0.1),              # rotate up to 10%
    layers.RandomZoom(0.1),                  # zoom up to 10%
    layers.RandomContrast(0.1),              # adjust contrast
])

# Build model with augmentation and transfer learning
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(*img_size, 3))
base_model.trainable = False

model = models.Sequential([
    data_augmentation,                              # augment training images
    layers.Rescaling(1./127.5, offset=-1),          # scale to [-1, 1] for MobileNetV2
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# Training would look like:
# model.fit(train_ds, epochs=10, validation_data=val_ds,
#     callbacks=[
#         callbacks.ModelCheckpoint('best_transfer.keras', save_best_only=True),
#         callbacks.EarlyStopping(patience=5, restore_best_weights=True)
#     ]
# )
```

### Exercise 4: tf.data Pipeline

```python
import tensorflow as tf
import numpy as np

# Build a complete tf.data pipeline with preprocessing
def create_dataset(X, y, batch_size=32, shuffle=True, augment=False):
    dataset = tf.data.Dataset.from_tensor_slices((X, y))

    if shuffle:
        dataset = dataset.shuffle(buffer_size=len(X))  # full shuffle

    dataset = dataset.batch(batch_size)

    if augment:
        # Apply data augmentation to each batch
        augment_layer = tf.keras.Sequential([
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.1),
        ])
        dataset = dataset.map(
            lambda x, y: (augment_layer(x, training=True), y),
            num_parallel_calls=tf.data.AUTOTUNE
        )

    dataset = dataset.prefetch(tf.data.AUTOTUNE)       # overlap IO and compute
    return dataset

# Example usage with CIFAR-10
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.cifar10.load_data()
X_train = X_train.astype('float32') / 255.0
X_test = X_test.astype('float32') / 255.0

train_ds = create_dataset(X_train, y_train, batch_size=64, shuffle=True, augment=True)
test_ds = create_dataset(X_test, y_test, batch_size=64, shuffle=False, augment=False)

# Inspect the pipeline
for images, labels in train_ds.take(1):
    print(f"Batch images shape: {images.shape}")  # (64, 32, 32, 3)
    print(f"Batch labels shape: {labels.shape}")   # (64, 1)
```

---

## Summary

These notes cover the fundamental concepts of TensorFlow:

1. **What is TensorFlow**: Google's ML framework with eager execution, GPU support, and Keras integration
2. **Tensors**: Creation, operations, reshaping, dtypes, and GPU placement
3. **Keras API**: Sequential models for linear stacks, Functional API for complex architectures
4. **Building Models**: Dense, Conv2D, LSTM, Dropout, BatchNormalization, and layer composition
5. **Compiling and Training**: Configuring loss, optimizer, and metrics; training with `fit`, evaluating with `evaluate`, inferring with `predict`
6. **tf.data Datasets**: Efficient input pipelines with batching, shuffling, prefetching, and parallel preprocessing
7. **Callbacks**: ModelCheckpoint, EarlyStopping, TensorBoard, LearningRateScheduler, and custom callbacks
8. **Saving and Loading**: SavedModel format, Keras format, HDF5, weights-only, and serving exports
9. **Transfer Learning**: Pretrained models from `tf.keras.applications`, feature extraction, and fine-tuning strategies
10. **TensorBoard**: Logging scalars, histograms, images, and launching the visualization dashboard

### Next Steps

1. Work through the practice exercises end-to-end with real datasets
2. Explore custom training loops with `tf.GradientTape` for full control
3. Learn `tf.function` and graph mode for production performance optimization
4. Study distributed training with `tf.distribute.MirroredStrategy`
5. Experiment with TensorFlow Hub for additional pretrained models
6. Deploy models with TF Serving, TF Lite (mobile), or TensorFlow.js (browser)

### Additional Resources

- **TensorFlow Documentation**: https://www.tensorflow.org/guide
- **Keras API Reference**: https://keras.io/api/
- **TensorFlow Tutorials**: https://www.tensorflow.org/tutorials
- **TensorFlow Hub**: https://tfhub.dev/
- **TensorFlow Model Garden**: https://github.com/tensorflow/models
- **Keras Examples**: https://keras.io/examples/
