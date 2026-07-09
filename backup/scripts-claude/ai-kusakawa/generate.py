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
    subs_png = subtitles.render_subs_sheet(phrases, out_dir)
    subs_timings = [(p["start"], p["end"]) for p in phrases]

    print("3/4 口パク解析...")
    states = lipsync.mouth_states(voice["mp3"])
    intervals = lipsync.to_intervals(states, lead_silence=config.INTRO_SEC)

    print("4/4 動画合成...")
    r = config.RENDERED_DIR
    mouth_pngs = {i: r / f"mouth_{i}.png" for i in range(3)}
    out_mp4 = compose.compose(
        base_png=r / f"base_{args.bg}.png", intro_png=r / "intro.png",
        mouth_pngs=mouth_pngs, intervals=intervals,
        voice_mp3=voice["mp3"], subs_png=subs_png, subs_timings=subs_timings,
        out_mp4=out_dir / "final.mp4", total_dur=total)
    print(f"完成: {out_mp4}（{total:.1f}秒）")
    return out_mp4


if __name__ == "__main__":
    main()
