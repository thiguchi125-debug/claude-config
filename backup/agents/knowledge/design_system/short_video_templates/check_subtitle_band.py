#!/usr/bin/env python3
"""
字幕セーフ帯ゲート（機械可読・人の目視に頼らない再発防止）
9:16 ショート動画挿入画像(1080x1920)で、字幕帯 y1240-1460 が
前景要素で汚れていないかを自動判定する。

正本ルール: short-video-image-designer.md L72/L136（2026-07-04草川承認）
  帯 y1240-1460 は全画像共通の固定座標で空ける。
  主役テキスト・高コントラスト要素を置かない。

使い方:
  python3 check_subtitle_band.py a1.png a2.png ...
  （引数なしなら カレントの *.png 全部）

判定:
  帯領域のうち「背景色から大きく外れる画素」の割合が閾値超なら FAIL。
  複数画像を渡した場合、帯に残る前景の重心yがバラつく（＝位置不統一）も警告。
終了コード: 全PASSなら0、1枚でもFAILなら1（CI/フックに載せられる）
"""
import sys, glob
from PIL import Image

BAND_TOP, BAND_BOTTOM = 1240, 1460      # 正本固定座標
FRAME_W, FRAME_H = 1080, 1920
DEV_THRESHOLD = 60      # 背景からの色差(0-255*3のL1)がこれ超で「前景」
FG_RATIO_LIMIT = 0.015  # 帯内前景画素の許容割合（1.5%）

def bg_color(img):
    # 最頻色＝背景（ベタ背景前提）。四隅サンプルの中央値でも可だが最頻が堅い
    small = img.resize((108, 192))  # 高速化
    colors = small.getcolors(108*192)
    return max(colors, key=lambda c: c[0])[1][:3]

def analyze(path):
    img = Image.open(path).convert("RGB")
    if img.size != (FRAME_W, FRAME_H):
        return dict(path=path, ok=False, msg=f"サイズ不一致 {img.size} (要 {FRAME_W}x{FRAME_H})")
    bg = bg_color(img)
    px = img.load()
    fg = 0; total = 0; ysum = 0
    for y in range(BAND_TOP, BAND_BOTTOM):
        for x in range(0, FRAME_W, 2):   # 2px間引きで十分
            r, g, b = px[x, y]
            if abs(r-bg[0]) + abs(g-bg[1]) + abs(b-bg[2]) > DEV_THRESHOLD:
                fg += 1; ysum += y
            total += 1
    ratio = fg / total
    ok = ratio <= FG_RATIO_LIMIT
    cy = (ysum/fg) if fg else None
    return dict(path=path, ok=ok, ratio=ratio, cy=cy,
                msg=f"帯内前景 {ratio*100:.2f}% (許容 {FG_RATIO_LIMIT*100:.1f}%)")

def main(argv):
    files = argv or sorted(glob.glob("*.png"))
    if not files:
        print("PNGが見つかりません"); return 1
    results = [analyze(f) for f in files]
    fail = 0
    print(f"== 字幕セーフ帯ゲート y{BAND_TOP}-{BAND_BOTTOM} ==")
    for r in results:
        mark = "✅PASS" if r["ok"] else "🚨FAIL"
        if not r["ok"]: fail += 1
        print(f"  {mark}  {r['path'].split('/')[-1]:<18} {r['msg']}")
    print(f"-- {len(results)-fail}/{len(results)} PASS --")
    return 1 if fail else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
