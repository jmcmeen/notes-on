# Introduction to SoundFile

## Table of Contents

- [What is SoundFile](#what-is-soundfile)
- [Installation](#installation)
- [Reading Audio Files](#reading-audio-files)
- [Getting File Information](#getting-file-information)
- [The SoundFile Object](#the-soundfile-object)
- [Writing Audio Files](#writing-audio-files)
- [Supported Formats](#supported-formats)
- [Block-wise Reading](#block-wise-reading)
- [Metadata](#metadata)
- [NumPy Integration](#numpy-integration)
- [Format Conversion](#format-conversion)
- [Comparison with Other Libraries](#comparison-with-other-libraries)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is SoundFile

SoundFile is a Python library for reading and writing audio files. It is a wrapper around the C library libsndfile, which supports a wide range of audio formats. SoundFile provides a simple, NumPy-friendly interface for working with audio data and is commonly used as a backend by other audio libraries like librosa.

Key features:
- Read and write WAV, FLAC, OGG, AIFF, and many other formats
- Direct integration with NumPy arrays
- Block-wise reading for processing large files without loading them into memory
- Access to audio file metadata and format information
- Thread-safe and efficient C-based backend

---

## Installation

```python
# Install SoundFile using pip
# pip install soundfile

# On Linux, you may need to install libsndfile separately
# sudo apt install libsndfile1   (Debian/Ubuntu)

# Verify the installation
import soundfile as sf
print(sf.__version__)  # prints the installed version
```

---

## Reading Audio Files

```python
import soundfile as sf
import numpy as np

# Read an entire audio file - returns (data, samplerate)
data, samplerate = sf.read('audio.wav')
print(f"Shape: {data.shape}")           # (num_samples,) mono, (num_samples, channels) stereo
print(f"Sample rate: {samplerate}")
print(f"Duration: {len(data) / samplerate:.2f} seconds")

# Read with a specific data type
data_float32, sr = sf.read('audio.wav', dtype='float32')   # 32-bit float
data_int16, sr = sf.read('audio.wav', dtype='int16')       # 16-bit integer

# Read only a portion of the file
data_section, sr = sf.read('audio.wav', start=44100, stop=88200)

# Force 2D output even for mono files
data_2d, sr = sf.read('mono.wav', always_2d=True)
print(f"2D mono shape: {data_2d.shape}")  # (num_samples, 1)

# Read into a pre-allocated buffer
buffer = np.empty((44100, 2), dtype='float64')
sf.read('stereo.wav', out=buffer)
```

---

## Getting File Information

```python
import soundfile as sf

# Get file information without reading the data
info = sf.info('audio.wav')
print(f"Channels: {info.channels}")
print(f"Sample rate: {info.samplerate}")
print(f"Frames: {info.frames}")
print(f"Duration: {info.duration:.2f} s")
print(f"Format: {info.format}")           # e.g., 'WAV'
print(f"Subtype: {info.subtype}")         # e.g., 'PCM_16'
print(f"Format info: {info.format_info}")
print(f"Subtype info: {info.subtype_info}")

# Check properties for multiple files
import os
audio_dir = 'audio_files/'
for filename in os.listdir(audio_dir):
    if filename.endswith(('.wav', '.flac', '.ogg')):
        filepath = os.path.join(audio_dir, filename)
        info = sf.info(filepath)
        print(f"{filename}: {info.channels}ch, {info.samplerate}Hz, "
              f"{info.duration:.1f}s, {info.subtype}")
```

---

## The SoundFile Object

```python
import soundfile as sf
import numpy as np

# Open a file for more control
with sf.SoundFile('audio.wav') as f:
    print(f"Channels: {f.channels}, SR: {f.samplerate}, Frames: {f.frames}")

    chunk = f.read(1024)         # read 1024 frames
    chunk2 = f.read(1024)       # continues from current position

    f.seek(0)                    # seek back to the beginning
    f.seek(44100)                # seek to sample 44100
    pos = f.tell()               # get current position

    remaining = f.read()         # read all remaining frames

# Open for writing
with sf.SoundFile('output.wav', mode='w', samplerate=44100,
                   channels=2, subtype='PCM_16') as f:
    for i in range(10):
        data = np.random.randn(1024, 2).astype('float64') * 0.1
        f.write(data)            # append data to the file

# Open in read-write mode
with sf.SoundFile('audio.wav', mode='r+') as f:
    data = f.read()
    f.seek(0)
    f.write(data * 0.5)         # overwrite with half-volume audio
```

---

## Writing Audio Files

```python
import soundfile as sf
import numpy as np

# Generate a sine wave for demonstration
samplerate = 44100
duration = 3.0
t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
signal = 0.5 * np.sin(2 * np.pi * 440 * t)

# Write a WAV file
sf.write('sine_wave.wav', signal, samplerate)

# Write with a specific subtype
sf.write('sine_16bit.wav', signal, samplerate, subtype='PCM_16')
sf.write('sine_24bit.wav', signal, samplerate, subtype='PCM_24')
sf.write('sine_float.wav', signal, samplerate, subtype='FLOAT')

# Write a stereo file
left = 0.5 * np.sin(2 * np.pi * 440 * t)
right = 0.5 * np.sin(2 * np.pi * 554.37 * t)
stereo = np.column_stack([left, right])
sf.write('stereo_output.wav', stereo, samplerate)

# Write different formats
sf.write('output.flac', signal, samplerate, format='FLAC')
sf.write('output.ogg', signal, samplerate, format='OGG', subtype='VORBIS')
sf.write('output.aiff', signal, samplerate, format='AIFF')
```

---

## Supported Formats

```python
import soundfile as sf

# List all available formats
print("Available formats:")
for fmt, description in sf.available_formats().items():
    print(f"  {fmt}: {description}")
# Common: WAV, FLAC, OGG, AIFF, AU, RAW

# List all available subtypes
print("\nAvailable subtypes:")
for subtype, description in sf.available_subtypes().items():
    print(f"  {subtype}: {description}")
# Common: PCM_16, PCM_24, PCM_32, FLOAT, DOUBLE, VORBIS

# Check subtypes for a specific format
print("\nWAV subtypes:")
for subtype, desc in sf.available_subtypes('WAV').items():
    print(f"  {subtype}: {desc}")

# Validate format/subtype combinations
print(f"WAV + PCM_16: {sf.check_format('WAV', 'PCM_16')}")    # True
print(f"OGG + PCM_16: {sf.check_format('OGG', 'PCM_16')}")    # False
print(f"OGG + VORBIS: {sf.check_format('OGG', 'VORBIS')}")    # True
```

---

## Block-wise Reading

```python
import soundfile as sf
import numpy as np

block_size = 4096

# Read a large file in blocks using the blocks generator
for block in sf.blocks('large_audio.wav', blocksize=block_size):
    rms = np.sqrt(np.mean(block ** 2))
    print(f"Block shape: {block.shape}, RMS: {rms:.4f}")

# Block reading with overlap
for block in sf.blocks('large_audio.wav', blocksize=block_size, overlap=1024):
    print(f"Overlapped block shape: {block.shape}")

# Compute global statistics without loading entire file
total_energy = 0.0
total_frames = 0
for block in sf.blocks('large_audio.wav', blocksize=block_size):
    total_energy += np.sum(block ** 2)
    total_frames += len(block)
rms_global = np.sqrt(total_energy / total_frames)

# Block-wise processing and writing to a new file
with sf.SoundFile('large_audio.wav') as infile:
    with sf.SoundFile('processed.wav', mode='w', samplerate=infile.samplerate,
                       channels=infile.channels, subtype=infile.subtype) as outfile:
        while True:
            data = infile.read(block_size)
            if len(data) == 0:
                break
            outfile.write(data * 0.5)    # apply gain reduction per block
```

---

## Metadata

```python
import soundfile as sf

# SoundFile provides basic metadata through the info object
info = sf.info('audio.wav')
print(f"Format: {info.format}, Subtype: {info.subtype}")
print(f"Endian: {info.endian}, Sections: {info.sections}")
print(f"Extra info: {info.extra_info}")

# Note: SoundFile has limited metadata support for tags (title, artist, etc.)
# For full metadata, combine SoundFile with mutagen or tinytag:
# pip install mutagen
# from mutagen.flac import FLAC
# audio = FLAC('audio.flac')
# print(audio.tags)
# data, sr = sf.read('audio.flac')  # read audio data with SoundFile
```

---

## NumPy Integration

```python
import soundfile as sf
import numpy as np

# SoundFile returns NumPy arrays by default
data, sr = sf.read('audio.wav')
print(f"Type: {type(data)}, Dtype: {data.dtype}")  # float64 by default

# Perform NumPy operations directly on audio data
peak = np.max(np.abs(data))
rms = np.sqrt(np.mean(data ** 2))
print(f"Peak: {peak:.4f}, RMS: {rms:.4f}, dB: {20 * np.log10(rms + 1e-10):.1f}")

# Normalize and save
normalized = data / (peak + 1e-10)
sf.write('normalized.wav', normalized, sr)

# Mix two audio files with zero-padding
data1, sr1 = sf.read('track1.wav', dtype='float64')
data2, sr2 = sf.read('track2.wav', dtype='float64')
max_len = max(len(data1), len(data2))
data1_padded = np.pad(data1, (0, max_len - len(data1)))
data2_padded = np.pad(data2, (0, max_len - len(data2)))
mixed = 0.5 * data1_padded + 0.5 * data2_padded
sf.write('mixed.wav', mixed, sr1)

# Channel manipulation
stereo, sr = sf.read('stereo.wav', always_2d=True)
left = stereo[:, 0]               # extract left channel
right = stereo[:, 1]              # extract right channel
mono = np.mean(stereo, axis=1)    # downmix to mono
sf.write('mono_downmix.wav', mono, sr)
```

---

## Format Conversion

```python
import soundfile as sf

# Convert between formats
data, sr = sf.read('input.wav')
sf.write('output.flac', data, sr, format='FLAC')
sf.write('output.ogg', data, sr, format='OGG', subtype='VORBIS')

# Convert with specific bit depth
data, sr = sf.read('input.flac')
sf.write('output_16bit.wav', data, sr, subtype='PCM_16')
sf.write('output_24bit.wav', data, sr, subtype='PCM_24')

# Convert and resample (requires librosa)
import librosa
y, sr_orig = librosa.load('input_48k.wav', sr=None)
y_resampled = librosa.resample(y, orig_sr=sr_orig, target_sr=16000)
sf.write('output_16k.wav', y_resampled, 16000)

# Batch conversion
import os
input_dir, output_dir = 'wav_files/', 'flac_files/'
os.makedirs(output_dir, exist_ok=True)
for filename in os.listdir(input_dir):
    if filename.endswith('.wav'):
        data, sr = sf.read(os.path.join(input_dir, filename))
        sf.write(os.path.join(output_dir, filename.replace('.wav', '.flac')),
                 data, sr, format='FLAC')
```

---

## Comparison with Other Libraries

```python
# SoundFile vs other Python audio I/O libraries:
#
# SoundFile (soundfile):
#   - Wrapper around libsndfile (C library)
#   - Supports WAV, FLAC, OGG, AIFF (NOT MP3)
#   - Returns NumPy arrays directly, block-wise reading
#   - Best for: lossless format I/O, scientific audio work
#
# scipy.io.wavfile:
#   - Part of SciPy, no extra install
#   - WAV only, returns raw integer data
#   - Best for: simple WAV reading when SciPy is available
#
# wave (standard library):
#   - Built into Python, WAV only
#   - Returns raw bytes (manual conversion needed)
#   - Best for: minimal dependency requirements
#
# pydub:
#   - High-level audio manipulation (not just I/O)
#   - Supports MP3, WAV, OGG, FLAC via ffmpeg
#   - Uses AudioSegment objects (not NumPy arrays)
#   - Best for: audio editing tasks, MP3 support

# Example: same file with different libraries
import soundfile as sf
data_sf, sr_sf = sf.read('audio.wav')    # float64 NumPy array

from scipy.io import wavfile
sr_scipy, data_scipy = wavfile.read('audio.wav')  # integer array
print(f"SoundFile: {data_sf.dtype}, SciPy: {data_scipy.dtype}")
```

---

## Practice Exercises

1. Read a WAV file, print its properties (channels, sample rate, duration, format), and write it out as a FLAC file preserving the same sample rate.

2. Implement a block-wise audio normalizer that reads a large file in chunks, finds the global peak, then processes the file again to normalize every block.

3. Write a script that generates a 5-second stereo sine wave with different frequencies in each channel and saves it as both WAV and FLAC.

4. Create a format conversion tool that converts all WAV files in a directory to OGG Vorbis, printing the compression ratio for each file.

5. Read a stereo audio file, swap the left and right channels, and write the result to a new file.

---

## Summary

SoundFile is a reliable and efficient library for reading and writing audio files in Python. Built on the mature libsndfile C library, it provides direct NumPy integration, support for multiple lossless formats (WAV, FLAC, OGG, AIFF), block-wise processing for large files, and a clean API for both simple one-line operations and more complex streaming workflows. It is widely used as a backend for higher-level audio libraries and is a solid choice for any audio I/O task that does not require MP3 support.

---

## Next Steps

- Explore using SoundFile as a backend for librosa and torchaudio
- Learn about different PCM subtypes and when to use each bit depth
- Investigate real-time audio streaming by combining SoundFile with sounddevice
- Study audio format specifications to understand trade-offs between WAV, FLAC, and OGG

---

## Additional Resources

- [SoundFile Documentation](https://python-soundfile.readthedocs.io/)
- [SoundFile GitHub Repository](https://github.com/bastibe/python-soundfile)
- [libsndfile Documentation](http://www.mega-nerd.com/libsndfile/)
- [Audio File Format Specifications](https://en.wikipedia.org/wiki/Audio_file_format)
