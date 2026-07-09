# AIくさかわ Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** テキスト（台本）を入力すると、イラストキャラ「AIくさかわ」が草川本人の声クローンで話す投稿可能なショート動画（9:16・60秒以内・字幕・AI明記付き）を全自動生成するローカルパイプラインを構築する。

**Architecture:** ElevenLabs APIで音声＋文字タイムスタンプを取得し、タイムスタンプから字幕(ASS)を、音声RMS解析から口パク（口3態PNGの切替タイムライン）を導出し、ffmpeg 1コマンドで合成する。ElevenLabs未登録でも動く開発モード（macOS `say`音声＋等間隔タイムスタンプ）を最初から備え、キャラ実画像が届く前は仮キャラ（HTML/CSS製）でE2Eを通す。

**Tech Stack:** Python 3.9（numpy 2.0.2 / requests 2.32.5 / 標準unittest）、ffmpeg（/usr/local/bin）、Chrome headless（HTML/CSS→PNG）、ElevenLabs API（eleven_multilingual_v2・with-timestamps）。

## Global Constraints

- 出力動画: 9:16・1080×1920・30fps・60秒以内・H.264/AAC・`format=yuv420p`
- 字幕帯: y1240〜1460 に収める（既存正本ルール。ASSは PlayResY=1920 / Alignment=2 / MarginV=460）
- 草川カラー: `#c7ff4a`（ライム）/ `#1f5a3a` / `#0f3d27`（深緑）/ `#f3efe4`（生成り）
- AI明記: 冒頭1.5秒に明記カード表示＋常時小ラベル（base画像に焼き込み）。音声・字幕・口パクはすべて1.5秒オフセット
- 発信物に絵文字を使わない（feedback_no_emoji_ai_smell）。テンプレ内テキストも同様
- パスはすべて絶対パス（cwd依存禁止）。生成物は `~/outputs/ai-kusakawa/`、コードは `~/.claude/scripts/ai-kusakawa/`
- APIキー: `~/.config/elevenlabs/api_key`、ボイスID: `~/.config/elevenlabs/voice_id`（各1行テキスト）
- `~/.claude` はgitリポジトリではない: git commit工程なし。全タスク完了後にclaude-configバックアップを案内する
- テストは `python3 -m unittest` で実行（pytest不使用）
- Python追加パッケージのインストール禁止（numpy/requestsのみで実装）

## File Structure

```
~/.claude/scripts/ai-kusakawa/
├── docs/                      # 設計書・計画書・手順書
│   ├── 2026-07-09-ai-kusakawa-design.md   （既存）
│   ├── plans/2026-07-09-ai-kusakawa.md    （本書）
│   ├── SETUP_ELEVENLABS.md    # Task 9: 草川手番ガイド
│   └── platform_ai_labels.md  # Task 8: PF別AIラベルON手順書
├── engine/
│   ├── __init__.py
│   ├── config.py              # Task 1: 定数（解像度・色・座標・パス）
│   ├── tts.py                 # Task 2: ElevenLabs／devモード音声生成
│   ├── subtitles.py           # Task 3: タイムスタンプ→ASS字幕
│   ├── lipsync.py             # Task 4: RMS解析→口状態タイムライン
│   └── compose.py             # Task 5: ffmpeg合成
├── generate.py                # Task 7: CLIパイプライン（入口）
├── assets/
│   ├── templates/             # Task 6: HTML/CSS（背景・introカード・仮キャラ）
│   ├── rendered/              # Task 6: Chrome headlessで出力したPNG
│   └── character/
│       └── prompt_cards.md    # Task 8: nano-bananaキャラ生成カード
└── tests/
    ├── __init__.py
    ├── test_subtitles.py
    ├── test_lipsync.py
    ├── test_compose.py
    └── test_e2e_dev.py

~/.claude/skills/ai-kusakawa/SKILL.md   # Task 8: オーケストレータースキル
```

---

### Task 1: プロジェクト骨格と config.py

**Files:**
- Create: `~/.claude/scripts/ai-kusakawa/engine/__init__.py`（空）
- Create: `~/.claude/scripts/ai-kusakawa/tests/__init__.py`（空）
- Create: `~/.claude/scripts/ai-kusakawa/engine/config.py`

**Interfaces:**
- Produces: `config.W, H, FPS, INTRO_SEC, COLORS(dict), SUB_BAND(y1240,1460), MOUTH_POS(tuple), MOUTH_SIZE(tuple), ASSETS_DIR, RENDERED_DIR, OUTPUT_ROOT, ELEVEN_KEY_PATH, ELEVEN_VOICE_PATH, FFMPEG, FFPROBE`（全タスクが参照）

- [ ] **Step 1: ディレクトリと空ファイル作成**

```bash
mkdir -p ~/.claude/scripts/ai-kusakawa/{engine,tests,assets/templates,assets/rendered,assets/character}
touch ~/.claude/scripts/ai-kusakawa/engine/__init__.py ~/.claude/scripts/ai-kusakawa/tests/__init__.py
```

- [ ] **Step 2: config.py を作成**

