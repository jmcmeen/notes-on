# Introduction to OpenSoundscape

## Table of Contents

- [What is OpenSoundscape](#what-is-opensoundscape)
- [Installation](#installation)
- [Audio Loading and Preprocessing](#audio-loading-and-preprocessing)
- [Spectrogram Generation](#spectrogram-generation)
- [CNN-based Classification](#cnn-based-classification)
- [Audio Annotation](#audio-annotation)
- [Signal Processing](#signal-processing)
- [Species Detection Workflow](#species-detection-workflow)
- [Data Preparation](#data-preparation)
- [Model Evaluation](#model-evaluation)
- [Working with Field Recordings](#working-with-field-recordings)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is OpenSoundscape

OpenSoundscape is a Python library for bioacoustics analysis and ecology research. It provides tools for analyzing, processing, and classifying wildlife sounds from field recordings. The library includes spectrogram generation, CNN-based sound event classification, integration with annotation tools like Raven, and signal processing utilities for detecting animal vocalizations.

Key features:
- Load and preprocess long-duration field recordings
- Generate spectrograms with configurable parameters
- Train and deploy CNN models for species identification
- Import and export annotations in Raven selection table format
- Signal processing tools for pulse rate analysis (RIBBIT)
- Built on PyTorch for GPU-accelerated model training

---

## Installation

```python
# Install OpenSoundscape using pip
# pip install opensoundscape

# For GPU support, install PyTorch with CUDA first
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# pip install opensoundscape

import opensoundscape
print(f"OpenSoundscape version: {opensoundscape.__version__}")
```

---

## Audio Loading and Preprocessing

```python
from opensoundscape import Audio
import numpy as np

# Load an audio file
audio = Audio.from_file('field_recording.wav')
print(f"Duration: {audio.duration:.2f}s, SR: {audio.sample_rate} Hz")

# Load with resampling or partial loading
audio_16k = Audio.from_file('field_recording.wav', sample_rate=16000)
# Load a portion of the file
audio_clip = Audio.from_file('field_recording.wav', offset=10.0, duration=30.0)

# Trim silence
audio_trimmed = audio.trim(threshold_db=-40)

# Apply bandpass filter
audio_filtered = audio.bandpass(low_f=1000, high_f=5000)

# Normalize
audio_normalized = audio.normalize()

# Split long recording into clips
clips = audio.split(clip_duration=5.0, clip_overlap=0.0)
print(f"Number of clips: {len(clips)}")

# Access raw samples as NumPy array
raw = audio.samples
print(f"Shape: {raw.shape}, Range: [{raw.min():.4f}, {raw.max():.4f}]")
```

---

## Spectrogram Generation

```python
from opensoundscape import Audio, Spectrogram
import matplotlib.pyplot as plt
import numpy as np

audio = Audio.from_file('field_recording.wav', sample_rate=22050)

# Create a spectrogram
spec = Spectrogram.from_audio(audio)
print(f"Shape: {spec.spectrogram.shape}")

# Custom parameters
spec_custom = Spectrogram.from_audio(
    audio,
    window_type='hann',
    window_samples=512,
    overlap_samples=256
)

# Display
spec.plot()
plt.title('Spectrogram')
plt.show()

# Bandpass the spectrogram
spec_bp = spec.bandpass(min_f=500, max_f=8000)
spec_bp.plot()
plt.title('Bandpassed Spectrogram (500-8000 Hz)')
plt.show()

# Trim to a time range
spec_trimmed = spec.trim(start_time=2.0, end_time=7.0)

# Convert to image for CNN input
spec_image = spec.to_image(shape=(224, 224))

# Mel spectrogram
from opensoundscape import MelSpectrogram
mel_spec = MelSpectrogram.from_audio(
    audio, n_mels=128, window_samples=2048, overlap_samples=512
)
mel_spec.plot()
plt.title('Mel Spectrogram')
plt.show()
```

---

## CNN-based Classification

```python
from opensoundscape import CNN
import pandas as pd

# Create a CNN model
model = CNN(
    architecture='resnet18',
    classes=['species_a', 'species_b', 'species_c'],
    sample_duration=5.0,
    single_target=False          # multi-label classification
)

# Training data: DataFrame with file paths as index, class columns (0/1)
train_df = pd.DataFrame(
    {'species_a': [1, 0, 1, 0], 'species_b': [0, 1, 0, 1],
     'species_c': [0, 0, 1, 1]},
    index=['clip1.wav', 'clip2.wav', 'clip3.wav', 'clip4.wav']
)

# Train the model
model.train(
    train_df=train_df, validation_df=None,
    epochs=10, batch_size=32, learning_rate=0.001,
    save_path='model_training/', num_workers=4
)

# Load a saved model
model_loaded = CNN.load('model_training/best.model')

# Make predictions
predictions = model_loaded.predict(['test1.wav', 'test2.wav'], batch_size=16)
print(predictions.head())

# Fine-tune a pre-trained model
model.freeze_feature_extractor()          # freeze backbone
model.train(train_df=train_df, epochs=5)  # train classifier head only
model.unfreeze_feature_extractor()        # unfreeze for full fine-tuning
model.train(train_df=train_df, epochs=10)
```

---

## Audio Annotation

```python
import pandas as pd
from opensoundscape.annotations import BoxedAnnotations
import matplotlib.pyplot as plt

# Load annotations from Raven selection tables
annotations = BoxedAnnotations.from_raven_files(
    ['annotations.txt'],
    audio_files=['field_recording.wav']
)
print(f"Annotations: {len(annotations.df)}")

# Create annotations manually
annotation_data = pd.DataFrame({
    'audio_file': ['recording.wav'] * 3,
    'start_time': [1.5, 5.0, 12.3],
    'end_time': [3.0, 7.5, 14.0],
    'low_f': [2000, 1500, 3000],
    'high_f': [5000, 4000, 7000],
    'annotation': ['bird_a', 'bird_b', 'bird_a'],
})
manual_annotations = BoxedAnnotations(annotation_data)

# Convert to one-hot labels for training
one_hot = annotations.one_hot_labels_like(
    clip_duration=5.0,
    clip_overlap=0.0,
    min_label_overlap=0.25       # minimum annotation overlap fraction
)
print(f"One-hot labels: {one_hot.shape}")

# Export back to Raven format
annotations.to_raven_files(save_dir='exported/', audio_files=['field_recording.wav'])

# Visualize annotations on spectrogram
from opensoundscape import Audio, Spectrogram
audio = Audio.from_file('field_recording.wav')
spec = Spectrogram.from_audio(audio)
fig, ax = plt.subplots(figsize=(14, 5))
spec.plot(ax=ax)
for _, row in annotation_data.iterrows():
    rect = plt.Rectangle(
        (row['start_time'], row['low_f']),
        row['end_time'] - row['start_time'],
        row['high_f'] - row['low_f'],
        linewidth=2, edgecolor='red', facecolor='none'
    )
    ax.add_patch(rect)
    ax.text(row['start_time'], row['high_f'], row['annotation'],
            color='red', fontsize=8)
plt.title('Annotations on Spectrogram')
plt.show()
```

---

## Signal Processing

```python
from opensoundscape import Audio, Spectrogram
import numpy as np

audio = Audio.from_file('field_recording.wav', sample_rate=22050)

# Bandpass filter to isolate target frequency range
audio_filtered = audio.bandpass(low_f=2000, high_f=6000)

# RIBBIT: pulse rate detection for calling species (e.g., frogs)
from opensoundscape.ribbit import ribbit

scores, times = ribbit(
    audio,
    pulse_rate_range=[10, 50],       # expected pulses per second
    signal_band=[1000, 3000],        # target signal frequency band (Hz)
    noise_bands=[[0, 500], [5000, 10000]],  # noise estimation bands
    clip_duration=2.0,
    clip_overlap=1.0,
    window_samples=512,
    overlap_samples=256
)

# Find detections above threshold
threshold = 0.5
detections = times[scores > threshold]
print(f"RIBBIT detections: {len(detections)}")

# Compute energy in specific frequency bands
spec = Spectrogram.from_audio(audio_filtered)

def band_energy(spectrogram, frequencies, low_f, high_f):
    """Compute energy in a frequency band over time."""
    mask = (frequencies >= low_f) & (frequencies <= high_f)
    return np.sum(spectrogram.spectrogram[mask, :] ** 2, axis=0)

energy = band_energy(spec, spec.frequencies, 2000, 5000)
print(f"Band energy shape: {energy.shape}")

# Simple spectral subtraction for noise reduction
noise_clip = Audio.from_file('field_recording.wav', offset=0.0, duration=2.0)
noise_spec = Spectrogram.from_audio(noise_clip)
noise_profile = np.mean(noise_spec.spectrogram, axis=1, keepdims=True)
signal_spec = Spectrogram.from_audio(audio)
cleaned = np.maximum(signal_spec.spectrogram - noise_profile, 0)
```

---

## Species Detection Workflow

```python
from opensoundscape import Audio, CNN
from opensoundscape.annotations import BoxedAnnotations
import pandas as pd
import glob

# Step 1: Load annotations
raven_files = glob.glob('annotations/*.txt')
audio_files = [f.replace('annotations/', 'recordings/').replace('.txt', '.wav')
               for f in raven_files]
annotations = BoxedAnnotations.from_raven_files(raven_files, audio_files=audio_files)

# Step 2: Generate labeled training clips
target_species = ['species_a', 'species_b', 'unknown']
labels = annotations.one_hot_labels_like(
    clip_duration=5.0, clip_overlap=2.5, min_label_overlap=0.5,
    class_subset=target_species
)

# Step 3: Train/validation split
from sklearn.model_selection import train_test_split
train_idx, val_idx = train_test_split(range(len(labels)), test_size=0.2, random_state=42)
train_df = labels.iloc[train_idx]
val_df = labels.iloc[val_idx]

# Step 4: Train CNN
model = CNN(architecture='resnet18', classes=target_species, sample_duration=5.0)
model.train(train_df=train_df, validation_df=val_df, epochs=20,
            batch_size=32, save_path='species_model/')

# Step 5: Predict on new recordings
new_files = glob.glob('new_recordings/*.wav')
predictions = model.predict(new_files, batch_size=16, activation_layer='sigmoid')

# Step 6: Apply threshold and report
threshold = 0.5
detections = predictions > threshold
for species in target_species:
    print(f"  {species}: {detections[species].sum()} detections")
```

---

## Data Preparation

```python
from opensoundscape import Audio
import pandas as pd
import numpy as np
import glob
import os

# Split long recordings into fixed-length clips
def split_recordings(audio_dir, output_dir, clip_duration=5.0):
    """Split all recordings into fixed-length clips."""
    os.makedirs(output_dir, exist_ok=True)
    clip_info = []
    for filepath in glob.glob(f'{audio_dir}/*.wav'):
        audio = Audio.from_file(filepath)
        base = os.path.splitext(os.path.basename(filepath))[0]
        for i, start in enumerate(np.arange(0, audio.duration - clip_duration + 0.01,
                                             clip_duration)):
            clip = Audio.from_file(filepath, offset=start, duration=clip_duration)
            clip_path = os.path.join(output_dir, f"{base}_clip{i:04d}.wav")
            clip.save(clip_path)
            clip_info.append({'clip_path': clip_path, 'source': filepath,
                              'start': start})
    return pd.DataFrame(clip_info)

# Validate audio files for issues (corrupted, too short)
def validate_audio_files(file_list, min_duration=1.0):
    valid, invalid = [], []
    for fp in file_list:
        try:
            audio = Audio.from_file(fp)
            (valid if audio.duration >= min_duration else invalid).append(fp)
        except Exception:
            invalid.append(fp)
    return valid, invalid
```

---

## Model Evaluation

```python
from opensoundscape import CNN
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, precision_recall_curve, f1_score
import matplotlib.pyplot as plt

model = CNN.load('species_model/best.model')
val_df = pd.read_csv('validation_labels.csv', index_col=0)
predictions = model.predict(val_df.index.tolist(), batch_size=16)

# Per-class metrics
threshold = 0.5
pred_labels = (predictions > threshold).astype(int)
for species in val_df.columns:
    print(f"\n{species}:")
    print(classification_report(val_df[species], pred_labels[species],
                                 target_names=['absent', 'present']))

# Threshold optimization: find best threshold per class by F1
for species in val_df.columns:
    best_f1, best_t = 0, 0.5
    for t in np.arange(0.1, 0.95, 0.05):
        f1 = f1_score(val_df[species], (predictions[species] > t).astype(int),
                      zero_division=0)
        if f1 > best_f1:
            best_f1, best_t = f1, t
    print(f"{species}: threshold={best_t:.2f}, F1={best_f1:.3f}")

# Precision-recall curves
fig, ax = plt.subplots(figsize=(8, 6))
for species in val_df.columns:
    prec, rec, _ = precision_recall_curve(val_df[species], predictions[species])
    ax.plot(rec, prec, label=species)
ax.set_xlabel('Recall')
ax.set_ylabel('Precision')
ax.legend()
plt.title('Precision-Recall Curves')
plt.tight_layout()
plt.show()
```

---

## Working with Field Recordings

```python
from opensoundscape import Audio, CNN
import pandas as pd
import numpy as np
import glob
import os

# Process a batch of field recordings
def process_recordings(audio_dir, model_path, output_dir):
    """Run species detection on all recordings."""
    os.makedirs(output_dir, exist_ok=True)
    model = CNN.load(model_path)
    audio_files = glob.glob(f'{audio_dir}/**/*.wav', recursive=True)

    all_detections = []
    for fp in audio_files:
        preds = model.predict([fp])
        for _, row in preds.iterrows():
            for sp in preds.columns:
                if row[sp] > 0.5:
                    all_detections.append({'file': os.path.basename(fp),
                                           'species': sp, 'confidence': row[sp]})

    pd.DataFrame(all_detections).to_csv(
        os.path.join(output_dir, 'detections.csv'), index=False)

# Quality check for recordings
def check_quality(filepath):
    """Assess recording quality metrics."""
    audio = Audio.from_file(filepath)
    samples = audio.samples
    peak = np.max(np.abs(samples))
    rms = np.sqrt(np.mean(samples ** 2))
    return {
        'duration': audio.duration, 'peak': peak, 'rms': rms,
        'dynamic_range_db': 20 * np.log10(peak / (rms + 1e-10)),
        'is_clipped': np.mean(np.abs(samples) > 0.99) > 0.001,
    }
```

---

## Practice Exercises

1. Load a field recording, bandpass filter to 2-8 kHz, generate a spectrogram, and save it as an image.

2. Create a training dataset from Raven annotations by splitting recordings into 5-second clips.

3. Train a ResNet18 CNN on labeled clips and evaluate with precision, recall, and F1 score.

4. Build a detection pipeline that processes a directory of recordings and exports results as CSV.

5. Use RIBBIT to detect frog calls and compare results across different time windows.

---

## Summary

OpenSoundscape is a specialized Python library for bioacoustics and ecological sound analysis. It provides end-to-end workflows for loading and preprocessing field recordings, generating spectrograms, training CNN classifiers for species identification, importing and exporting Raven annotations, signal processing with bandpass filters and RIBBIT pulse rate detection, and evaluating model performance. Built on PyTorch, it enables GPU-accelerated training and is designed for researchers working with wildlife sound data.

---

## Next Steps

- Explore transfer learning with pre-trained bioacoustics models
- Combine OpenSoundscape with BirdNET for broader species coverage
- Build automated monitoring pipelines for long-term ecological studies

---

## Additional Resources

- [OpenSoundscape Documentation](https://opensoundscape.org/)
- [OpenSoundscape GitHub Repository](https://github.com/kitzeslab/opensoundscape)
- [Raven Pro (Cornell Lab)](https://ravensoundsoftware.com/)
- [Bioacoustics Research Program](https://www.birds.cornell.edu/brp/)
