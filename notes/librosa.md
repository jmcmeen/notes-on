# Introduction to librosa

## Table of Contents

- [What is librosa](#what-is-librosa)
- [Installation](#installation)
- [Loading Audio](#loading-audio)
- [Waveform Visualization](#waveform-visualization)
- [Short-Time Fourier Transform](#short-time-fourier-transform)
- [Spectrogram Display](#spectrogram-display)
- [Mel Spectrogram](#mel-spectrogram)
- [Mel-Frequency Cepstral Coefficients](#mel-frequency-cepstral-coefficients)
- [Chroma Features](#chroma-features)
- [Spectral Centroid Bandwidth and Rolloff](#spectral-centroid-bandwidth-and-rolloff)
- [Time-Domain Features](#time-domain-features)
- [Display Utilities](#display-utilities)
- [Beat Tracking and Tempo](#beat-tracking-and-tempo)
- [Onset Detection](#onset-detection)
- [Pitch Tracking](#pitch-tracking)
- [Audio Effects](#audio-effects)
- [Feature Extraction Pipeline](#feature-extraction-pipeline)
- [Saving and Exporting](#saving-and-exporting)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is librosa

librosa is a Python library for analyzing and processing audio and music signals. It provides the building blocks for creating music information retrieval (MIR) systems, including functions for feature extraction, spectral analysis, beat tracking, and audio manipulation.

Key features:
- Load and decode audio files into NumPy arrays
- Compute spectral and time-domain features
- Visualize audio data with built-in display functions
- Track beats, onsets, and tempo
- Apply audio transformations like time stretching and pitch shifting

---

## Installation

```python
# Install librosa using pip
# pip install librosa

# Optional: install ffmpeg for broader format support
# sudo apt install ffmpeg   (Linux)
# brew install ffmpeg        (macOS)

# Verify the installation
import librosa
print(librosa.__version__)  # prints the installed version
```

---

## Loading Audio

```python
import librosa
import numpy as np

# Load an audio file - returns (audio_time_series, sample_rate)
y, sr = librosa.load('audio.wav')
print(f"Signal shape: {y.shape}")    # (num_samples,) for mono
print(f"Sample rate: {sr}")           # default is 22050 Hz

# Load with the native sample rate (no resampling)
y, sr = librosa.load('audio.wav', sr=None)

# Load with a specific sample rate
y, sr = librosa.load('audio.wav', sr=16000)  # resample to 16 kHz

# Load only a portion of the file
y, sr = librosa.load('audio.wav', offset=5.0, duration=10.0)

# Load stereo audio (default converts to mono)
y_stereo, sr = librosa.load('stereo.wav', mono=False)
print(f"Stereo shape: {y_stereo.shape}")  # (2, num_samples)

# Get duration of a loaded signal or directly from file
duration = librosa.get_duration(y=y, sr=sr)
duration = librosa.get_duration(path='audio.wav')
```

---

## Waveform Visualization

```python
import librosa
import librosa.display
import matplotlib.pyplot as plt

y, sr = librosa.load('audio.wav', sr=22050)

# Plot using librosa's built-in waveshow function
plt.figure(figsize=(14, 4))
librosa.display.waveshow(y, sr=sr, alpha=0.7)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Waveform')
plt.tight_layout()
plt.show()

# Plot stereo waveform with separate channels
y_stereo, sr = librosa.load('stereo.wav', mono=False, sr=22050)
fig, axes = plt.subplots(2, 1, figsize=(14, 6), sharex=True)
librosa.display.waveshow(y_stereo[0], sr=sr, ax=axes[0])  # left channel
axes[0].set_title('Left Channel')
librosa.display.waveshow(y_stereo[1], sr=sr, ax=axes[1])  # right channel
axes[1].set_title('Right Channel')
plt.tight_layout()
plt.show()
```

---

## Short-Time Fourier Transform

```python
import librosa
import numpy as np

y, sr = librosa.load('audio.wav', sr=22050)

# Compute the STFT - returns complex-valued matrix (1 + n_fft/2, num_frames)
D = librosa.stft(
    y,
    n_fft=2048,         # FFT window size
    hop_length=512,      # samples between frames
    window='hann'        # window function
)

# Separate magnitude and phase
magnitude = np.abs(D)
phase = np.angle(D)

# Convert magnitude to decibels
D_db = librosa.amplitude_to_db(magnitude, ref=np.max)

# Power spectrogram (magnitude squared)
S_power = np.abs(D) ** 2
S_power_db = librosa.power_to_db(S_power, ref=np.max)

# Inverse STFT to reconstruct the signal
y_reconstructed = librosa.istft(D, hop_length=512)

# Different resolutions: larger n_fft = better freq resolution, worse time resolution
D_high_freq = librosa.stft(y, n_fft=4096, hop_length=1024)
D_high_time = librosa.stft(y, n_fft=512, hop_length=128)
```

---

## Spectrogram Display

```python
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

y, sr = librosa.load('audio.wav', sr=22050)
D = librosa.stft(y, n_fft=2048, hop_length=512)

# Display spectrogram with linear frequency axis
plt.figure(figsize=(14, 5))
librosa.display.specshow(
    librosa.amplitude_to_db(np.abs(D), ref=np.max),
    sr=sr, hop_length=512,
    x_axis='time', y_axis='hz'       # label axes with time and Hz
)
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram (dB)')
plt.tight_layout()
plt.show()

# Log-frequency spectrogram (better for music)
plt.figure(figsize=(14, 5))
librosa.display.specshow(
    librosa.amplitude_to_db(np.abs(D), ref=np.max),
    sr=sr, hop_length=512,
    x_axis='time', y_axis='log'      # log-scaled frequency axis
)
plt.colorbar(format='%+2.0f dB')
plt.title('Log-Frequency Spectrogram')
plt.tight_layout()
plt.show()
```

---

## Mel Spectrogram

```python
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

y, sr = librosa.load('audio.wav', sr=22050)

# Compute the mel spectrogram
S_mel = librosa.feature.melspectrogram(
    y=y, sr=sr,
    n_fft=2048, hop_length=512,
    n_mels=128,            # number of mel bands
    fmin=0, fmax=8000      # frequency range
)
S_mel_db = librosa.power_to_db(S_mel, ref=np.max)

# Display the mel spectrogram
plt.figure(figsize=(14, 5))
librosa.display.specshow(
    S_mel_db, sr=sr, hop_length=512,
    x_axis='time', y_axis='mel', fmax=8000
)
plt.colorbar(format='%+2.0f dB')
plt.title('Mel Spectrogram')
plt.tight_layout()
plt.show()

# Different mel band counts for different tasks
S_mel_40 = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=40)    # speech tasks
S_mel_128 = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)  # music tasks
```

---

## Mel-Frequency Cepstral Coefficients

```python
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

y, sr = librosa.load('audio.wav', sr=22050)

# Compute MFCCs from the audio signal
mfccs = librosa.feature.mfcc(
    y=y, sr=sr,
    n_mfcc=13,            # number of MFCCs to return
    n_fft=2048, hop_length=512
)
print(f"MFCCs shape: {mfccs.shape}")  # (n_mfcc, num_frames)

# Display MFCCs
plt.figure(figsize=(14, 5))
librosa.display.specshow(mfccs, sr=sr, hop_length=512, x_axis='time')
plt.colorbar()
plt.title('MFCCs')
plt.tight_layout()
plt.show()

# Compute delta and delta-delta MFCCs
delta_mfccs = librosa.feature.delta(mfccs)           # first derivative
delta2_mfccs = librosa.feature.delta(mfccs, order=2) # second derivative

# Stack for a complete feature set
mfcc_features = np.vstack([mfccs, delta_mfccs, delta2_mfccs])
print(f"Full MFCC feature shape: {mfcc_features.shape}")  # (39, num_frames)

# Normalize MFCCs (common preprocessing step)
mfccs_normalized = (mfccs - np.mean(mfccs, axis=1, keepdims=True)) / \
                   (np.std(mfccs, axis=1, keepdims=True) + 1e-8)
```

---

## Chroma Features

```python
import librosa
import librosa.display
import matplotlib.pyplot as plt

y, sr = librosa.load('audio.wav', sr=22050)

# Chroma features map the spectrum onto 12 pitch classes
chroma = librosa.feature.chroma_stft(y=y, sr=sr, n_fft=2048, hop_length=512)
print(f"Chroma shape: {chroma.shape}")  # (12, num_frames)

# Display chroma features
plt.figure(figsize=(14, 4))
librosa.display.specshow(chroma, sr=sr, hop_length=512,
                          x_axis='time', y_axis='chroma')
plt.colorbar()
plt.title('Chroma Features')
plt.tight_layout()
plt.show()

# Alternative chroma methods
chroma_cqt = librosa.feature.chroma_cqt(y=y, sr=sr)    # CQT-based, better for music
chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)   # energy-normalized, robust to dynamics
```

---

## Spectral Centroid Bandwidth and Rolloff

```python
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

y, sr = librosa.load('audio.wav', sr=22050)

# Spectral centroid: weighted mean of frequencies ("brightness")
centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=512)

# Spectral bandwidth: spread of spectrum around centroid
bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr, hop_length=512)

# Spectral rolloff: frequency below which 85% of energy lies
rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, hop_length=512)

# Spectral flatness: noise-like vs tonal character
flatness = librosa.feature.spectral_flatness(y=y, hop_length=512)

# Spectral contrast: difference between peaks and valleys
contrast = librosa.feature.spectral_contrast(y=y, sr=sr, hop_length=512)

# Plot spectral features overlaid on waveform
frames = range(centroid.shape[1])
t = librosa.frames_to_time(frames, sr=sr, hop_length=512)
plt.figure(figsize=(14, 5))
librosa.display.waveshow(y, sr=sr, alpha=0.4)
plt.plot(t, centroid[0] / sr, color='r', label='Centroid')
plt.plot(t, rolloff[0] / sr, color='g', label='Rolloff')
plt.legend()
plt.title('Spectral Centroid and Rolloff')
plt.tight_layout()
plt.show()
```

---

## Time-Domain Features

```python
import librosa
import matplotlib.pyplot as plt
import numpy as np

y, sr = librosa.load('audio.wav', sr=22050)

# Zero Crossing Rate: rate at which signal changes sign
zcr = librosa.feature.zero_crossing_rate(y, frame_length=2048, hop_length=512)
print(f"Mean ZCR: {zcr.mean():.4f}")  # higher for noisy/unvoiced segments

# RMS Energy per frame
rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)
print(f"Mean RMS: {rms.mean():.4f}")

# Plot ZCR and RMS over time
fig, axes = plt.subplots(2, 1, figsize=(14, 6), sharex=True)
t = librosa.frames_to_time(range(zcr.shape[1]), sr=sr, hop_length=512)
axes[0].plot(t, zcr[0], color='blue')
axes[0].set_ylabel('Zero Crossing Rate')
axes[1].plot(t, rms[0], color='red')
axes[1].set_ylabel('RMS Energy')
axes[1].set_xlabel('Time (s)')
plt.tight_layout()
plt.show()
```

---

## Display Utilities

```python
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

y, sr = librosa.load('audio.wav', sr=22050)
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
S_db = librosa.power_to_db(S, ref=np.max)

# specshow: primary display function for time-frequency representations
# y_axis options: 'hz', 'log', 'mel', 'chroma', 'cqt_note', None
# x_axis options: 'time', 'frames', 's', 'ms', None
plt.figure(figsize=(14, 5))
img = librosa.display.specshow(
    S_db, sr=sr, hop_length=512,
    x_axis='time', y_axis='mel',
    cmap='viridis', vmin=-80, vmax=0
)
plt.colorbar(img, format='%+2.0f dB')
plt.title('Mel Spectrogram with specshow')
plt.tight_layout()
plt.show()

# Multi-panel figure with different representations
fig, axes = plt.subplots(3, 1, figsize=(14, 10))
librosa.display.waveshow(y, sr=sr, ax=axes[0])
axes[0].set_title('Waveform')
librosa.display.specshow(S_db, sr=sr, hop_length=512,
                          x_axis='time', y_axis='mel', ax=axes[1])
axes[1].set_title('Mel Spectrogram')
chroma = librosa.feature.chroma_stft(y=y, sr=sr)
librosa.display.specshow(chroma, sr=sr, hop_length=512,
                          x_axis='time', y_axis='chroma', ax=axes[2])
axes[2].set_title('Chroma')
plt.tight_layout()
plt.show()
```

---

## Beat Tracking and Tempo

```python
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

y, sr = librosa.load('music.wav', sr=22050)

# Estimate tempo (BPM) and beat positions
tempo, beat_frames = librosa.beat.beat_track(
    y=y, sr=sr, hop_length=512,
    start_bpm=120, units='frames'
)
print(f"Estimated tempo: {tempo:.1f} BPM")

# Convert beat frames to time
beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=512)

# Visualize beats on the waveform
plt.figure(figsize=(14, 4))
librosa.display.waveshow(y, sr=sr, alpha=0.6)
for bt in beat_times:
    plt.axvline(x=bt, color='r', alpha=0.5, linestyle='--')
plt.title(f'Beat Tracking (Tempo: {tempo:.1f} BPM)')
plt.tight_layout()
plt.show()

# Tempogram: local tempo estimation over time
onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr, hop_length=512)
plt.figure(figsize=(14, 5))
librosa.display.specshow(tempogram, sr=sr, hop_length=512,
                          x_axis='time', y_axis='tempo')
plt.title('Tempogram')
plt.tight_layout()
plt.show()
```

---

## Onset Detection

```python
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

y, sr = librosa.load('audio.wav', sr=22050)

# Compute onset strength and detect onset frames
onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
onset_frames = librosa.onset.onset_detect(
    y=y, sr=sr, hop_length=512,
    backtrack=True, units='frames'     # move onsets to nearest preceding minimum
)
onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=512)
print(f"Number of onsets: {len(onset_frames)}")

# Visualize onsets on the spectrogram
plt.figure(figsize=(14, 5))
D = librosa.stft(y)
librosa.display.specshow(librosa.amplitude_to_db(np.abs(D), ref=np.max),
                          sr=sr, hop_length=512, x_axis='time', y_axis='hz')
plt.vlines(onset_times, 0, sr / 2, color='r', alpha=0.7, label='Onsets')
plt.legend()
plt.title('Onset Detection')
plt.tight_layout()
plt.show()
```

---

## Pitch Tracking

```python
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

y, sr = librosa.load('audio.wav', sr=22050)

# Pitch tracking using pYIN algorithm
f0, voiced_flag, voiced_probs = librosa.pyin(
    y,
    fmin=librosa.note_to_hz('C2'),   # minimum expected frequency
    fmax=librosa.note_to_hz('C7'),   # maximum expected frequency
    sr=sr, hop_length=512
)

# Plot pitch on a spectrogram
times = librosa.times_like(f0, sr=sr, hop_length=512)
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
plt.figure(figsize=(14, 5))
librosa.display.specshow(D, sr=sr, hop_length=512, x_axis='time', y_axis='log')
plt.plot(times, f0, color='cyan', linewidth=2, label='f0 (pYIN)')
plt.legend()
plt.title('Pitch Contour on Spectrogram')
plt.tight_layout()
plt.show()

# Convert to MIDI note numbers and names
midi_notes = librosa.hz_to_midi(f0[voiced_flag])
note_names = librosa.midi_to_note(midi_notes.astype(int))
print(f"First 5 detected notes: {note_names[:5]}")
```

---

## Audio Effects

```python
import librosa
import numpy as np

y, sr = librosa.load('audio.wav', sr=22050)

# Time stretching: change speed without changing pitch
y_fast = librosa.effects.time_stretch(y, rate=1.5)    # 1.5x faster
y_slow = librosa.effects.time_stretch(y, rate=0.75)   # 25% slower

# Pitch shifting: change pitch without changing speed
y_up = librosa.effects.pitch_shift(y, sr=sr, n_steps=4)     # up 4 semitones
y_down = librosa.effects.pitch_shift(y, sr=sr, n_steps=-3)  # down 3 semitones

# Harmonic-percussive source separation
y_harmonic, y_percussive = librosa.effects.hpss(y)

# Trim silence from beginning and end
y_trimmed, trim_indices = librosa.effects.trim(y, top_db=20)

# Split audio on silence
intervals = librosa.effects.split(y, top_db=30)
print(f"Number of non-silent intervals: {len(intervals)}")

# Preemphasis / deemphasis filters (common in speech processing)
y_preemph = librosa.effects.preemphasis(y, coef=0.97)
y_deemph = librosa.effects.deemphasis(y_preemph, coef=0.97)
```

---

## Feature Extraction Pipeline

```python
import librosa
import numpy as np

def extract_features(file_path, sr=22050, n_mfcc=13):
    """Extract a comprehensive set of audio features from a file."""
    y, sr = librosa.load(file_path, sr=sr)

    # Spectral features
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    delta_mfccs = librosa.feature.delta(mfccs)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    flatness = librosa.feature.spectral_flatness(y=y)

    # Time-domain features
    zcr = librosa.feature.zero_crossing_rate(y)
    rms = librosa.feature.rms(y=y)

    # Rhythm features
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Aggregate statistics: mean and std per feature
    features = {
        'mfcc_mean': np.mean(mfccs, axis=1),
        'mfcc_std': np.std(mfccs, axis=1),
        'delta_mfcc_mean': np.mean(delta_mfccs, axis=1),
        'chroma_mean': np.mean(chroma, axis=1),
        'centroid_mean': np.mean(centroid),
        'bandwidth_mean': np.mean(bandwidth),
        'rolloff_mean': np.mean(rolloff),
        'contrast_mean': np.mean(contrast, axis=1),
        'flatness_mean': np.mean(flatness),
        'zcr_mean': np.mean(zcr),
        'rms_mean': np.mean(rms),
        'tempo': tempo,
    }
    return features

# Create a flat feature vector for machine learning
def features_to_vector(features):
    """Flatten all features into a single 1D vector."""
    parts = []
    for key in sorted(features.keys()):
        val = features[key]
        if isinstance(val, np.ndarray):
            parts.append(val.flatten())
        else:
            parts.append(np.array([val]))
    return np.concatenate(parts)

features = extract_features('audio.wav')
feature_vector = features_to_vector(features)
print(f"Feature vector length: {len(feature_vector)}")
```

---

## Saving and Exporting

```python
import librosa
import librosa.display
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

y, sr = librosa.load('audio.wav', sr=22050)

# Save processed audio using soundfile
y_processed = librosa.effects.time_stretch(y, rate=1.25)
sf.write('output_stretched.wav', y_processed, sr)
sf.write('output.flac', y_processed, sr, format='FLAC')

# Save features to disk using NumPy
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
np.save('mfccs.npy', mfccs)

# Save multiple features to a single file
mel_spec = librosa.feature.melspectrogram(y=y, sr=sr)
chroma = librosa.feature.chroma_stft(y=y, sr=sr)
np.savez('features.npz', mfccs=mfccs, mel_spec=mel_spec, chroma=chroma)

# Export a spectrogram as an image
S_db = librosa.power_to_db(mel_spec, ref=np.max)
fig, ax = plt.subplots(figsize=(10, 4))
librosa.display.specshow(S_db, sr=sr, hop_length=512,
                          x_axis='time', y_axis='mel', ax=ax)
plt.colorbar(format='%+2.0f dB')
fig.savefig('spectrogram.png', dpi=150, bbox_inches='tight')
plt.close(fig)
```

---

## Practice Exercises

1. Load an audio file, compute its mel spectrogram with 64 mel bands, and display it alongside the waveform in a two-panel figure.

2. Extract MFCCs (13 coefficients), their deltas, and delta-deltas, then compute the mean and standard deviation across time for each coefficient.

3. Use beat tracking on a music file and create a click track by placing short clicks at each detected beat position using `librosa.clicks()`.

4. Apply harmonic-percussive source separation to a music file and compare the chroma features of the harmonic component with the original.

5. Build a feature extraction function that processes a directory of audio files and saves all feature vectors into a single CSV file for classification.

6. Use pitch tracking (pYIN) on a vocal recording, filter out unvoiced frames, and plot the pitch contour in both Hz and MIDI note numbers.

---

## Summary

librosa is a comprehensive Python library for audio and music analysis. It provides tools for loading audio into NumPy arrays, computing spectral features (STFT, mel spectrograms, MFCCs, chroma), analyzing rhythm (beat tracking, tempo estimation, onset detection), tracking pitch, and applying audio effects. The library's consistent API and integration with matplotlib make it well-suited for research, prototyping, and building audio processing pipelines.

---

## Next Steps

- Explore advanced harmonic analysis with CQT and variable-Q transforms
- Combine librosa features with scikit-learn for audio classification tasks
- Investigate librosa's segment and decomposition modules for structural analysis
- Use librosa with deep learning frameworks for audio-based neural networks

---

## Additional Resources

- [librosa Documentation](https://librosa.org/doc/latest/)
- [librosa GitHub Repository](https://github.com/librosa/librosa)
- [librosa Tutorial Notebooks](https://librosa.org/doc/latest/tutorial.html)
- [Music Information Retrieval with librosa (ISMIR)](https://musicinformationretrieval.com/)
- [Audio Signal Processing for Machine Learning (YouTube)](https://www.youtube.com/playlist?list=PL-wATfeyAMNqIee7cH3q1bh4QJFAaeNv0)