```python
"""AIくさかわ 合成エンジン共通設定。すべて絶対パス・cwd非依存。"""
from pathlib import Path

W, H, FPS = 1080, 1920, 30
INTRO_SEC = 1.5          # 冒頭AI明記カード表示秒数（音声・字幕・口パクを全てこの分遅らせる）
MAX_DURATION = 60.0

COLORS = {
    "lime": "#c7ff4a",
    "green": "#1f5a3a",
    "deep": "#0f3d27",
    "cream": "#f3efe4",
}

# 字幕帯 y1240-1460（既存正本ルール）
SUB_BAND = (1240, 1460)
SUB_MARGIN_V = H - SUB_BAND[1]   # ASS MarginV=460（下端から字幕ベースラインまで）

# 口パクPNGの合成位置とサイズ（仮キャラ基準。実キャラ投入時にここだけ調整）
MOUTH_POS = (410, 760)           # base.png 上の左上座標
MOUTH_SIZE = (260, 170)

BASE_DIR = Path.home() / ".claude/scripts/ai-kusakawa"
ASSETS_DIR = BASE_DIR / "assets"
RENDERED_DIR = ASSETS_DIR / "rendered"
OUTPUT_ROOT = Path.home() / "outputs/ai-kusakawa"

ELEVEN_KEY_PATH = Path.home() / ".config/elevenlabs/api_key"
ELEVEN_VOICE_PATH = Path.home() / ".config/elevenlabs/voice_id"
ELEVEN_MODEL = "eleven_multilingual_v2"

FFMPEG = "/usr/local/bin/ffmpeg"
FFPROBE = "/usr/local/bin/ffprobe"
```

- [ ] **Step 3: import 検証**

Run: `python3 -c "import sys; sys.path.insert(0,'$HOME/.claude/scripts/ai-kusakawa'); from engine import config; print(config.SUB_MARGIN_V)"`
Expected: `460`

---

### Task 2: tts.py（ElevenLabs＋devモード音声生成）

**Files:**
- Create: `~/.claude/scripts/ai-kusakawa/engine/tts.py`
- Test: なし（純関数 `parse_alignment` はTask 3のテストと同居させず、本タスク内で inline 検証。ネットワーク層はE2Eで検証）

**Interfaces:**
- Consumes: `engine.config`
- Produces: `synthesize(text: str, out_dir: Path, dev: bool=False) -> dict`
  返り値: `{"mp3": Path, "chars": list[str], "starts": list[float], "ends": list[float], "duration": float}`
  （starts/ends はオフセット適用前の生タイムスタンプ。INTRO_SECの加算は下流の責務）

- [ ] **Step 1: tts.py を実装**

```python
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
```

- [ ] **Step 2: devモードで動作検証**

Run:
```bash
cd ~/.claude/scripts/ai-kusakawa && python3 -c "
from pathlib import Path
from engine.tts import synthesize
r = synthesize('こんにちは、AIくさかわです。テスト音声です。', Path.home()/'outputs/ai-kusakawa/_smoke', dev=True)
print(round(r['duration'],1), len(r['chars']), r['mp3'].exists())"
```
Expected: `3.0前後 22 True`（durationは環境で多少前後してよい。mp3が実在しchars数=22であること）

---

### Task 3: subtitles.py（タイムスタンプ→ASS字幕）

**Files:**
- Create: `~/.claude/scripts/ai-kusakawa/engine/subtitles.py`
- Test: `~/.claude/scripts/ai-kusakawa/tests/test_subtitles.py`

**Interfaces:**
- Consumes: `engine.config`、tts出力の `chars/starts/ends`
- Produces:
  - `chunk_phrases(chars, starts, ends, max_len=16) -> list[dict]` 各dict= `{"text": str, "start": float, "end": float}`
  - `build_ass(phrases, offset: float, out_path: Path) -> Path`（offset=INTRO_SECを加算して書き出す）

- [ ] **Step 1: 失敗するテストを書く**

```python
import sys, unittest, tempfile
from pathlib import Path
sys.path.insert(0, str(Path.home() / ".claude/scripts/ai-kusakawa"))
from engine.subtitles import chunk_phrases, build_ass


def _mk(text):
    """等間隔0.1秒/文字のダミータイムスタンプを生成"""
    chars = list(text)
    starts = [i * 0.1 for i in range(len(chars))]
    ends = [(i + 1) * 0.1 for i in range(len(chars))]
    return chars, starts, ends


class TestChunk(unittest.TestCase):
    def test_splits_on_punctuation(self):
        ph = chunk_phrases(*_mk("こんにちは。AIくさかわです。"))
        self.assertEqual([p["text"] for p in ph], ["こんにちは。", "AIくさかわです。"])
        self.assertAlmostEqual(ph[0]["start"], 0.0)
        self.assertAlmostEqual(ph[1]["start"], 0.6, places=5)

    def test_splits_long_phrase_at_max_len(self):
        ph = chunk_phrases(*_mk("あ" * 40))  # 句読点なし40文字
        self.assertTrue(all(len(p["text"]) <= 16 for p in ph))
        self.assertEqual(sum(len(p["text"]) for p in ph), 40)

    def test_timestamps_monotonic(self):
        ph = chunk_phrases(*_mk("市政を、動かす。声を、チカラに。"))
        for a, b in zip(ph, ph[1:]):
            self.assertLessEqual(a["end"], b["start"] + 1e-9)


class TestAss(unittest.TestCase):
    def test_ass_offset_and_band(self):
        ph = chunk_phrases(*_mk("こんにちは。"))
        with tempfile.TemporaryDirectory() as d:
            out = build_ass(ph, offset=1.5, out_path=Path(d) / "s.ass")
            body = out.read_text()
        self.assertIn("PlayResY: 1920", body)
        self.assertIn("MarginV", body)   # 字幕帯y1240-1460をMarginV=460で表現
        self.assertIn("0:00:01.50", body)  # offset反映


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 失敗を確認**

Run: `cd ~/.claude/scripts/ai-kusakawa && python3 -m unittest tests.test_subtitles -v`
Expected: FAIL（`ModuleNotFoundError: No module named 'engine.subtitles'`）

- [ ] **Step 3: subtitles.py を実装**

```python
"""文字タイムスタンプ → フレーズ分割 → ASS字幕（字幕帯y1240-1460）。"""
from pathlib import Path

