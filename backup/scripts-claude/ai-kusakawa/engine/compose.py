"""ffmpeg 1コマンド合成: base + 口パク + introカード + 字幕PNGシート + 遅延音声 → mp4

字幕はASSフィルタ非搭載ffmpeg対応のため、subtitles.render_subs_sheet が作る
透過PNGシート（1080 x フレーズ数*220）を crop でフレーズ別に切り出し、
enable='between(t,start,end)' で字幕帯 y1240 に順次 overlay する。
"""
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


def subs_overlay_chain(n_phrases, timings, offset, in_label, sheet_label,
                       out_label):
    """字幕シートをn分割してoverlayするfilter_complex断片を組み立てる純関数。

    timings: [(start,end), ...] オフセット適用前秒。offset: INTRO_SEC。
    in_label: 字幕を重ねる映像ストリームのラベル（例 'v2'）。
    sheet_label: 字幕シート入力のラベル（例 '4:v'）。
    """
    if n_phrases == 0:
        return f"[{in_label}]null[{out_label}]"
    parts = [f"[{sheet_label}]format=rgba,split={n_phrases}"
             + "".join(f"[sh{i}]" for i in range(n_phrases))]
    for i in range(n_phrases):
        parts.append(
            f"[sh{i}]crop={config.W}:{config.SUB_BLOCK_H}:0:"
            f"{i * config.SUB_BLOCK_H}[s{i}]")
    cur = in_label
    for i, (s, e) in enumerate(timings):
        nxt = out_label if i == n_phrases - 1 else f"o{i}"
        parts.append(
            f"[{cur}][s{i}]overlay=0:{config.SUB_BAND[0]}:"
            f"enable='between(t,{s + offset:.3f},{e + offset:.3f})'[{nxt}]")
        cur = nxt
    return ";".join(parts)


def compose(base_png: Path, intro_png: Path, mouth_pngs: dict, intervals,
            voice_mp3: Path, subs_png: Path, subs_timings, out_mp4: Path,
            total_dur: float) -> Path:
    concat_txt = out_mp4.parent / "mouth_concat.txt"
    write_concat(intervals, mouth_pngs, concat_txt)
    mx, my = config.MOUTH_POS
    mw, mh = config.MOUTH_SIZE
    delay_ms = int(config.INTRO_SEC * 1000)
    subs_chain = subs_overlay_chain(
        len(subs_timings), subs_timings, config.INTRO_SEC,
        in_label="v2", sheet_label="4:v", out_label="vsub")
    filter_complex = (
        f"[1:v]fps={config.FPS},scale={mw}:{mh}[mouth];"
        f"[0:v][mouth]overlay={mx}:{my}[v1];"
        f"[v1][3:v]overlay=0:0:enable='lt(t,{config.INTRO_SEC})'[v2];"
        f"{subs_chain};"
        f"[vsub]format=yuv420p[v];"
        f"[2:a]adelay={delay_ms}|{delay_ms}[a]"
    )
    cmd = [
        config.FFMPEG, "-y",
        "-loop", "1", "-i", str(base_png),
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-i", str(voice_mp3),
        "-loop", "1", "-i", str(intro_png),
        "-loop", "1", "-i", str(subs_png),
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
