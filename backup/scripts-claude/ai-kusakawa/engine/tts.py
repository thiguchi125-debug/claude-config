"""音声生成。ElevenLabs with-timestamps API または devモード（macOS say）。"""
import base64
import json
import subprocess
from pathlib import Path

import requests

from . import config


def parse_alignment(alignment: dict):
    """ElevenLabs alignment オブジェクト → (chars, starts, ends)"""
    return (
        alignment["characters"],
        alignment["character_start_times_seconds"],
        alignment["character_end_times_seconds"],
    )


def _probe_duration(path: Path) -> float:
    out = subprocess.run(
        [config.FFPROBE, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def _synth_eleven(text: str, out_mp3: Path) -> dict:
    api_key = config.ELEVEN_KEY_PATH.read_text().strip()
    voice_id = config.ELEVEN_VOICE_PATH.read_text().strip()
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
    resp = requests.post(
        url,
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        json={"text": text, "model_id": config.ELEVEN_MODEL,
              "output_format": "mp3_44100_128"},
        timeout=120)
    resp.raise_for_status()
    data = resp.json()
    out_mp3.write_bytes(base64.b64decode(data["audio_base64"]))
    chars, starts, ends = parse_alignment(data["alignment"])
    return {"mp3": out_mp3, "chars": chars, "starts": starts, "ends": ends,
            "duration": _probe_duration(out_mp3)}


def _synth_dev(text: str, out_mp3: Path) -> dict:
    """ElevenLabs未登録でもパイプラインを通すための say -v Kyoko 音声＋等間隔タイムスタンプ。"""
    aiff = out_mp3.with_suffix(".aiff")
    subprocess.run(["say", "-v", "Kyoko", "-o", str(aiff), text], check=True)
    subprocess.run([config.FFMPEG, "-y", "-i", str(aiff),
                    "-codec:a", "libmp3lame", "-b:a", "192k", str(out_mp3)],
                   check=True, capture_output=True)
    aiff.unlink()
    dur = _probe_duration(out_mp3)
    chars = list(text)
    step = dur / max(len(chars), 1)
    starts = [i * step for i in range(len(chars))]
    ends = [(i + 1) * step for i in range(len(chars))]
    return {"mp3": out_mp3, "chars": chars, "starts": starts, "ends": ends,
            "duration": dur}


def synthesize(text: str, out_dir: Path, dev: bool = False) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_mp3 = out_dir / "voice.mp3"
    result = _synth_dev(text, out_mp3) if dev else _synth_eleven(text, out_mp3)
    (out_dir / "alignment.json").write_text(json.dumps(
        {"chars": result["chars"], "starts": result["starts"],
         "ends": result["ends"], "duration": result["duration"]},
        ensure_ascii=False, indent=1))
    return result