from . import config

_BREAKS = "。、！？!?\n"


def chunk_phrases(chars, starts, ends, max_len=16):
    phrases, buf, t0 = [], "", None
    for ch, s, e in zip(chars, starts, ends):
        if ch == "\n" and not buf:
            continue
        if t0 is None:
            t0 = s
        buf += ch if ch != "\n" else ""
        if ch in _BREAKS or len(buf) >= max_len:
            if buf:
                phrases.append({"text": buf, "start": t0, "end": e})
            buf, t0 = "", None
    if buf:
        phrases.append({"text": buf, "start": t0, "end": ends[-1]})
    return phrases


def _ts(sec: float) -> str:
    h = int(sec // 3600)
    m = int(sec % 3600 // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"


_HEADER = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {config.W}
PlayResY: {config.H}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV
Style: Main,Hiragino Sans,68,&H00FFFFFF,&H00273D0F,&HB0273D0F,1,3,10,0,2,60,60,{config.SUB_MARGIN_V}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def build_ass(phrases, offset: float, out_path: Path) -> Path:
    lines = [_HEADER]
    for p in phrases:
        lines.append(
            f"Dialogue: 0,{_ts(p['start'] + offset)},{_ts(p['end'] + offset)},"
            f"Main,,0,0,0,,{p['text']}\n")
    out_path.write_text("".join(lines))
    return out_path
```

（BackColour `&HB0273D0F` = 深緑 #0f3d27 の半透明帯。ABGR順に注意）

- [ ] **Step 4: テスト通過を確認**

Run: `cd ~/.claude/scripts/ai-kusakawa && python3 -m unittest tests.test_subtitles -v`
Expected: PASS（4件）

---

### Task 4: lipsync.py（音声RMS→口状態タイムライン）

**Files:**
- Create: `~/.claude/scripts/ai-kusakawa/engine/lipsync.py`
- Test: `~/.claude/scripts/ai-kusakawa/tests/test_lipsync.py`

**Interfaces:**
- Consumes: `engine.config`、tts出力のmp3
- Produces:
  - `mouth_states(mp3_path: Path) -> list[int]` 動画フレームごと（30fps）の口状態 0=閉/1=半開/2=開
  - `states_from_samples(samples: np.ndarray, sr: int) -> list[int]`（純関数・テスト対象）
  - `to_intervals(states: list[int], lead_silence: float) -> list[tuple[int, float]]`
    連続同状態をまとめ `(state, duration_sec)` の列に。先頭に `(0, lead_silence)` を挿入（INTRO_SEC用）

- [ ] **Step 1: 失敗するテストを書く**

```python
import sys, unittest
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path.home() / ".claude/scripts/ai-kusakawa"))
from engine.lipsync import states_from_samples, to_intervals
from engine import config

SR = 22050


class TestStates(unittest.TestCase):
    def test_silence_is_closed(self):
        s = states_from_samples(np.zeros(SR * 2, dtype=np.float32), SR)
        self.assertEqual(len(s), 2 * config.FPS)
        self.assertTrue(all(x == 0 for x in s))

    def test_loud_speech_opens_mouth(self):
        t = np.linspace(0, 2, SR * 2, dtype=np.float32)
        loud = np.sin(2 * np.pi * 220 * t).astype(np.float32)
        s = states_from_samples(loud, SR)
        self.assertGreater(sum(1 for x in s if x == 2), len(s) * 0.5)

    def test_alternating_produces_multiple_states(self):
        t = np.linspace(0, 1, SR, dtype=np.float32)
        tone = np.sin(2 * np.pi * 220 * t).astype(np.float32)
        sig = np.concatenate([tone, np.zeros(SR, dtype=np.float32),
                              tone * 0.3, np.zeros(SR, dtype=np.float32)])
        s = states_from_samples(sig, SR)
        self.assertEqual(sorted(set(s)), [0, 1, 2])


class TestIntervals(unittest.TestCase):
    def test_merge_and_lead(self):
        iv = to_intervals([0, 0, 2, 2, 2, 1], lead_silence=1.5)
        self.assertEqual(iv[0], (0, 1.5))
        self.assertEqual(iv[1], (0, 2 / config.FPS))
        self.assertEqual(iv[2], (2, 3 / config.FPS))
        self.assertEqual(iv[3], (1, 1 / config.FPS))
        self.assertAlmostEqual(sum(d for _, d in iv), 1.5 + 6 / config.FPS)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 失敗を確認**

