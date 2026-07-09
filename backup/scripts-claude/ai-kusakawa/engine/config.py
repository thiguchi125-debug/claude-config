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
SUB_MARGIN_V = H - SUB_BAND[1]   # 460（下端から字幕帯下端まで・参考値）
SUB_BLOCK_H = SUB_BAND[1] - SUB_BAND[0]   # 220: 字幕PNGシートの1フレーズ分の高さ

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 口パクPNGの合成位置とサイズ（仮キャラ基準。実キャラ投入時にここだけ調整）
MOUTH_POS = (440, 750)           # base.png 上の左上座標（仮キャラ顔円 中心540,720 r200 の内側に収める）
MOUTH_SIZE = (200, 130)

BASE_DIR = Path.home() / ".claude/scripts/ai-kusakawa"
ASSETS_DIR = BASE_DIR / "assets"
RENDERED_DIR = ASSETS_DIR / "rendered"
OUTPUT_ROOT = Path.home() / "outputs/ai-kusakawa"

ELEVEN_KEY_PATH = Path.home() / ".config/elevenlabs/api_key"
ELEVEN_VOICE_PATH = Path.home() / ".config/elevenlabs/voice_id"
ELEVEN_MODEL = "eleven_multilingual_v2"

FFMPEG = "/usr/local/bin/ffmpeg"
FFPROBE = "/usr/local/bin/ffprobe"
