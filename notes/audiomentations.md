# Introduction to audiomentations

## Table of Contents

- [What is audiomentations](#what-is-audiomentations)
- [Installation](#installation)
- [Core Concepts](#core-concepts)
- [Noise Augmentations](#noise-augmentations)
- [Time-Domain Augmentations](#time-domain-augmentations)
- [Pitch and Speed Augmentations](#pitch-and-speed-augmentations)
- [Gain and Volume Augmentations](#gain-and-volume-augmentations)
- [Clipping and Distortion](#clipping-and-distortion)
- [Spectrogram Augmentations](#spectrogram-augmentations)
- [Composing Augmentations](#composing-augmentations)
- [Integration with PyTorch Dataset](#integration-with-pytorch-dataset)
- [Custom Augmentation](#custom-augmentation)
- [Reproducibility](#reproducibility)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is audiomentations

audiomentations is a Python library for audio data augmentation. Inspired by the image augmentation library albumentations, it provides a wide collection of audio transforms that can be composed into augmentation pipelines. Each transform has a probability parameter controlling how often it is applied, making it easy to build stochastic augmentation strategies for training robust audio models.

Key features:
- Large collection of time-domain audio augmentations
- Composable pipeline with probability control per transform
- NumPy-based for compatibility with any framework
- OneOf and SomeOf selectors for varied augmentation
- Reproducible augmentation with random seed control

---

## Installation

```python
# Install audiomentations using pip
# pip install audiomentations

# Install with extra dependencies for all augmentations
# pip install audiomentations[extras]

# For spectrogram augmentations with PyTorch
# pip install torch-audiomentations

import audiomentations
print(f"audiomentations version: {audiomentations.__version__}")
```

---

## Core Concepts

```python
import numpy as np
from audiomentations import Compose, AddGaussianNoise, TimeStretch, PitchShift

# audiomentations works with 1D float32 NumPy arrays in [-1.0, 1.0]

# Create an augmentation pipeline
augment = Compose([
    AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=0.5),
    TimeStretch(min_rate=0.8, max_rate=1.25, p=0.5),
    PitchShift(min_semitones=-4, max_semitones=4, p=0.5),
])

# p parameter controls probability: 0.5 = applied 50% of the time

# Load audio (using soundfile)
import soundfile as sf
samples, sample_rate = sf.read('audio.wav', dtype='float32')

# Apply augmentation
augmented = augment(samples=samples, sample_rate=sample_rate)
print(f"Input: {samples.shape}, Output: {augmented.shape}")

# Each call produces different results due to randomness
aug1 = augment(samples=samples, sample_rate=sample_rate)
aug2 = augment(samples=samples, sample_rate=sample_rate)
print(f"Same result: {np.array_equal(aug1, aug2)}")  # False

# Transforms work individually too
noise = AddGaussianNoise(min_amplitude=0.01, max_amplitude=0.05, p=1.0)
noisy = noise(samples=samples, sample_rate=sample_rate)
```

---

## Noise Augmentations

```python
import soundfile as sf
from audiomentations import (
    AddGaussianNoise, AddGaussianSNR,
    AddBackgroundNoise, AddShortNoises,
)

samples, sample_rate = sf.read('audio.wav', dtype='float32')

# Add Gaussian noise with amplitude range
gaussian = AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=1.0)
noisy = gaussian(samples=samples, sample_rate=sample_rate)

# Add Gaussian noise with SNR control
gaussian_snr = AddGaussianSNR(min_snr_db=5.0, max_snr_db=20.0, p=1.0)
noisy_snr = gaussian_snr(samples=samples, sample_rate=sample_rate)

# Add background noise from a directory of noise files
bg_noise = AddBackgroundNoise(
    sounds_path='noise_files/',      # directory of noise audio files
    min_snr_db=3.0, max_snr_db=30.0, p=0.5
)
with_bg = bg_noise(samples=samples, sample_rate=sample_rate)

# Add short noise bursts (clicks, pops, etc.)
short_noises = AddShortNoises(
    sounds_path='short_noise_files/',
    min_snr_db=0.0, max_snr_db=20.0,
    min_time_between_sounds=2.0,
    max_time_between_sounds=8.0, p=0.5
)
with_bursts = short_noises(samples=samples, sample_rate=sample_rate)
```

---

## Time-Domain Augmentations

```python
import soundfile as sf
from audiomentations import Shift, Trim, Padding, Reverse, Resample

samples, sample_rate = sf.read('audio.wav', dtype='float32')

# Shift: circular shift forward or backward in time
shift = Shift(
    min_shift=-0.5, max_shift=0.5,   # fraction of total length
    shift_unit='fraction',            # or 'seconds'
    rollover=True, p=1.0              # wrap around
)
shifted = shift(samples=samples, sample_rate=sample_rate)

# Trim: remove silence from beginning and end
trim = Trim(top_db=30.0, p=1.0)
trimmed = trim(samples=samples, sample_rate=sample_rate)

# Padding: add zero-padding
padding = Padding(
    mode='silence', min_fraction=0.01,
    max_fraction=0.5, pad_section='end', p=1.0
)
padded = padding(samples=samples, sample_rate=sample_rate)

# Reverse: flip the audio
reverse = Reverse(p=0.5)
reversed_audio = reverse(samples=samples, sample_rate=sample_rate)

# Resample: change sample rate and back (degrades quality)
resample = Resample(min_sample_rate=8000, max_sample_rate=44100, p=0.5)
resampled = resample(samples=samples, sample_rate=sample_rate)
```

---

## Pitch and Speed Augmentations

```python
import soundfile as sf
from audiomentations import PitchShift, TimeStretch

samples, sample_rate = sf.read('audio.wav', dtype='float32')

# PitchShift: change pitch without changing duration
pitch_shift = PitchShift(min_semitones=-4, max_semitones=4, p=1.0)
pitched = pitch_shift(samples=samples, sample_rate=sample_rate)

# TimeStretch: change speed without changing pitch
time_stretch = TimeStretch(
    min_rate=0.8, max_rate=1.25,
    leave_length_unchanged=False, p=1.0  # allow output length to change
)
stretched = time_stretch(samples=samples, sample_rate=sample_rate)

# Fixed output length version
time_stretch_fixed = TimeStretch(
    min_rate=0.8, max_rate=1.25,
    leave_length_unchanged=True, p=1.0   # pad/truncate to original length
)
stretched_fixed = time_stretch_fixed(samples=samples, sample_rate=sample_rate)
```

---

## Gain and Volume Augmentations

```python
import soundfile as sf
from audiomentations import Gain, Normalize, Mp3Compression, LoudnessNormalization

samples, sample_rate = sf.read('audio.wav', dtype='float32')

# Gain: random volume change
gain = Gain(min_gain_db=-12, max_gain_db=12, p=1.0)
gained = gain(samples=samples, sample_rate=sample_rate)

# Normalize: peak normalize to [-1, 1]
normalize = Normalize(p=1.0)
normalized = normalize(samples=samples, sample_rate=sample_rate)

# LoudnessNormalization: normalize to target LUFS
loudness = LoudnessNormalization(min_lufs=-31, max_lufs=-13, p=1.0)
lufs_norm = loudness(samples=samples, sample_rate=sample_rate)

# Mp3Compression: simulate lossy compression artifacts
mp3 = Mp3Compression(min_bitrate=64, max_bitrate=192, p=0.5)
compressed = mp3(samples=samples, sample_rate=sample_rate)
```

---

## Clipping and Distortion

```python
import soundfile as sf
from audiomentations import (
    ClippingDistortion, Clip,
    BandPassFilter, HighPassFilter, LowPassFilter
)

samples, sample_rate = sf.read('audio.wav', dtype='float32')

# ClippingDistortion: simulate signal clipping
clipping = ClippingDistortion(
    min_percentile_threshold=0, max_percentile_threshold=40, p=1.0
)
clipped = clipping(samples=samples, sample_rate=sample_rate)

# Hard clip to a range
clip = Clip(a_min=-0.5, a_max=0.5, p=1.0)
hard_clipped = clip(samples=samples, sample_rate=sample_rate)

# Filters
bandpass = BandPassFilter(
    min_center_freq=200, max_center_freq=4000, p=1.0
)
highpass = HighPassFilter(min_cutoff_freq=200, max_cutoff_freq=4000, p=1.0)
lowpass = LowPassFilter(min_cutoff_freq=150, max_cutoff_freq=7500, p=1.0)

# Telephone effect: bandpass + optional distortion
from audiomentations import Compose
telephone = Compose([
    HighPassFilter(min_cutoff_freq=300, max_cutoff_freq=400, p=1.0),
    LowPassFilter(min_cutoff_freq=3000, max_cutoff_freq=3400, p=1.0),
    ClippingDistortion(min_percentile_threshold=0, max_percentile_threshold=10, p=0.3),
])
telephone_audio = telephone(samples=samples, sample_rate=sample_rate)
```

---

## Spectrogram Augmentations

```python
# Spectrogram-level augmentations use torch-audiomentations
# pip install torch-audiomentations
import torch
import soundfile as sf
from torch_audiomentations import Compose as TorchCompose
from torch_audiomentations import Gain as TorchGain, PolarityInversion

# torch-audiomentations works with PyTorch tensors: (batch, channels, samples)
torch_augment = TorchCompose([
    TorchGain(min_gain_in_db=-15.0, max_gain_in_db=5.0, p=0.5),
    PolarityInversion(p=0.5),
])
samples, sample_rate = sf.read('audio.wav', dtype='float32')
waveform = torch.from_numpy(samples).unsqueeze(0).unsqueeze(0)
augmented = torch_augment(waveform, sample_rate=sample_rate)

# For SpecAugment-style masking, use torchaudio directly
import torchaudio.transforms as T
mel_spec = T.MelSpectrogram(sample_rate=sample_rate, n_mels=128)(
    torch.from_numpy(samples).unsqueeze(0))
masked = T.TimeMasking(40)(T.FrequencyMasking(20)(mel_spec))
```

---

## Composing Augmentations

```python
import soundfile as sf
from audiomentations import (
    Compose, OneOf, SomeOf,
    AddGaussianNoise, TimeStretch, PitchShift,
    Shift, Gain, Normalize, HighPassFilter, LowPassFilter,
    Mp3Compression
)

samples, sample_rate = sf.read('audio.wav', dtype='float32')

# Compose: sequential application, each with its own probability
pipeline = Compose([
    AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=0.5),
    TimeStretch(min_rate=0.8, max_rate=1.25, p=0.5),
    PitchShift(min_semitones=-4, max_semitones=4, p=0.5),
    Normalize(p=1.0),
])

# OneOf: randomly select exactly one transform
one_of = OneOf([
    AddGaussianNoise(min_amplitude=0.01, max_amplitude=0.05, p=1.0),
    TimeStretch(min_rate=0.8, max_rate=1.25, p=1.0),
    PitchShift(min_semitones=-4, max_semitones=4, p=1.0),
], p=0.8)

# SomeOf: randomly select a subset of (1 to 3) transforms
some_of = SomeOf((1, 3), [
    AddGaussianNoise(min_amplitude=0.005, max_amplitude=0.02, p=1.0),
    TimeStretch(min_rate=0.9, max_rate=1.1, p=1.0),
    PitchShift(min_semitones=-2, max_semitones=2, p=1.0),
    Gain(min_gain_db=-6, max_gain_db=6, p=1.0),
], p=0.9)

# Complex pipeline combining Compose, OneOf, and SomeOf
full_pipeline = Compose([
    Normalize(p=1.0),
    OneOf([
        AddGaussianNoise(min_amplitude=0.005, max_amplitude=0.02),
        Mp3Compression(min_bitrate=64, max_bitrate=128),
    ], p=0.5),
    SomeOf((1, 2), [
        TimeStretch(min_rate=0.85, max_rate=1.15),
        PitchShift(min_semitones=-3, max_semitones=3),
    ], p=0.7),
    Gain(min_gain_db=-3, max_gain_db=3, p=0.5),
])
augmented = full_pipeline(samples=samples, sample_rate=sample_rate)
```

---

## Integration with PyTorch Dataset

```python
import torch
import numpy as np
import soundfile as sf
from torch.utils.data import Dataset, DataLoader
from audiomentations import Compose, AddGaussianNoise, TimeStretch, PitchShift, Normalize

class AugmentedAudioDataset(Dataset):
    """PyTorch Dataset with audiomentations augmentation."""

    def __init__(self, file_list, labels, sample_rate=16000, max_samples=16000,
                 augment=True):
        self.file_list = file_list
        self.labels = labels
        self.sample_rate = sample_rate
        self.max_samples = max_samples
        # Use full augmentation for training, normalize-only for validation
        self.augment = Compose([
            AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=0.5),
            TimeStretch(min_rate=0.8, max_rate=1.25, p=0.4),
            PitchShift(min_semitones=-4, max_semitones=4, p=0.4),
            Normalize(p=1.0),
        ]) if augment else Normalize(p=1.0)

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        samples, sr = sf.read(self.file_list[idx], dtype='float32')
        if samples.ndim > 1:
            samples = np.mean(samples, axis=1)       # stereo to mono
        samples = self.augment(samples=samples, sample_rate=self.sample_rate)
        # Pad or truncate to fixed length
        if len(samples) > self.max_samples:
            start = np.random.randint(0, len(samples) - self.max_samples)
            samples = samples[start:start + self.max_samples]
        elif len(samples) < self.max_samples:
            samples = np.pad(samples, (0, self.max_samples - len(samples)))
        return torch.from_numpy(samples).float().unsqueeze(0), self.labels[idx]

# Usage: augmentation in __getitem__ means each epoch sees different variations
train_loader = DataLoader(
    AugmentedAudioDataset(['a1.wav', 'a2.wav'], [0, 1], augment=True),
    batch_size=32, shuffle=True, num_workers=4
)
```

---

## Custom Augmentation

```python
import numpy as np
from audiomentations import BaseWaveformTransform

class CustomVolumeRamp(BaseWaveformTransform):
    """Custom augmentation: apply a linear volume ramp."""
    supports_multichannel = True

    def __init__(self, min_start_gain=0.0, max_start_gain=1.0,
                 min_end_gain=0.0, max_end_gain=1.0, p=0.5):
        super().__init__(p)
        self.min_start_gain = min_start_gain
        self.max_start_gain = max_start_gain
        self.min_end_gain = min_end_gain
        self.max_end_gain = max_end_gain

    def randomize_parameters(self, samples, sample_rate):
        super().randomize_parameters(samples, sample_rate)
        if self.parameters["should_apply"]:
            self.parameters["start_gain"] = np.random.uniform(
                self.min_start_gain, self.max_start_gain)
            self.parameters["end_gain"] = np.random.uniform(
                self.min_end_gain, self.max_end_gain)

    def apply(self, samples, sample_rate):
        ramp = np.linspace(self.parameters["start_gain"],
                           self.parameters["end_gain"], num=len(samples))
        return samples * ramp

# Custom transforms work in pipelines like built-in ones
from audiomentations import Compose, Normalize
pipeline = Compose([CustomVolumeRamp(p=0.3), Normalize(p=1.0)])
```

---

## Reproducibility

```python
import numpy as np
import soundfile as sf
from audiomentations import Compose, AddGaussianNoise, PitchShift, TimeStretch

samples, sample_rate = sf.read('audio.wav', dtype='float32')
augment = Compose([
    AddGaussianNoise(min_amplitude=0.005, max_amplitude=0.02, p=0.8),
    PitchShift(min_semitones=-3, max_semitones=3, p=0.6),
])

# NumPy seed for reproducibility
np.random.seed(42)
result_1 = augment(samples=samples, sample_rate=sample_rate)
np.random.seed(42)
result_2 = augment(samples=samples, sample_rate=sample_rate)
print(f"Identical: {np.array_equal(result_1, result_2)}")  # True

# freeze_parameters: apply same augmentation to related samples
augment.randomize_parameters(samples=samples, sample_rate=sample_rate)
augment.freeze_parameters()          # lock current random parameters
aug1 = augment(samples=samples[:len(samples)//2], sample_rate=sample_rate)
aug2 = augment(samples=samples[len(samples)//2:], sample_rate=sample_rate)
# Both segments get identical augmentation parameters
augment.unfreeze_parameters()        # unlock for new random parameters
```

---

## Practice Exercises

1. Create an augmentation pipeline with AddGaussianNoise, TimeStretch, and PitchShift. Apply it to an audio file 10 times and save each version.

2. Build a OneOf selector choosing between Gaussian noise, background noise, and MP3 compression artifacts.

3. Implement a custom transform that adds echo by mixing a delayed copy at lower volume.

4. Create a PyTorch Dataset with separate pipelines for training (aggressive augmentation) and validation (normalize only).

5. Design a pipeline simulating telephone quality, noisy room, and distant microphone conditions.

---

## Summary

audiomentations is a specialized Python library for audio data augmentation following the albumentations design pattern. It provides time-domain augmentations (noise, time stretch, pitch shift, shifting, trimming, filtering, clipping), composable pipelines with probability control (Compose, OneOf, SomeOf), PyTorch dataset integration, custom augmentation support through BaseWaveformTransform, and reproducibility via seed control and parameter freezing. It is an essential tool for building robust audio machine learning models.

---

## Next Steps

- Explore the full catalog of audiomentations transforms
- Investigate torch-audiomentations for GPU-accelerated augmentation
- Combine audiomentations with torchaudio for end-to-end pipelines

---

## Additional Resources

- [audiomentations GitHub Repository](https://github.com/iver56/audiomentations)
- [audiomentations Documentation](https://iver56.github.io/audiomentations/)
- [torch-audiomentations GitHub](https://github.com/asteroid-team/torch-audiomentations)
- [SpecAugment Paper](https://arxiv.org/abs/1904.08779)
