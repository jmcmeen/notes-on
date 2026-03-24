# Introduction to sounddevice

## Table of Contents

- [What is sounddevice](#what-is-sounddevice)
- [Installation](#installation)
- [Playing Audio](#playing-audio)
- [Recording Audio](#recording-audio)
- [Simultaneous Play and Record](#simultaneous-play-and-record)
- [Stream API](#stream-api)
- [Real-Time Processing](#real-time-processing)
- [Device Configuration](#device-configuration)
- [NumPy Integration](#numpy-integration)
- [Audio Monitoring](#audio-monitoring)
- [Recording to File](#recording-to-file)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is sounddevice

sounddevice is a Python library for playing and recording audio through your computer's sound hardware. It is a wrapper around the PortAudio C library, providing access to audio input and output devices. sounddevice supports blocking and callback-based audio I/O, making it suitable for both simple playback tasks and real-time audio processing applications.

Key features:
- Play NumPy arrays as audio through speakers
- Record audio from microphones into NumPy arrays
- Simultaneous playback and recording (full-duplex)
- Callback-based streaming for real-time processing
- Query and select audio devices
- Cross-platform support (Windows, macOS, Linux)

---

## Installation

```python
# Install sounddevice using pip
# pip install sounddevice

# On Linux, you may need PortAudio
# sudo apt install libportaudio2   (Debian/Ubuntu)

# Optional: install soundfile for file I/O
# pip install soundfile

import sounddevice as sd
print(f"sounddevice: {sd.__version__}")
print(sd.query_devices())  # list available audio devices
```

---

## Playing Audio

```python
import sounddevice as sd
import numpy as np

# Generate a sine wave
sample_rate = 44100
duration = 2.0
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio = 0.3 * np.sin(2 * np.pi * 440 * t)  # 440 Hz, amplitude 0.3

# Play audio (blocking - waits until done)
sd.play(audio, samplerate=sample_rate)
sd.wait()

# Play without blocking
sd.play(audio, samplerate=sample_rate, blocking=False)
# ... do other work ...
sd.wait()  # wait when ready

# Stop playback early
sd.play(audio, samplerate=sample_rate)
import time
time.sleep(0.5)
sd.stop()

# Play stereo audio
left = 0.3 * np.sin(2 * np.pi * 440 * t)
right = 0.3 * np.sin(2 * np.pi * 554 * t)
stereo = np.column_stack([left, right])     # shape: (samples, 2)
sd.play(stereo, samplerate=sample_rate)
sd.wait()

# Play from a file (requires soundfile: pip install soundfile)
import soundfile as sf
data, sr = sf.read('audio.wav')
sd.play(data, samplerate=sr); sd.wait()
```

---

## Recording Audio

```python
import sounddevice as sd
import numpy as np

sample_rate = 44100
duration = 5.0

# Blocking recording
recording = sd.rec(
    frames=int(sample_rate * duration),
    samplerate=sample_rate,
    channels=1,
    dtype='float32'
)
sd.wait()
print(f"Recording: {recording.shape}")  # (num_frames, channels)

# Record stereo
stereo_rec = sd.rec(int(sample_rate * duration), samplerate=sample_rate,
                    channels=2, dtype='float32')
sd.wait()
# Record into a pre-allocated buffer
buffer = np.empty((int(sample_rate * duration), 1), dtype='float32')
sd.rec(int(sample_rate * duration), samplerate=sample_rate,
       channels=1, out=buffer)
sd.wait()
# Set default parameters
sd.default.device = (0, 1)          # (input, output)
sd.default.samplerate = 44100
sd.default.channels = 1

# Check recording levels
peak = np.max(np.abs(recording))
rms = np.sqrt(np.mean(recording ** 2))
print(f"Peak: {peak:.4f}, RMS: {rms:.4f}, dB: {20 * np.log10(peak + 1e-10):.1f}")
```

---

## Simultaneous Play and Record

```python
import sounddevice as sd
import soundfile as sf
import numpy as np

# Load audio and play while recording (playrec)
play_data, play_sr = sf.read('stimulus.wav', dtype='float32')
recording = sd.playrec(play_data, samplerate=play_sr, channels=1, dtype='float32')
sd.wait()
print(f"Played: {play_data.shape}, Recorded: {recording.shape}")

# Measure impulse response: play stimulus and record room response
def measure_impulse_response(stimulus, sample_rate, extra_time=1.0):
    total = len(stimulus) + int(sample_rate * extra_time)
    padded = np.zeros(total)
    padded[:len(stimulus)] = stimulus
    rec = sd.playrec(padded.reshape(-1, 1), samplerate=sample_rate,
                     channels=1, dtype='float32')
    sd.wait()
    return rec

# Generate a log sweep and measure response
t = np.linspace(0, 2.0, int(play_sr * 2.0), endpoint=False)
sweep = 0.3 * np.sin(2 * np.pi * np.logspace(1, 4, len(t)) * t)
response = measure_impulse_response(sweep, play_sr)
```

---

## Stream API

```python
import sounddevice as sd
import numpy as np
import time

# InputStream: recording with callback
def input_callback(indata, frames, time_info, status):
    """Called for each audio block from the input."""
    print(f"RMS: {np.sqrt(np.mean(indata ** 2)):.4f}")

with sd.InputStream(samplerate=44100, channels=1, dtype='float32',
                     blocksize=1024, callback=input_callback):
    time.sleep(3)

# OutputStream: playback with callback
phase = 0
def output_callback(outdata, frames, time_info, status):
    """Fill output buffer with generated audio."""
    global phase
    t = (np.arange(frames) + phase) / 44100
    outdata[:, 0] = 0.3 * np.sin(2 * np.pi * 440 * t)
    phase += frames

with sd.OutputStream(samplerate=44100, channels=1, dtype='float32',
                      blocksize=1024, callback=output_callback):
    time.sleep(2)

# Full-duplex Stream: simultaneous input and output
def duplex_callback(indata, outdata, frames, time_info, status):
    outdata[:] = indata  # pass-through (monitoring)

with sd.Stream(samplerate=44100, channels=1, dtype='float32',
               blocksize=1024, callback=duplex_callback):
    time.sleep(5)
```

---

## Real-Time Processing

```python
import sounddevice as sd
import numpy as np
import queue

# Real-time processor with gain and lowpass filter
class RealtimeProcessor:
    """Apply gain and lowpass filter in real time."""

    def __init__(self, sample_rate=44100, blocksize=1024, gain_db=0.0):
        self.sample_rate = sample_rate
        self.blocksize = blocksize
        self.gain = 10 ** (gain_db / 20)
        self.prev_sample = 0.0

    def callback(self, indata, outdata, frames, time_info, status):
        processed = indata * self.gain
        alpha = 0.1  # lowpass filter coefficient
        for i in range(frames):
            processed[i, 0] = alpha * processed[i, 0] + (1 - alpha) * self.prev_sample
            self.prev_sample = processed[i, 0]
        outdata[:] = processed

    def start(self, duration=10):
        with sd.Stream(samplerate=self.sample_rate, blocksize=self.blocksize,
                       channels=1, dtype='float32', callback=self.callback,
                       latency='low') as stream:
            print(f"Latency: {stream.latency}")
            import time; time.sleep(duration)

# processor = RealtimeProcessor(gain_db=-6)
# processor.start(duration=10)

# Real-time level meter
level_queue = queue.Queue()

def level_callback(indata, frames, time_info, status):
    """Compute dB level and queue it."""
    level_queue.put(20 * np.log10(np.sqrt(np.mean(indata ** 2)) + 1e-10))

def run_level_meter(duration=10):
    """Console-based level meter."""
    with sd.InputStream(samplerate=44100, channels=1, blocksize=2048,
                         callback=level_callback):
        import time
        end = time.time() + duration
        while time.time() < end:
            try:
                db = level_queue.get(timeout=0.1)
                bar = '#' * max(0, int((db + 60) * 0.8))
                print(f"\r{db:6.1f} dBFS |{bar:<50}|", end='', flush=True)
            except queue.Empty:
                pass
    print()
```

---

## Device Configuration

```python
import sounddevice as sd

# Query all available devices
print(sd.query_devices())

# Query a specific device by index
info = sd.query_devices(0)
print(f"Device 0: {info['name']}")
print(f"  Input ch: {info['max_input_channels']}, Output ch: {info['max_output_channels']}")
print(f"  Default SR: {info['default_samplerate']}")

# Get default devices
print(f"Default input: {sd.query_devices(kind='input')['name']}")
print(f"Default output: {sd.query_devices(kind='output')['name']}")

# Set default parameters
sd.default.device = (0, 1)           # (input_index, output_index)
sd.default.samplerate = 44100
sd.default.channels = 1
sd.default.dtype = 'float32'
sd.default.latency = 'low'          # 'low', 'high', or seconds

# Check which sample rates a device supports
def check_rates(device, rates=[8000, 16000, 22050, 44100, 48000, 96000]):
    supported = []
    for rate in rates:
        try:
            sd.check_input_settings(device=device, samplerate=rate)
            supported.append(rate)
        except sd.PortAudioError:
            pass
    return supported

print(f"Supported rates: {check_rates(0)}")
```

---

## NumPy Integration

```python
import sounddevice as sd
import numpy as np

sample_rate = 44100
duration = 3.0
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate signals with NumPy
sine = 0.3 * np.sin(2 * np.pi * 440 * t).astype(np.float32)
chord = 0.2 * (np.sin(2 * np.pi * 261.63 * t) +       # C4
               np.sin(2 * np.pi * 329.63 * t) +        # E4
               np.sin(2 * np.pi * 392.00 * t)).astype(np.float32)  # G4
noise = 0.1 * np.random.randn(int(sample_rate * duration)).astype(np.float32)

# Record and analyze
recording = sd.rec(int(sample_rate * 2), samplerate=sample_rate,
                   channels=1, dtype='float32')
sd.wait()
recording = recording.flatten()

# Normalize, fade out, and find dominant frequency
normalized = recording / (np.max(np.abs(recording)) + 1e-10)
faded = normalized * np.linspace(1, 0, len(normalized))
fft_result = np.fft.rfft(recording)
frequencies = np.fft.rfftfreq(len(recording), d=1/sample_rate)
dominant = frequencies[np.argmax(np.abs(fft_result[1:])) + 1]
print(f"Dominant frequency: {dominant:.1f} Hz")
```

---

## Audio Monitoring

```python
import sounddevice as sd
import numpy as np
import threading

# Simple audio pass-through (monitor mic through speakers)
def monitor_callback(indata, outdata, frames, time_info, status):
    outdata[:] = indata  # direct pass-through

def start_monitor(duration=30, sample_rate=44100):
    with sd.Stream(samplerate=sample_rate, channels=1, dtype='float32',
                   blocksize=512, latency='low', callback=monitor_callback) as stream:
        print(f"Latency: in={stream.latency[0]*1000:.1f}ms, "
              f"out={stream.latency[1]*1000:.1f}ms")
        import time; time.sleep(duration)

# Monitor with real-time level display
class AudioMonitor:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.peak_level = -100
        self.running = False

    def callback(self, indata, outdata, frames, time_info, status):
        outdata[:] = indata * 0.8          # slight gain reduction for safety
        self.peak_level = 20 * np.log10(np.sqrt(np.mean(indata ** 2)) + 1e-10)

    def start(self, duration=30):
        self.running = True
        def display():
            while self.running:
                bar = '=' * max(0, int((self.peak_level + 60) * 0.8))
                print(f"\r{self.peak_level:6.1f} dBFS |{bar:<50}|",
                      end='', flush=True)
                import time; time.sleep(0.05)
        threading.Thread(target=display, daemon=True).start()
        with sd.Stream(samplerate=self.sample_rate, channels=1, dtype='float32',
                       latency='low', callback=self.callback):
            import time; time.sleep(duration)
        self.running = False
```

---

## Recording to File

```python
import sounddevice as sd
import soundfile as sf
import numpy as np
import queue
import threading

# Simple record and save
def record_to_wav(filename, duration, sample_rate=44100):
    """Record and save to WAV."""
    recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate,
                       channels=1, dtype='float32')
    sd.wait()
    sf.write(filename, recording, sample_rate)

# Stream recording to file (memory-efficient for long recordings)
class FileRecorder:
    """Stream audio directly to a file using a background writer thread."""

    def __init__(self, filename, sample_rate=44100, channels=1):
        self.filename = filename
        self.sample_rate = sample_rate
        self.channels = channels
        self.q = queue.Queue()
        self.recording = False

    def callback(self, indata, frames, time_info, status):
        self.q.put(indata.copy())

    def record(self, duration):
        self.recording = True
        def write_loop():
            with sf.SoundFile(self.filename, mode='w', samplerate=self.sample_rate,
                               channels=self.channels, subtype='PCM_16') as f:
                while self.recording or not self.q.empty():
                    try:
                        f.write(self.q.get(timeout=0.1))
                    except queue.Empty:
                        continue
        writer = threading.Thread(target=write_loop, daemon=True)
        writer.start()
        with sd.InputStream(samplerate=self.sample_rate, channels=self.channels,
                             dtype='float32', blocksize=4096, callback=self.callback):
            import time; time.sleep(duration)
        self.recording = False
        writer.join()

# recorder = FileRecorder('long_recording.wav')
# recorder.record(duration=60)

# Record until sustained silence is detected
def record_until_silence(filename, sample_rate=44100, silence_thresh=-40,
                         silence_duration=2.0):
    chunks, silence_samples = [], 0
    max_silence, active = int(sample_rate * silence_duration), True

    def callback(indata, frames, time_info, status):
        nonlocal silence_samples, active
        chunks.append(indata.copy())
        db = 20 * np.log10(np.sqrt(np.mean(indata ** 2)) + 1e-10)
        silence_samples = silence_samples + frames if db < silence_thresh else 0
        if silence_samples > max_silence:
            active = False

    with sd.InputStream(samplerate=sample_rate, channels=1, dtype='float32',
                         blocksize=1024, callback=callback):
        import time
        while active: time.sleep(0.1)
    sf.write(filename, np.concatenate(chunks), sample_rate)
```

---

## Practice Exercises

1. Generate a C major chord (C4, E4, G4) with fade-in/fade-out and play it through speakers.

2. Build a voice recorder with real-time RMS level display that saves to WAV.

3. Implement real-time audio pass-through with adjustable gain using the Stream API.

4. Create a tremolo effect (amplitude modulation) applied to microphone input in real time.

5. Record audio and print the dominant frequency per 1-second window using FFT.

6. Build a recording tool that splits audio into separate files on silence detection.

---

## Summary

sounddevice is a Python wrapper around PortAudio for real-time audio input and output. It provides simple functions for playing (play) and recording (rec) NumPy arrays, simultaneous playback and recording (playrec), and a powerful Stream API with callback-based processing for low-latency real-time applications. Combined with soundfile for file I/O and NumPy for signal processing, sounddevice enables a wide range of audio applications from simple playback to real-time effects and monitoring.

---

## Next Steps

- Build a real-time audio effects chain with multiple processing stages
- Combine sounddevice with librosa for real-time feature extraction
- Study PortAudio documentation for advanced device configuration

---

## Additional Resources

- [sounddevice Documentation](https://python-sounddevice.readthedocs.io/)
- [sounddevice GitHub Repository](https://github.com/spatialaudio/python-sounddevice)
- [PortAudio Documentation](http://www.portaudio.com/docs.html)