Run: `cd ~/.claude/scripts/ai-kusakawa && python3 -m unittest tests.test_lipsync -v`
Expected: FAIL（ModuleNotFoundError）

- [ ] **Step 3: lipsync.py を実装**

```python
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
```

- [ ] **Step 4: テスト通過を確認**

Run: `cd ~/.claude/scripts/ai-kusakawa && python3 -m unittest tests.test_lipsync -v`
Expected: PASS（4件）

---

### Task 5: compose.py（ffmpeg合成）

**Files:**
- Create: `~/.claude/scripts/ai-kusakawa/engine/compose.py`
- Test: `~/.claude/scripts/ai-kusakawa/tests/test_compose.py`

**Interfaces:**
- Consumes: `engine.config`、`lipsync.to_intervals` の出力、`subtitles.build_ass` のASSファイル
- Produces:
  - `write_concat(intervals, mouth_pngs: dict[int, Path], out_txt: Path) -> Path`（ffmpeg concat demuxer形式）
  - `compose(base_png, intro_png, mouth_pngs, intervals, voice_mp3, ass_path, out_mp4, total_dur) -> Path`
- 合成方式: 口3態PNGを concat demuxer（duration指定）で小さな口ストリーム化→`fps=30`→base.png上に `overlay=MOUTH_POS`→introカードを `enable='lt(t,1.5)'` で全画面overlay→`ass=`字幕焼き込み→音声は `adelay` でINTRO_SEC遅延

- [ ] **Step 1: 失敗するテストを書く**

```python
import sys, unittest, tempfile
from pathlib import Path
sys.path.insert(0, str(Path.home() / ".claude/scripts/ai-kusakawa"))
from engine.compose import write_concat


class TestConcat(unittest.TestCase):
    def test_concat_format(self):
        pngs = {0: Path("/tmp/m0.png"), 1: Path("/tmp/m1.png"), 2: Path("/tmp/m2.png")}
        with tempfile.TemporaryDirectory() as d:
            out = write_concat([(0, 1.5), (2, 0.2), (0, 0.1)], pngs, Path(d) / "c.txt")
            body = out.read_text()
        lines = body.strip().splitlines()
        self.assertEqual(lines[0], "file '/tmp/m0.png'")
        self.assertEqual(lines[1], "duration 1.500000")
        self.assertEqual(lines[2], "file '/tmp/m2.png'")
        # concat demuxer仕様: 最終エントリはduration行の後にfile行を重ねて閉じる
        self.assertEqual(lines[-1], "file '/tmp/m0.png'")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 失敗を確認**

Run: `cd ~/.claude/scripts/ai-kusakawa && python3 -m unittest tests.test_compose -v`
Expected: FAIL（ModuleNotFoundError）

- [ ] **Step 3: compose.py を実装**

```python
"""ffmpeg 1コマンド合成: base + 口パク + introカード + ASS字幕 + 遅延音声 → mp4"""
import subprocess
from pathlib import Path

from . import config


def write_concat(intervals, mouth_pngs, out_txt: Path) -> Path:
    lines = []
    for state, dur in intervals:
        lines.append(f"file '{mouth_pngs[state]}'")
        lines.append(f"duration {dur:.6f}")
    # concat demuxer は最後のdurationを無視するため最終フレームのfile行を重ねる
    last_state = intervals[-1][0]
    lines.append(f"file '{mouth_pngs[last_state]}'")
    out_txt.write_text("\n".join(lines) + "\n")
    return out_txt


