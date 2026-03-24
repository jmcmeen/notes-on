# Introduction to pydub

## Table of Contents

- [What is pydub](#what-is-pydub)
- [Installation](#installation)
- [Loading Audio](#loading-audio)
- [Audio Properties](#audio-properties)
- [Slicing and Concatenation](#slicing-and-concatenation)
- [Effects](#effects)
- [Volume Adjustment](#volume-adjustment)
- [Working with Silence](#working-with-silence)
- [Export](#export)
- [Overlay and Mixing](#overlay-and-mixing)
- [Channel Operations](#channel-operations)
- [Sample Rate and Sample Width Conversion](#sample-rate-and-sample-width-conversion)
- [Generating Tones](#generating-tones)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is pydub

pydub is a high-level Python library for audio manipulation. It provides an intuitive interface for common audio editing tasks like slicing, concatenation, volume adjustment, and format conversion. pydub uses ffmpeg as its backend, giving it broad format support including MP3, WAV, OGG, FLAC, and many more.

Key features:
- Simple, Pythonic API for audio manipulation
- Millisecond-precision slicing with bracket notation
- Easy concatenation with the `+` operator
- Volume adjustment with `+` and `-` in dB
- Built-in effects: fade, normalize, speed change, reverse
- Silence detection and splitting

---

## Installation

```python
# Install pydub using pip
# pip install pydub

# pydub requires ffmpeg for non-WAV formats
# sudo apt install ffmpeg       (Debian/Ubuntu)
# brew install ffmpeg            (macOS)

# Optional: install simpleaudio for playback
# pip install simpleaudio

from pydub import AudioSegment
print("pydub imported successfully")
```

---

## Loading Audio

```python
from pydub import AudioSegment

# Load audio from different formats
audio_wav = AudioSegment.from_wav('audio.wav')
audio_mp3 = AudioSegment.from_mp3('audio.mp3')
audio_ogg = AudioSegment.from_ogg('audio.ogg')

# Generic loader for any format supported by ffmpeg
audio = AudioSegment.from_file('audio.flac', format='flac')
audio = AudioSegment.from_file('audio.m4a', format='m4a')

# Load raw audio data
raw_audio = AudioSegment.from_raw(
    'audio.raw',
    sample_width=2,          # 2 bytes = 16-bit
    frame_rate=44100,
    channels=1
)

# Load only a portion of a file
audio_section = AudioSegment.from_file(
    'long_audio.mp3', format='mp3',
    start_second=10, duration=30     # load 30 seconds starting at 10s
)
```

---

## Audio Properties

```python
from pydub import AudioSegment

audio = AudioSegment.from_file('audio.wav')

# Duration in milliseconds
duration_ms = len(audio)
print(f"Duration: {duration_ms} ms ({duration_ms / 1000:.2f} seconds)")

# Audio properties
print(f"Channels: {audio.channels}")              # 1 for mono, 2 for stereo
print(f"Sample width: {audio.sample_width} bytes") # 2 for 16-bit
print(f"Frame rate: {audio.frame_rate} Hz")         # e.g., 44100
print(f"Loudness: {audio.dBFS:.2f} dBFS")          # average loudness
print(f"Max dBFS: {audio.max_dBFS:.2f} dBFS")      # peak amplitude
print(f"RMS: {audio.rms}")                          # root mean square level
print(f"Frame count: {audio.frame_count()}")
```

---

## Slicing and Concatenation

```python
from pydub import AudioSegment

audio = AudioSegment.from_file('audio.wav')

# Slice using millisecond indexing
first_5_seconds = audio[:5000]
last_3_seconds = audio[-3000:]
middle = audio[5000:15000]          # from 5s to 15s

# Concatenation with the + operator
combined = first_5_seconds + last_3_seconds

# Repeat audio
repeated = audio * 3                # repeat 3 times

# Build a sequence from multiple files
playlist = AudioSegment.empty()
for track in ['track1.wav', 'track2.wav', 'track3.wav']:
    playlist += AudioSegment.from_file(track)

# Insert silence between segments
silence = AudioSegment.silent(duration=1000)   # 1 second of silence
with_pauses = AudioSegment.empty()
segments = [audio[:5000], audio[5000:10000], audio[10000:15000]]
for i, seg in enumerate(segments):
    with_pauses += seg
    if i < len(segments) - 1:
        with_pauses += silence

# Helper for timestamp conversion
def time_to_ms(minutes, seconds):
    """Convert minutes and seconds to milliseconds."""
    return (minutes * 60 + seconds) * 1000

chorus = audio[time_to_ms(1, 30):time_to_ms(2, 15)]
```

---

## Effects

```python
from pydub import AudioSegment
from pydub.effects import normalize, speedup, low_pass_filter, high_pass_filter

audio = AudioSegment.from_file('audio.wav')

# Fade in and fade out
faded = audio.fade_in(2000).fade_out(3000)      # 2s fade in, 3s fade out

# Cross-fade between two segments
segment1 = audio[:10000]
segment2 = audio[10000:20000]
crossfaded = segment1.append(segment2, crossfade=1500)  # 1.5-second crossfade

# Normalize: adjust volume so peak is at 0 dBFS
normalized = normalize(audio)
normalized_hr = normalize(audio, headroom=3.0)   # peak at -3 dBFS

# Speed up (increases tempo, no pitch correction)
faster = speedup(audio, playback_speed=1.5)

# Reverse
reversed_audio = audio.reverse()

# Filters
low_passed = low_pass_filter(audio, cutoff=3000)     # cut above 3 kHz
high_passed = high_pass_filter(audio, cutoff=300)     # cut below 300 Hz

# Chain multiple effects
processed = audio.fade_in(1000).fade_out(2000)
processed = normalize(processed, headroom=1.0)
processed = low_pass_filter(processed, cutoff=8000)
```

---

## Volume Adjustment

```python
from pydub import AudioSegment

audio = AudioSegment.from_file('audio.wav')

# Increase/decrease volume with + and - operators (in dB)
louder = audio + 6                    # increase by 6 dB
quieter = audio - 10                  # decrease by 10 dB

# Apply gain using the method
gained = audio.apply_gain(3.5)        # apply 3.5 dB gain

# Set volume to a specific dBFS level
def set_loudness(audio_segment, target_dbfs):
    """Adjust audio to a target loudness level."""
    change = target_dbfs - audio_segment.dBFS
    return audio_segment.apply_gain(change)

normalized_to_minus20 = set_loudness(audio, -20.0)

# Volume envelope with fade at specific points
segment = audio[:10000]
segment = segment.fade(from_gain=0, to_gain=-20, start=0, end=3000)
segment = segment.fade(from_gain=-20, to_gain=0, start=7000, end=10000)
```

---

## Working with Silence

```python
from pydub import AudioSegment
from pydub.silence import detect_silence, detect_nonsilent, split_on_silence

audio = AudioSegment.from_file('speech.wav')

# Create silence
silence = AudioSegment.silent(duration=1000, frame_rate=44100)

# Detect silent sections - returns list of [start_ms, end_ms]
silent_ranges = detect_silence(audio, min_silence_len=500, silence_thresh=-40)
print(f"Found {len(silent_ranges)} silent sections")

# Detect non-silent sections
nonsilent_ranges = detect_nonsilent(audio, min_silence_len=500, silence_thresh=-40)

# Split audio on silence
chunks = split_on_silence(
    audio,
    min_silence_len=700,     # minimum silence duration (ms)
    silence_thresh=-40,      # silence threshold in dBFS
    keep_silence=200         # keep 200ms of silence at edges
)
print(f"Split into {len(chunks)} chunks")

# Export each chunk
for i, chunk in enumerate(chunks):
    chunk.export(f"chunk_{i:03d}.wav", format="wav")

# Add silence padding
padded = silence + audio + silence
```

---

## Export

```python
from pydub import AudioSegment

audio = AudioSegment.from_file('audio.wav')

# Export in different formats
audio.export('output.wav', format='wav')
audio.export('output.mp3', format='mp3', bitrate='192k')
audio.export('output.ogg', format='ogg')
audio.export('output.flac', format='flac')

# Export with metadata tags
audio.export(
    'output_tagged.mp3', format='mp3', bitrate='320k',
    tags={'title': 'My Song', 'artist': 'Artist Name', 'album': 'Album Name'}
)

# Export with album art
audio.export('output_art.mp3', format='mp3', cover='album_cover.jpg')

# Export with custom ffmpeg parameters
audio.export('output_custom.mp3', format='mp3',
             parameters=['-ar', '22050', '-ac', '1', '-ab', '128k'])

# Export to a file-like object
from io import BytesIO
buffer = BytesIO()
audio.export(buffer, format='wav')
buffer.seek(0)

# Batch export
for fmt in ['wav', 'mp3', 'ogg', 'flac']:
    audio.export(f'output.{fmt}', format=fmt)
```

---

## Overlay and Mixing

```python
from pydub import AudioSegment

music = AudioSegment.from_file('background_music.wav')
voice = AudioSegment.from_file('voiceover.wav')

# Basic overlay: mix two segments
mixed = music.overlay(voice)

# Overlay with position offset
mixed_offset = music.overlay(voice, position=5000)     # start at 5 seconds

# Overlay with gain adjustment during overlay
mixed_gain = music.overlay(voice, gain_during_overlay=-6)

# Loop the overlay to fill the duration
short_sfx = AudioSegment.from_file('click.wav')
with_sfx = music.overlay(short_sfx, loop=True)

# Mix multiple tracks
tracks = [
    AudioSegment.from_file('drums.wav') - 3,       # drums at -3 dB
    AudioSegment.from_file('bass.wav') - 2,        # bass at -2 dB
    AudioSegment.from_file('vocals.wav'),           # vocals at original level
]
mix = max(tracks, key=len)
for track in tracks:
    if track is not mix:
        mix = mix.overlay(track)

# Ducking: reduce background when voice is present
def duck_audio(background, foreground, duck_amount=10, position=0):
    """Reduce background volume where foreground plays."""
    before = background[:position]
    during = background[position:position + len(foreground)] - duck_amount
    after = background[position + len(foreground):]
    ducked = before + during + after
    return ducked.overlay(foreground, position=position)

ducked_mix = duck_audio(music, voice, duck_amount=12, position=3000)
```

---

## Channel Operations

```python
from pydub import AudioSegment

audio = AudioSegment.from_file('stereo.wav')

# Split stereo into mono channels
channels = audio.split_to_mono()
left_channel = channels[0]
right_channel = channels[1]

# Export individual channels
left_channel.export('left.wav', format='wav')
right_channel.export('right.wav', format='wav')

# Convert mono to stereo / stereo to mono
mono = AudioSegment.from_file('mono.wav')
stereo = mono.set_channels(2)         # duplicate to both channels
mono_from_stereo = audio.set_channels(1)  # downmix

# Create stereo from two mono files
left = AudioSegment.from_file('left_channel.wav')
right = AudioSegment.from_file('right_channel.wav')
stereo = AudioSegment.from_mono_audiosegments(left, right)
```

---

## Sample Rate and Sample Width Conversion

```python
from pydub import AudioSegment
import numpy as np

audio = AudioSegment.from_file('audio.wav')

# Change sample rate and sample width
audio_16k = audio.set_frame_rate(16000)       # resample to 16 kHz
audio_16bit = audio.set_sample_width(2)       # 16-bit

# Convert to NumPy array
samples = np.array(audio.get_array_of_samples())
if audio.channels == 2:
    samples = samples.reshape((-1, 2))        # reshape for stereo

# Convert NumPy array back to AudioSegment
audio_from_array = AudioSegment(
    data=samples.tobytes(),
    sample_width=audio.sample_width,
    frame_rate=audio.frame_rate,
    channels=audio.channels
)

# Standardize audio properties
def standardize_audio(audio_segment, rate=44100, width=2, channels=1):
    """Convert audio to standard properties."""
    return (audio_segment.set_frame_rate(rate)
            .set_sample_width(width)
            .set_channels(channels))

standardized = standardize_audio(audio)
```

---

## Generating Tones

```python
from pydub import AudioSegment
from pydub.generators import Sine, Square, WhiteNoise

# Generate waveforms
sine_440 = Sine(440).to_audio_segment(duration=2000, volume=-20)
square_wave = Square(440).to_audio_segment(duration=2000, volume=-20)
noise = WhiteNoise().to_audio_segment(duration=3000, volume=-30)

# Create a simple melody
notes = {'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
         'G4': 392.00, 'A4': 440.00, 'B4': 493.88, 'C5': 523.25}

melody = AudioSegment.empty()
for note_name in ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']:
    tone = Sine(notes[note_name]).to_audio_segment(duration=500, volume=-20)
    tone = tone.fade_in(50).fade_out(50)    # smooth transitions
    melody += tone
melody.export('melody.wav', format='wav')

# DTMF tone (dual-tone multi-frequency)
def dtmf_tone(freq1, freq2, duration=200, volume=-20):
    """Generate a DTMF tone from two frequencies."""
    tone1 = Sine(freq1).to_audio_segment(duration=duration, volume=volume)
    tone2 = Sine(freq2).to_audio_segment(duration=duration, volume=volume)
    return tone1.overlay(tone2)

dtmf_5 = dtmf_tone(770, 1336)  # DTMF digit '5'
```

---

## Practice Exercises

1. Load an MP3 file, extract the first 30 seconds, apply a 2-second fade in and 3-second fade out, normalize to -3 dBFS headroom, and export as both WAV and OGG.

2. Split a podcast recording on silence (threshold -35 dBFS, minimum silence 1 second) and export each segment as a separate numbered WAV file.

3. Create a simple audio mixer that overlays background music under a voice recording, ducking the music by 10 dB during voice sections.

4. Write a batch converter that converts all MP3 files in a directory to WAV at 16 kHz mono 16-bit.

5. Generate a 10-second audio file playing a C major scale using sine wave tones with smooth fade transitions.

6. Load a stereo file, apply different effects to each channel, and recombine into a new stereo file.

---

## Summary

pydub is a high-level Python library for audio manipulation that prioritizes simplicity and ease of use. It wraps ffmpeg for broad format support and provides an intuitive API with millisecond-precision slicing, dB-based volume control, built-in effects (fading, normalization, speed change), silence detection and splitting, audio overlay/mixing, and channel manipulation. While not designed for low-level signal processing, pydub excels at practical audio editing tasks and format conversion.

---

## Next Steps

- Explore integrating pydub with speech recognition libraries like Whisper
- Combine pydub with librosa for high-level editing followed by detailed analysis
- Build audio processing pipelines for podcast production or music editing
- Investigate using pydub in web applications for server-side audio processing

---

## Additional Resources

- [pydub GitHub Repository](https://github.com/jiaaro/pydub)
- [pydub API Documentation](https://github.com/jiaaro/pydub/blob/master/API.markdown)
- [ffmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Audio Processing in Python (Real Python)](https://realpython.com/playing-and-recording-sound-python/)
