# Introduction to torchaudio

## Table of Contents

- [What is torchaudio](#what-is-torchaudio)
- [Installation](#installation)
- [Loading and Saving Audio](#loading-and-saving-audio)
- [Audio Information](#audio-information)
- [Spectrogram Transforms](#spectrogram-transforms)
- [Mel Spectrogram and MFCC](#mel-spectrogram-and-mfcc)
- [Resampling and Volume](#resampling-and-volume)
- [Amplitude Conversions](#amplitude-conversions)
- [Functional API](#functional-api)
- [Data Augmentation](#data-augmentation)
- [Built-in Datasets](#built-in-datasets)
- [Pre-trained Models](#pre-trained-models)
- [Feature Extraction Pipeline](#feature-extraction-pipeline)
- [Integration with PyTorch DataLoader](#integration-with-pytorch-dataloader)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is torchaudio

torchaudio is a PyTorch library for audio processing. It provides I/O functions, signal transformations, and pre-trained models that integrate seamlessly with the PyTorch ecosystem. torchaudio enables GPU-accelerated audio processing and is designed for building end-to-end audio deep learning pipelines.

Key features:
- Load and save audio files with multiple backend support
- GPU-accelerated spectral transforms (Spectrogram, MelSpectrogram, MFCC)
- Functional and class-based transform APIs
- Data augmentation for training robustness
- Built-in datasets for speech and audio tasks
- Pre-trained models (wav2vec 2.0, HuBERT)

---

## Installation

```python
# Install torchaudio along with PyTorch
# pip install torch torchaudio

# For a specific CUDA version
# pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify the installation
import torch
import torchaudio
print(f"PyTorch: {torch.__version__}, torchaudio: {torchaudio.__version__}")
print(f"Backends: {torchaudio.list_audio_backends()}")
print(f"CUDA: {torch.cuda.is_available()}")
```

---

## Loading and Saving Audio

```python
import torch
import torchaudio

# Load an audio file - returns (waveform, sample_rate)
waveform, sample_rate = torchaudio.load('audio.wav')
print(f"Shape: {waveform.shape}")        # (channels, num_samples)
print(f"Duration: {waveform.shape[1] / sample_rate:.2f} seconds")

# Load a specific portion
waveform_section, sr = torchaudio.load(
    'audio.wav', frame_offset=44100, num_frames=88200
)

# Save audio to a file
torchaudio.save('output.wav', waveform, sample_rate)
torchaudio.save('output_16bit.wav', waveform, sample_rate,
                encoding='PCM_S', bits_per_sample=16)
torchaudio.save('output.flac', waveform, sample_rate)

# Convert stereo to mono
if waveform.shape[0] == 2:
    mono = torch.mean(waveform, dim=0, keepdim=True)
    torchaudio.save('mono.wav', mono, sample_rate)

# Move to GPU for processing
if torch.cuda.is_available():
    waveform_gpu = waveform.to('cuda')
```

---

## Audio Information

```python
import torchaudio

# Get metadata without loading data
info = torchaudio.info('audio.wav')
print(f"Sample rate: {info.sample_rate}")
print(f"Num frames: {info.num_frames}")
print(f"Num channels: {info.num_channels}")
print(f"Bits per sample: {info.bits_per_sample}")
print(f"Encoding: {info.encoding}")
print(f"Duration: {info.num_frames / info.sample_rate:.2f} seconds")
```

---

## Spectrogram Transforms

```python
import torch
import torchaudio
import torchaudio.transforms as T

waveform, sample_rate = torchaudio.load('audio.wav')

# Power spectrogram from STFT
spectrogram_transform = T.Spectrogram(
    n_fft=2048, win_length=2048,
    hop_length=512, power=2.0        # 2.0 for power, 1.0 for magnitude
)
spectrogram = spectrogram_transform(waveform)
print(f"Spectrogram shape: {spectrogram.shape}")  # (channels, freq_bins, time_frames)

# Complex spectrogram (preserves phase)
complex_spec_transform = T.Spectrogram(n_fft=2048, hop_length=512, power=None)
complex_spec = complex_spec_transform(waveform)

# Inverse spectrogram (Griffin-Lim reconstruction)
griffin_lim = T.GriffinLim(n_fft=2048, hop_length=512, power=2.0, n_iter=32)
reconstructed = griffin_lim(spectrogram)

# GPU-accelerated computation
if torch.cuda.is_available():
    spec_gpu = spectrogram_transform.to('cuda')
    spec_result = spec_gpu(waveform.to('cuda'))

# Visualize
import matplotlib.pyplot as plt
plt.figure(figsize=(14, 5))
plt.imshow(10 * torch.log10(spectrogram[0] + 1e-10).numpy(),
           aspect='auto', origin='lower', cmap='viridis')
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram')
plt.tight_layout()
plt.show()
```

---

## Mel Spectrogram and MFCC

```python
import torch
import torchaudio
import torchaudio.transforms as T

waveform, sample_rate = torchaudio.load('audio.wav')

# Mel Spectrogram
mel_transform = T.MelSpectrogram(
    sample_rate=sample_rate, n_fft=2048,
    hop_length=512, n_mels=128, f_min=0, f_max=8000
)
mel_spec = mel_transform(waveform)

# Convert to decibels
amp_to_db = T.AmplitudeToDB(stype='power', top_db=80)
mel_spec_db = amp_to_db(mel_spec)

# MFCC
mfcc_transform = T.MFCC(
    sample_rate=sample_rate, n_mfcc=13,
    melkwargs={'n_fft': 2048, 'hop_length': 512, 'n_mels': 128}
)
mfccs = mfcc_transform(waveform)
print(f"MFCC shape: {mfccs.shape}")  # (channels, n_mfcc, time_frames)

# Compute deltas
compute_deltas = T.ComputeDeltas()
delta_mfccs = compute_deltas(mfccs)
delta2_mfccs = compute_deltas(delta_mfccs)
full_features = torch.cat([mfccs, delta_mfccs, delta2_mfccs], dim=1)
print(f"Full features: {full_features.shape}")  # (channels, 39, time_frames)

# Visualize
import matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 1, figsize=(14, 8))
axes[0].imshow(mel_spec_db[0].numpy(), aspect='auto', origin='lower', cmap='magma')
axes[0].set_title('Mel Spectrogram (dB)')
axes[1].imshow(mfccs[0].numpy(), aspect='auto', origin='lower')
axes[1].set_title('MFCCs')
plt.tight_layout()
plt.show()
```

---

## Resampling and Volume

```python
import torchaudio
import torchaudio.transforms as T

waveform, sample_rate = torchaudio.load('audio.wav')

# Resample to a different sample rate
resampler = T.Resample(orig_freq=sample_rate, new_freq=16000)
waveform_16k = resampler(waveform)

# Volume adjustment
vol_quiet = T.Vol(gain=0.5, gain_type='amplitude')(waveform)    # half amplitude
vol_down = T.Vol(gain=-6, gain_type='db')(waveform)             # reduce by 6 dB
vol_up = T.Vol(gain=3, gain_type='db')(waveform)                # increase by 3 dB

# Dithering (reduce quantization artifacts)
dither = T.Dither(density_function='TPDF', noise_shaping=True)
waveform_dithered = dither(waveform)

# Preemphasis / deemphasis filters
preemphasis = T.Preemphasis(coeff=0.97)
deemphasis = T.Deemphasis(coeff=0.97)
waveform_preemph = preemphasis(waveform)
waveform_restored = deemphasis(waveform_preemph)
```

---

## Amplitude Conversions

```python
import torch
import torchaudio
import torchaudio.transforms as T

waveform, sample_rate = torchaudio.load('audio.wav')
power_spec = T.Spectrogram(n_fft=2048, hop_length=512, power=2.0)(waveform)

# Convert to decibels
amp_to_db = T.AmplitudeToDB(stype='power', top_db=80)
spec_db = amp_to_db(power_spec)

# Mel scale conversion
mel_scale = T.MelScale(n_mels=128, sample_rate=sample_rate, n_stft=1025)
mel_from_stft = mel_scale(power_spec)

# Inverse mel scale
inverse_mel = T.InverseMelScale(n_stft=1025, n_mels=128, sample_rate=sample_rate)
reconstructed_stft = inverse_mel(mel_from_stft)
```

---

## Functional API

```python
import torch
import torchaudio
import torchaudio.functional as F

waveform, sample_rate = torchaudio.load('audio.wav')

# Pitch detection
pitch = F.detect_pitch_frequency(
    waveform, sample_rate=sample_rate,
    frame_time=0.01, freq_low=85, freq_high=3400
)

# Filters
highpassed = F.highpass_biquad(waveform, sample_rate, cutoff_freq=300)
lowpassed = F.lowpass_biquad(waveform, sample_rate, cutoff_freq=4000)
bandpassed = F.bandpass_biquad(waveform, sample_rate, central_freq=1000, Q=0.707)

# Gain
gained = F.gain(waveform, gain_db=6.0)

# Mu-law encoding/decoding (audio compression)
encoded = F.mu_law_encoding(waveform, quantization_channels=256)
decoded = F.mu_law_decoding(encoded, quantization_channels=256)

# Cepstral mean and variance normalization
mfccs = torchaudio.transforms.MFCC(sample_rate=sample_rate, n_mfcc=13)(waveform)
normalized = F.sliding_window_cmn(mfccs, cmn_window=600, norm_vars=True)
```

---

## Data Augmentation

```python
import torch
import torchaudio
import torchaudio.transforms as T

waveform, sample_rate = torchaudio.load('audio.wav')
mel_transform = T.MelSpectrogram(sample_rate=sample_rate, n_mels=128)
mel_spec = mel_transform(waveform)

# Time and frequency masking (SpecAugment)
time_mask = T.TimeMasking(time_mask_param=80)
freq_mask = T.FrequencyMasking(freq_mask_param=27)

def spec_augment(spectrogram, num_time_masks=2, num_freq_masks=2):
    """Apply SpecAugment: multiple time and frequency masks."""
    augmented = spectrogram.clone()
    for _ in range(num_time_masks):
        augmented = T.TimeMasking(time_mask_param=80)(augmented)
    for _ in range(num_freq_masks):
        augmented = T.FrequencyMasking(freq_mask_param=27)(augmented)
    return augmented

augmented_spec = spec_augment(mel_spec)

# Speed perturbation
def speed_perturb(waveform, sample_rate, speeds=[0.9, 1.0, 1.1]):
    """Randomly change speed by resampling."""
    import random
    speed = random.choice(speeds)
    if speed == 1.0:
        return waveform
    return T.Resample(sample_rate, int(sample_rate * speed))(waveform)

# Add noise with SNR control
def add_noise_snr(signal, noise, snr_db=10):
    """Mix signal with noise at a specified SNR."""
    signal_power = signal.norm(p=2)
    noise_power = noise.norm(p=2)
    snr = 10 ** (snr_db / 20)
    scale = signal_power / (snr * noise_power + 1e-10)
    if noise.shape[1] < signal.shape[1]:
        noise = noise.repeat(1, signal.shape[1] // noise.shape[1] + 1)
    noise = noise[:, :signal.shape[1]]
    return signal + scale * noise

# Visualize augmentation
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(14, 4))
axes[0].imshow(T.AmplitudeToDB()(mel_spec[0]).numpy(), aspect='auto', origin='lower')
axes[0].set_title('Original')
axes[1].imshow(T.AmplitudeToDB()(augmented_spec[0]).numpy(), aspect='auto', origin='lower')
axes[1].set_title('SpecAugment')
plt.tight_layout()
plt.show()
```

---

## Built-in Datasets

```python
import torchaudio

# Speech Commands dataset (keyword spotting)
speech_commands = torchaudio.datasets.SPEECHCOMMANDS(
    root='./data', download=True, subset='training'
)
waveform, sr, label, speaker_id, utterance_num = speech_commands[0]
print(f"Shape: {waveform.shape}, Label: {label}")

# LibriSpeech dataset (speech recognition)
librispeech = torchaudio.datasets.LIBRISPEECH(
    root='./data', url='dev-clean', download=True
)
waveform, sr, transcript, speaker_id, chapter_id, utt_id = librispeech[0]
print(f"Transcript: {transcript}")

# YESNO dataset (simple binary speech dataset)
yesno = torchaudio.datasets.YESNO(root='./data', download=True)
waveform, sr, labels = yesno[0]
print(f"Labels: {labels}")  # list of 0s and 1s

# Get all labels in Speech Commands
labels = sorted(set(item[2] for item in speech_commands))
print(f"Classes: {len(labels)}, Examples: {labels[:5]}")
```

---

## Pre-trained Models

```python
import torch
import torchaudio
from torchaudio.pipelines import WAV2VEC2_BASE, HUBERT_BASE

# wav2vec 2.0: self-supervised speech representations
bundle = WAV2VEC2_BASE
model = bundle.get_model()
waveform, sr = torchaudio.load('speech.wav')
if sr != bundle.sample_rate:
    waveform = torchaudio.transforms.Resample(sr, bundle.sample_rate)(waveform)

with torch.no_grad():
    features, _ = model.extract_features(waveform)
    print(f"Layers: {len(features)}, Last: {features[-1].shape}")

# HuBERT
hubert_model = HUBERT_BASE.get_model()
with torch.no_grad():
    hubert_features, _ = hubert_model.extract_features(waveform)

# ASR with wav2vec 2.0
from torchaudio.pipelines import WAV2VEC2_ASR_BASE_960H
asr_bundle = WAV2VEC2_ASR_BASE_960H
asr_model = asr_bundle.get_model()
labels = asr_bundle.get_labels()

with torch.no_grad():
    emission, _ = asr_model(waveform)

# Greedy CTC decoding
predicted_ids = torch.argmax(emission[0], dim=-1)
predicted_tokens = [labels[id] for id in predicted_ids]
transcript = ''.join([t for i, t in enumerate(predicted_tokens)
                      if t != '-' and (i == 0 or t != predicted_tokens[i-1])])
print(f"Transcript: {transcript}")
```

---

## Feature Extraction Pipeline

```python
import torch
import torchaudio
import torchaudio.transforms as T

class AudioFeatureExtractor:
    """Configurable audio feature extraction pipeline."""

    def __init__(self, sample_rate=16000, n_mels=128, n_mfcc=13,
                 n_fft=2048, hop_length=512):
        self.sample_rate = sample_rate
        self.mel_transform = T.MelSpectrogram(
            sample_rate=sample_rate, n_fft=n_fft,
            hop_length=hop_length, n_mels=n_mels
        )
        self.mfcc_transform = T.MFCC(
            sample_rate=sample_rate, n_mfcc=n_mfcc,
            melkwargs={'n_fft': n_fft, 'hop_length': hop_length, 'n_mels': n_mels}
        )
        self.amp_to_db = T.AmplitudeToDB()
        self.compute_deltas = T.ComputeDeltas()

    def __call__(self, filepath, feature_type='mel'):
        """Load audio and extract features."""
        waveform, sr = torchaudio.load(filepath)
        if sr != self.sample_rate:
            waveform = T.Resample(sr, self.sample_rate)(waveform)

        if feature_type == 'mel':
            return self.amp_to_db(self.mel_transform(waveform))
        elif feature_type == 'mfcc':
            mfccs = self.mfcc_transform(waveform)
            delta = self.compute_deltas(mfccs)
            delta2 = self.compute_deltas(delta)
            return torch.cat([mfccs, delta, delta2], dim=1)

extractor = AudioFeatureExtractor(sample_rate=16000, n_mels=80)
mel_features = extractor('audio.wav', feature_type='mel')
mfcc_features = extractor('audio.wav', feature_type='mfcc')
print(f"Mel: {mel_features.shape}, MFCC: {mfcc_features.shape}")
```

---

## Integration with PyTorch DataLoader

```python
import torch
import torchaudio
import torchaudio.transforms as T
from torch.utils.data import Dataset, DataLoader

class AudioDataset(Dataset):
    """Custom dataset for audio classification."""

    def __init__(self, file_list, labels, target_sr=16000, max_length=16000,
                 n_mels=128):
        self.file_list = file_list
        self.labels = labels
        self.target_sr = target_sr
        self.max_length = max_length
        self.mel_transform = T.MelSpectrogram(
            sample_rate=target_sr, n_mels=n_mels, n_fft=1024, hop_length=256
        )
        self.amp_to_db = T.AmplitudeToDB()

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        waveform, sr = torchaudio.load(self.file_list[idx])

        # Resample, convert to mono, pad/truncate
        if sr != self.target_sr:
            waveform = T.Resample(sr, self.target_sr)(waveform)
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)
        if waveform.shape[1] > self.max_length:
            waveform = waveform[:, :self.max_length]
        elif waveform.shape[1] < self.max_length:
            waveform = torch.nn.functional.pad(waveform, (0, self.max_length - waveform.shape[1]))

        mel_spec_db = self.amp_to_db(self.mel_transform(waveform))
        return mel_spec_db, self.labels[idx]

# Create dataset and dataloader
dataset = AudioDataset(['a1.wav', 'a2.wav'], [0, 1], target_sr=16000, max_length=32000)
loader = DataLoader(dataset, batch_size=16, shuffle=True, num_workers=4, pin_memory=True)

for features, targets in loader:
    print(f"Batch: features={features.shape}, targets={targets.shape}")
    break
```

---

## Practice Exercises

1. Load an audio file, compute its mel spectrogram with torchaudio transforms, and visualize it with a dB scale using matplotlib.

2. Implement a SpecAugment pipeline that applies two time masks and two frequency masks, then compare original and augmented spectrograms visually.

3. Build a custom PyTorch Dataset that loads audio, resamples to 16 kHz, extracts MFCCs with deltas, and pads/truncates to a fixed length.

4. Use wav2vec 2.0 to extract speech representations and print the feature shapes from each transformer layer.

5. Create a data augmentation pipeline combining speed perturbation, additive noise, and SpecAugment.

6. Compare spectrograms produced by different window sizes (512, 1024, 2048, 4096) to visualize the time-frequency resolution trade-off.

---

## Summary

torchaudio is the audio processing library for the PyTorch ecosystem. It provides efficient I/O operations, GPU-accelerated spectral transforms (Spectrogram, MelSpectrogram, MFCC), a functional API for signal processing, data augmentation techniques (SpecAugment, noise addition, speed perturbation), built-in datasets for speech tasks, and pre-trained models like wav2vec 2.0 and HuBERT. Its tight integration with PyTorch makes it the natural choice for end-to-end audio deep learning pipelines.

---

## Next Steps

- Explore torchaudio's CTC decoder for automatic speech recognition
- Build a complete ASR system using pre-trained models and fine-tuning
- Combine torchaudio with torchvision for multimodal audio-visual models
- Study advanced augmentation strategies for improving model robustness

---

## Additional Resources

- [torchaudio Documentation](https://pytorch.org/audio/stable/)
- [torchaudio GitHub Repository](https://github.com/pytorch/audio)
- [torchaudio Tutorials](https://pytorch.org/audio/stable/tutorials.html)
- [SpecAugment Paper](https://arxiv.org/abs/1904.08779)
