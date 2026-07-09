"""音声RMS解析 → 30fpsの口状態列（0閉/1半開/2開） → 同状態インターバル列。"""
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

from . import config

_SR = 22050
_THRESH_HALF = 0.08   # 最大RMS比: これ未満=閉
_THRESH_OPEN = 0.40   # これ未満=半開、以上=開


def _decode_to_samples(mp3_path: Path):
    with tempfile.TemporaryDirectory() as d:
        wav = Path(d) / "a.wav"
        subprocess.run(
            [config.FFMPEG, "-y", "-i", str(mp3_path), "-ac", "1",
             "-ar", str(_SR), "-c:a", "pcm_s16le", str(wav)],
            check=True, capture_output=True)
        with wave.open(str(wav)) as w:
            raw = w.readframes(w.getnframes())
    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    return samples, _SR


def states_from_samples(samples: np.ndarray, sr: int):
    spf = sr // config.FPS                      # samples per video frame
    n_frames = max(1, len(samples) // spf)
    rms = np.array([
        float(np.sqrt(np.mean(samples[i * spf:(i + 1) * spf] ** 2)))
        for i in range(n_frames)])
    peak = rms.max()
    if peak < 1e-6:
        return [0] * n_frames
    ratio = rms / peak
    states = np.where(ratio < _THRESH_HALF, 0,
                      np.where(ratio < _THRESH_OPEN, 1, 2))
    # 3フレーム中央値でチラつきを平滑化
    if len(states) >= 3:
        sm = states.copy()
        sm[1:-1] = np.median(
            np.stack([states[:-2], states[1:-1], states[2:]]), axis=0)
        states = sm
    return [int(x) for x in states]


def mouth_states(mp3_path: Path):
    return states_from_samples(*_decode_to_samples(mp3_path))


def to_intervals(states, lead_silence: float):
    intervals = [(0, float(lead_silence))] if lead_silence > 0 else []
    i = 0
    while i < len(states):
        j = i
        while j < len(states) and states[j] == states[i]:
            j += 1
        intervals.append((states[i], (j - i) / config.FPS))
        i = j
    return intervals
