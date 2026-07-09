"""文字タイムスタンプ → フレーズ分割 → 字幕PNGシート（字幕帯y1240-1460）。

このMacのffmpegはass/subtitles/drawtextフィルタ非搭載のため、字幕は
「全フレーズを縦に積んだ透過PNGシートをChrome headlessで1回レンダ →
ffmpeg側でcrop＋overlay」方式で焼き込む（compose.pyが担当）。
"""
import html
import subprocess
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


def build_subs_html(phrases) -> str:
    """全フレーズを1080x220のブロックとして縦積みしたHTML（背景透過）。"""
    blocks = "".join(
        f'<div class="line"><span>{html.escape(p["text"])}</span></div>'
        for p in phrases)
    return f"""<meta charset="utf-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ width:{config.W}px; background:transparent;
         font-family:"Hiragino Sans",sans-serif; }}
  .line {{ width:{config.W}px; height:{config.SUB_BLOCK_H}px;
          display:flex; justify-content:center; align-items:center; }}
  .line span {{ max-width:960px; background:rgba(15,61,39,.85); color:#ffffff;
               font-size:56px; font-weight:800; line-height:1.3;
               padding:18px 42px; border-radius:16px; text-align:center; }}
</style>
{blocks}"""


def render_subs_sheet(phrases, out_dir: Path) -> Path:
    """subs.html→Chrome headless（透過背景）→subs.png（1080 x フレーズ数*220）"""
    out_dir.mkdir(parents=True, exist_ok=True)
    html_path = out_dir / "subs.html"
    png_path = out_dir / "subs.png"
    html_path.write_text(build_subs_html(phrases))
    height = max(1, len(phrases)) * config.SUB_BLOCK_H
    subprocess.run(
        [config.CHROME, "--headless", "--disable-gpu",
         f"--screenshot={png_path}",
         f"--window-size={config.W},{height}",
         "--default-background-color=00000000",
         "--hide-scrollbars", f"file://{html_path}"],
        check=True, capture_output=True)
    return png_path
