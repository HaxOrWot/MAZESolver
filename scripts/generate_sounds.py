import wave
import struct
import math
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOUNDS_DIR = os.path.join(PROJECT_ROOT, "assets", "sounds")


def generate_sine_wav(
    filepath: str,
    freq: float = 440.0,
    duration: float = 0.05,
    amplitude: float = 0.3,
    sample_rate: int = 44100,
) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    n_samples = int(sample_rate * duration)
    with wave.open(filepath, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for i in range(n_samples):
            t = i / sample_rate
            envelope = max(0.0, 1.0 - (i / n_samples))
            sample = amplitude * envelope * math.sin(2 * math.pi * freq * t)
            wf.writeframes(struct.pack("<h", int(sample * 32767)))


def generate_chord_wav(
    filepath: str,
    freqs=(523.25, 659.25, 783.99),
    duration: float = 0.6,
    amplitude: float = 0.25,
    sample_rate: int = 44100,
) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    n_samples = int(sample_rate * duration)
    with wave.open(filepath, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for i in range(n_samples):
            t = i / sample_rate
            envelope = max(0.0, 1.0 - (i / n_samples))
            val = sum(math.sin(2 * math.pi * f * t) for f in freqs) / len(freqs)
            sample = amplitude * envelope * val
            wf.writeframes(struct.pack("<h", int(sample * 32767)))


def main():
    tick_path = os.path.join(SOUNDS_DIR, "tick.wav")
    goal_path = os.path.join(SOUNDS_DIR, "goal.wav")

    generate_sine_wav(tick_path, freq=880.0, duration=0.03, amplitude=0.15)
    generate_chord_wav(goal_path, freqs=(523.25, 659.25, 783.99), duration=0.7, amplitude=0.35)
    print(f"Generated sound files at: {SOUNDS_DIR}")


if __name__ == "__main__":
    main()