def compose(base_png: Path, intro_png: Path, mouth_pngs: dict, intervals,
            voice_mp3: Path, ass_path: Path, out_mp4: Path,
            total_dur: float) -> Path:
    concat_txt = out_mp4.parent / "mouth_concat.txt"
    write_concat(intervals, mouth_pngs, concat_txt)
    mx, my = config.MOUTH_POS
    mw, mh = config.MOUTH_SIZE
    delay_ms = int(config.INTRO_SEC * 1000)
    filter_complex = (
        f"[1:v]fps={config.FPS},scale={mw}:{mh}[mouth];"
        f"[0:v][mouth]overlay={mx}:{my}[v1];"
        f"[v1][3:v]overlay=0:0:enable='lt(t,{config.INTRO_SEC})'[v2];"
        f"[v2]ass={ass_path},format=yuv420p[v];"
        f"[2:a]adelay={delay_ms}|{delay_ms}[a]"
    )
    cmd = [
        config.FFMPEG, "-y",
        "-loop", "1", "-i", str(base_png),
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-i", str(voice_mp3),
        "-loop", "1", "-i", str(intro_png),
        "-filter_complex", filter_complex,
        "-map", "[v]", "-map", "[a]",
        "-t", f"{total_dur:.3f}",
        "-r", str(config.FPS),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        str(out_mp4),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_mp4
```

- [ ] **Step 4: テスト通過を確認**

Run: `cd ~/.claude/scripts/ai-kusakawa && python3 -m unittest tests.test_compose -v`
Expected: PASS（1件）
（composeの実走はTask 7のE2Eで検証する）

---

### Task 6: 背景テンプレ・introカード・仮キャラ（HTML/CSS→PNG）

**Files:**
- Create: `~/.claude/scripts/ai-kusakawa/assets/templates/base_green.html`（背景1: 深緑）
- Create: `~/.claude/scripts/ai-kusakawa/assets/templates/base_cream.html`（背景2: 生成り）
- Create: `~/.claude/scripts/ai-kusakawa/assets/templates/intro.html`（AI明記カード全画面）
- Create: `~/.claude/scripts/ai-kusakawa/assets/templates/mouth_{0,1,2}.html`（仮キャラ口3態）
- Create: `~/.claude/scripts/ai-kusakawa/assets/templates/render_all.sh`（Chrome headless一括レンダ）
- Output: `~/.claude/scripts/ai-kusakawa/assets/rendered/{base_green,base_cream,intro,mouth_0,mouth_1,mouth_2}.png`

**Interfaces:**
- Produces: Task 7 が参照するPNGファイル名（上記固定名）。実キャラ投入時は `mouth_*.png` と base の差し替えのみで済む契約。
- 仕様: base=1080×1920（キャラの顔・体・「AIくさかわ」常時小ラベルを焼き込み、口領域 `MOUTH_POS(410,760)`〜`MOUTH_SIZE(260,170)` は肌色ベタで空けておく）。mouth_*=260×170透過なし（肌色背景に口イラスト）。intro=1080×1920。

- [ ] **Step 1: base_green.html を作成**

```html
<meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { width:1080px; height:1920px; overflow:hidden;
         background:linear-gradient(170deg,#1f5a3a 0%,#0f3d27 70%);
         font-family:"Hiragino Sans",sans-serif; position:relative; }
  /* 仮キャラ: 実キャラ(nano-banana)投入までのプレースホルダー */
  .face { position:absolute; left:340px; top:520px; width:400px; height:400px;
          border-radius:50%; background:#f7d7b8; }
  .hair { position:absolute; left:320px; top:470px; width:440px; height:200px;
          border-radius:220px 220px 0 0; background:#2b2b2b; }
  .eye  { position:absolute; top:660px; width:38px; height:52px;
          border-radius:50%; background:#222; }
  .eye.l { left:440px; } .eye.r { left:600px; }
  .body { position:absolute; left:290px; top:900px; width:500px; height:420px;
          border-radius:80px 80px 0 0; background:#243b8f; }
  .collar { position:absolute; left:500px; top:900px; width:80px; height:110px;
            background:#fff; clip-path:polygon(0 0,100% 0,50% 100%); }
  .badge { position:absolute; left:96px; top:96px; background:#c7ff4a;
           color:#0f3d27; font-size:40px; font-weight:800;
           padding:16px 36px; border-radius:999px; }
  .name { position:absolute; left:0; right:0; top:1500px; text-align:center;
          color:#f3efe4; font-size:52px; font-weight:800; letter-spacing:.1em; }
</style>
<div class="hair"></div><div class="face"></div>
<div class="eye l"></div><div class="eye r"></div>
<div class="body"></div><div class="collar"></div>
<div class="badge">AIくさかわ｜AI生成動画</div>
<div class="name">AIくさかわ</div>
```

- [ ] **Step 2: base_cream.html を作成**（background を `linear-gradient(170deg,#f3efe4,#e4e0cf)`、`.name` と `.badge` の配色反転: badge背景 `#1f5a3a`・文字 `#c7ff4a`、name文字 `#0f3d27`。他はbase_greenと同一）

base_green.html をコピーして該当3箇所のみ変更する。

- [ ] **Step 3: intro.html を作成**

```html
<meta charset="utf-8">
<style>
  * { margin:0; padding:0; }
  body { width:1080px; height:1920px; overflow:hidden; background:#0f3d27;
         font-family:"Hiragino Sans",sans-serif;
         display:flex; flex-direction:column; justify-content:center;
         align-items:center; gap:48px; }
  .t1 { color:#c7ff4a; font-size:96px; font-weight:900; letter-spacing:.08em; }
  .t2 { color:#f3efe4; font-size:44px; font-weight:600; }
  .bar { width:200px; height:10px; background:#c7ff4a; }
</style>
<div class="t1">AIくさかわ</div>
<div class="bar"></div>
<div class="t2">この動画はAIで生成しています</div>
<div class="t2">話し手: 草川たくや公認のAIキャラクター</div>
```

- [ ] **Step 4: mouth_0/1/2.html を作成**（口3態・260×170・肌色背景 `#f7d7b8` はbaseの顔と同色）

mouth_0.html（閉じ）:
```html
<meta charset="utf-8">
<style>* {margin:0} body{width:260px;height:170px;background:#f7d7b8;position:relative}
.m{position:absolute;left:60px;top:80px;width:140px;height:10px;border-radius:6px;background:#a0522d}</style>
<div class="m"></div>
```
mouth_1.html（半開き）: `.m` を `top:66px;height:44px;border-radius:50%/60%;background:#7a2f1d` に変更（他同一）。
mouth_2.html（開き）: `.m` を `top:52px;height:76px;border-radius:48%/55%;background:#5e1f12` に、さらに `box-shadow:inset 0 -18px 0 #d96a6a`（舌）を追加（他同一）。

- [ ] **Step 5: render_all.sh を作成して実行**

```bash
#!/bin/bash
# Chrome headless で templates/*.html → rendered/*.png を一括生成
set -euo pipefail
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DIR="$HOME/.claude/scripts/ai-kusakawa/assets"
render() { # $1=name $2=WxH
  "$CHROME" --headless --disable-gpu --screenshot="$DIR/rendered/$1.png" \
    --window-size="$2" --hide-scrollbars "file://$DIR/templates/$1.html"
}
render base_green 1080,1920
render base_cream 1080,1920
render intro      1080,1920
render mouth_0    260,170
render mouth_1    260,170
render mouth_2    260,170
echo done
```

Run: `chmod +x ~/.claude/scripts/ai-kusakawa/assets/templates/render_all.sh && ~/.claude/scripts/ai-kusakawa/assets/templates/render_all.sh`
Expected: `done`・rendered/ に6枚のPNG

- [ ] **Step 6: EYES-FIRST検証**

rendered/ の6枚をReadツールで実際に開いて確認する（既存ルール: PNGは必ず自分の目で見る）:
- base 2枚: キャラの顔・体が破綻していない・口領域(410,760)-(670,930)が肌色ベタで空いている・「AIくさかわ｜AI生成動画」ラベルが読める
- mouth 3枚: 口の開き具合が3段階で判別できる・背景色がbaseの顔色と一致
- intro: 文言4行が中央に収まり読める

ズレがあればHTMLの座標・配色を修正して再レンダ→再Read。

---

### Task 7: generate.py（CLIパイプライン＋E2E）

**Files:**
- Create: `~/.claude/scripts/ai-kusakawa/generate.py`
- Test: `~/.claude/scripts/ai-kusakawa/tests/test_e2e_dev.py`

**Interfaces:**
- Consumes: Task 2-6 の全成果物（`tts.synthesize` / `subtitles.chunk_phrases`・`build_ass` / `lipsync.mouth_states`・`to_intervals` / `compose.compose` / rendered PNG群）
- Produces: CLI `python3 generate.py <台本txt> [--dev] [--bg green|cream] [--out-dir DIR]`
  → `~/outputs/ai-kusakawa/<YYYY-MM-DD>_<slug>/final.mp4`（＋voice.mp3/alignment.json/subs.ass）

- [ ] **Step 1: generate.py を実装**

```python
#!/usr/bin/env python3
"""AIくさかわ 動画生成CLI。
usage: python3 generate.py 台本.txt [--dev] [--bg green|cream] [--out-dir DIR] [--slug NAME]
"""
import argparse
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine import compose, config, lipsync, subtitles, tts  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script", help="台本テキストファイル")
    ap.add_argument("--dev", action="store_true",
                    help="ElevenLabs未使用（say -v Kyoko で検証）")
    ap.add_argument("--bg", choices=["green", "cream"], default="green")
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--slug", default="ai-kusakawa")
    args = ap.parse_args()

    text = Path(args.script).read_text().strip()
    if not text:
        sys.exit("台本が空です")

    today = datetime.date.today().isoformat()
    out_dir = Path(args.out_dir) if args.out_dir else \
        config.OUTPUT_ROOT / f"{today}_{args.slug}"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("1/4 音声生成...")
    voice = tts.synthesize(text, out_dir, dev=args.dev)
    total = config.INTRO_SEC + voice["duration"] + 0.5
    if total > config.MAX_DURATION:
        sys.exit(f"NG: 合計{total:.1f}秒（上限{config.MAX_DURATION}秒）。台本を短くしてください")

    print("2/4 字幕生成...")
    phrases = subtitles.chunk_phrases(voice["chars"], voice["starts"], voice["ends"])
    ass = subtitles.build_ass(phrases, offset=config.INTRO_SEC,
                              out_path=out_dir / "subs.ass")

    print("3/4 口パク解析...")
    states = lipsync.mouth_states(voice["mp3"])
    intervals = lipsync.to_intervals(states, lead_silence=config.INTRO_SEC)

    print("4/4 動画合成...")
    r = config.RENDERED_DIR
    mouth_pngs = {i: r / f"mouth_{i}.png" for i in range(3)}
    out_mp4 = compose.compose(
        base_png=r / f"base_{args.bg}.png", intro_png=r / "intro.png",
        mouth_pngs=mouth_pngs, intervals=intervals,
        voice_mp3=voice["mp3"], ass_path=ass,
        out_mp4=out_dir / "final.mp4", total_dur=total)
    print(f"完成: {out_mp4}（{total:.1f}秒）")
    return out_mp4


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: E2Eテストを書く**

```python
import subprocess, sys, unittest
from pathlib import Path

BASE = Path.home() / ".claude/scripts/ai-kusakawa"
sys.path.insert(0, str(BASE))
from engine import config  # noqa: E402

OUT = Path.home() / "outputs/ai-kusakawa/_e2e_test"


class TestE2EDev(unittest.TestCase):
    def test_generates_valid_mp4(self):
        script = OUT / "script.txt"
        OUT.mkdir(parents=True, exist_ok=True)
        script.write_text("こんにちは、AIくさかわです。今日は亀山市のコミュニティバスの話をします。運賃は小中学生100円、高校生以上200円です。")
        subprocess.run(
            ["python3", str(BASE / "generate.py"), str(script),
             "--dev", "--out-dir", str(OUT)],
            check=True, capture_output=True, text=True)
        mp4 = OUT / "final.mp4"
        self.assertTrue(mp4.exists())
        probe = subprocess.run(
            [config.FFPROBE, "-v", "error", "-show_entries",
             "stream=codec_type,width,height:format=duration",
             "-of", "csv", str(mp4)],
            capture_output=True, text=True, check=True).stdout
        self.assertIn("video,1080,1920", probe)
        self.assertIn("audio", probe)
        dur = float(probe.strip().splitlines()[-1].split(",")[1])
        self.assertGreater(dur, config.INTRO_SEC + 3)   # intro+音声が入っている
        self.assertLess(dur, config.MAX_DURATION)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: E2E実行**

Run: `cd ~/.claude/scripts/ai-kusakawa && python3 -m unittest tests.test_e2e_dev -v`
Expected: PASS（1件・30秒前後かかる）

- [ ] **Step 4: 全テスト一括＋目視確認**

Run: `cd ~/.claude/scripts/ai-kusakawa && python3 -m unittest discover tests -v && open ~/outputs/ai-kusakawa/_e2e_test/final.mp4`
Expected: 全PASS。動画をQuickTimeで再生し、①intro1.5秒→キャラ登場②口パクが音声に同期③字幕が帯内に表示④音ズレなし、を確認。ズレがあれば `MOUTH_POS`／字幕スタイル／しきい値を調整。

---

### Task 8: nano-bananaキャラプロンプトカード＋SKILL.md＋PFラベル手順書

**Files:**
- Create: `~/.claude/scripts/ai-kusakawa/assets/character/prompt_cards.md`
- Create: `~/.claude/skills/ai-kusakawa/SKILL.md`
- Create: `~/.claude/scripts/ai-kusakawa/docs/platform_ai_labels.md`

**Interfaces:**
- Consumes: photo-curator（参照写真選抜）、既存デザインシステムの明るいイラスト路線ルール
- Produces: 草川がGeminiで実行するプロンプトカード（出力契約: 透過なし全身1080×1920相当のbase差替画像1枚＋口3態260×170）／スキルトリガー「AIくさかわで動画」「AI動画作って」等

- [ ] **Step 1: photo-curator で参照写真を3枚選抜**

Agentツールで photo-curator を起動: 「AIくさかわのイラストキャラ化の参照素材として、正面顔がはっきり写った明るい表情の草川写真を3枚、JPEGパスで」。結果パスを prompt_cards.md に記載。

- [ ] **Step 2: prompt_cards.md を作成**

内容（日本語の指示＋英語プロンプト。design-studioのprompt_cards.md形式に合わせる）:
- カード1〜3: スタイル3案（A: 水彩タッチの温かい似顔絵 / B: フラットで現代的な政治系イラスト / C: 親しみ系マスコット調）。各カード共通要件: bright and friendly, watercolor/flat illustration, Japanese male in his 40s based on reference photo, suit with green tie, plain background `#1f5a3a`, mouth closed, front facing, waist-up, 9:16
- カード4: 選択スタイルで「同一人物・同一構図のまま口だけ半開き」「口だけ大きく開き」の差分2枚（image-to-image編集指示）
- 出力契約の明記: base用1枚（1080×1920・口閉じ・口領域に他要素をかぶせない）＋口3態のクロップ位置指示
- 投入手順: 生成PNGを `assets/character/` に置き「AIくさかわのキャラ画像を投入して」とClaudeに指示→Claudeが口領域クロップ・`MOUTH_POS/MOUTH_SIZE` 調整・base再構成・E2E再実行まで行う旨を記載

- [ ] **Step 3: platform_ai_labels.md を作成**

TikTok（投稿画面→その他のオプション→「AI生成コンテンツ」ラベルON）/ Instagram Reels（詳細設定→「AIラベルを追加」）/ YouTube Shorts（詳細設定→改変コンテンツ「はい」）/ X・Threads・Facebook・LINE（機能なし→キャプション文頭の「※この動画はAIが生成しています」で代替）の操作手順を箇条書きで記載。各PFのUI文言は変わりうるため「見つからない場合は投稿設定内のAI・改変コンテンツ項目を探す」と付記。

- [ ] **Step 4: SKILL.md を作成**

frontmatter（name: ai-kusakawa、description 400字以内厳守・トリガー「AIくさかわ」「AIくさかわで動画」「AI動画作って」「AIくさかわに話させて」等・NOT: 実写ショート動画→short-video-create、写真投稿→photo-post）。本文の工程:
1. 入力判定（テーマ1行→short-video-virality-architectで台本生成35〜45秒／台本持ち込み→そのまま）
2. 安全ゲート: content-fact-checker → content-risk-reviewer（skip禁止・災害/選挙期間/他者言及はHIGH扱い→本人判断）
3. 台本を草川に提示→承認後に `python3 ~/.claude/scripts/ai-kusakawa/generate.py 台本.txt`（本番はdevなし・ElevenLabs未設定時は--devでプレビューのみと明示）
4. 完成mp4をopenで再生確認→草川OK後に sns-content-creator で7PF投稿文（キャプション文頭に「※この動画はAIが生成しています」固定）
5. 保存: mp4→Drive `📱動画素材/`ミラー、📣SNS投稿管理DB(1bd98deb-)に1ページ（タイトル先頭にロボット・映画絵文字マーカー「AI動画」表記はDB管理用のみ可）
6. 投稿時のPF別AIラベルON→docs/platform_ai_labels.md参照を案内
末尾に「📌恒久ガードルール」節: AI明記4原則（冒頭カード・常時ラベル・キャプション文頭・実写誤認編集禁止）＋選挙運動用流用は個別リスクレビュー必須。

- [ ] **Step 5: スキル登録検証**

Run: `ls ~/.claude/skills/ai-kusakawa/SKILL.md && head -5 ~/.claude/skills/ai-kusakawa/SKILL.md`
Expected: ファイル実在・frontmatterに `name: ai-kusakawa`（実在検証はfeedback_agent_tools_frontmatter_breaksの教訓）

---

### Task 9: 声素材監査＋草川手番ガイド（SETUP_ELEVENLABS.md）

**Files:**
- Create: `~/.claude/scripts/ai-kusakawa/docs/SETUP_ELEVENLABS.md`

**Interfaces:**
- Consumes: `~/Archive/録音/` 等の既存録音（候補監査）
- Produces: 草川の手番チェックリスト（これが完了すると `--dev` なし本番生成が可能になる）

- [ ] **Step 1: 既存録音の候補監査**

```bash
for f in ~/Archive/録音/*.m4a; do
  d=$(/usr/local/bin/ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$f")
  echo "$(printf '%6.0f' "$d")秒  $f"
done | sort -rn | head -20
```

3〜10分の独り語り候補を洗い出し、上位候補の冒頭30秒をffmpegで切り出して聴取確認用に `~/outputs/ai-kusakawa/_voice_candidates/` へ書き出す（`ffmpeg -i 元 -t 30 -c copy 切り出し.m4a`）。複数話者・雑音入り（委員会録音等）は候補から除外し、結果をSETUP_ELEVENLABS.mdに記載。適格候補ゼロなら「新規録音が必要」と明記。

- [ ] **Step 2: SETUP_ELEVENLABS.md を作成**

記載内容:
1. **録音素材**（Step 1の監査結果を貼る）: 使える既存録音のパス、または新規録音手順（静かな室内・スマホ標準ボイスメモ・原稿を普段の演説調で3〜5分・BGMなし）
2. **アカウント作成**: elevenlabs.io → Starterプラン（$5/月・月30分生成≒40本）→ 品質不足時はCreator（$22/月・Professional Voice Clone）へ昇格
3. **Instant Voice Clone登録**: Voices → Add Voice → Instant Voice Clone → 音声アップロード → 名前「Kusakawa」→ 本人音声である旨の同意チェック
4. **キー設置**（コマンド付き）:
```bash
mkdir -p ~/.config/elevenlabs
echo 'APIキーをここに' > ~/.config/elevenlabs/api_key
echo 'ボイスIDをここに' > ~/.config/elevenlabs/voice_id
chmod 600 ~/.config/elevenlabs/*
```
（APIキー: Profile → API Keys、ボイスID: Voices → Kusakawa → ID copy）
5. **本番テスト**: 「AIくさかわでテスト動画作って」とClaudeに言う→devなし生成→本人が声品質を確認

- [ ] **Step 3: 完了報告と手番提示**

草川に提示: ①手番2つ（ElevenLabs設定=SETUP_ELEVENLABS.md／キャラ生成=prompt_cards.md）②devモード試作動画の場所③claude-configバックアップの実行推奨。memory `project_ai_kusakawa.md` の状況欄を「実装完了・草川手番待ち（声=ElevenLabs／キャラ=nano-banana）」に更新し、MEMORY.mdの束ね行も同期。

---

## Self-Review 結果

- **Spec coverage**: 設計書§1パイプライン=Task 2-5,7,8／§2初期構築=Task 6,8,9／§3合成エンジン仕様=Task 2-5／§4 AI明記ルール=Task 6(intro/badge焼き込み)+Task 8(SKILL.mdガードルール節)／§5コスト・初回テスト=Task 9／§6スコープ外=どのタスクにも含めていない。ギャップなし。
- **Placeholder scan**: コード必須ステップは全て完全コード掲載。Task 6 Step 2・Task 8 Step 2-4は差分・目次指定型だが変更箇所と文言を具体指定済み。
- **Type consistency**: `synthesize`→`chars/starts/ends`→`chunk_phrases`／`mouth_states`→`to_intervals`→`compose(intervals=...)`／PNG固定名（base_green/base_cream/intro/mouth_0..2）をTask 6-7で一致確認済み。`config.INTRO_SEC` のオフセットは字幕(build_ass offset)・口パク(lead_silence)・音声(adelay)の3系統で一貫。
