#!/usr/bin/env python3
"""
ショート動画 挿入画像の確定デザイン仕様ゲート（機械可読）

check_subtitle_band.py が「字幕帯だけ」を見るのに対し、こちらは
[[feedback_short_video_insert_image_design_spec]]（2026-06-26 草川が6往復で確定）と
正本テンプレ ~/.claude/agents/knowledge/short_video_templates/insert_image_v1/
の実測値に対する適合を判定する。

2026-08-06 追加の理由:
  可読性フロア（最小72px/44px）を「要件」と誤解し、確定仕様（見出し100px+/lh1.36・
  補助56px・注記36px・暗緑ベタ面NG）を外した画像を5枚作った。
  帯ゲートがPASSしたため適合したと錯覚した。フロアは落第ラインであって合格ラインではない。

使い方:
  python3 check_image_design.py <name.html> [...]   # 同名 .png があれば配色も見る
終了コード: 全PASSなら0、1件でもFAILなら1
"""
import sys, re, os

# 正本テンプレ insert_image_v1/template_b_infocard.html の実測値を下限とする
MIN_KICKER   = 48    # ライムチップの見出しラベル
MIN_H1       = 100   # 見出し（memory仕様は120〜150／テンプレ実測100+nowrap）
WANT_H1      = 120   # ここを下回ったら警告
MIN_BIGNUM   = 80    # 主要情報（数値など）
MIN_SUPPORT  = 56    # 補助文
MIN_NOTE     = 36    # 注記・出典
MIN_LH_HEAD  = 1.30  # 見出しの行間（テンプレ1.36）
MIN_LH_BODY  = 1.45  # 本文の行間（テンプレ1.54）
BAND_END     = 1460  # 字幕帯の下端。下部ゾーンはここ以降
DARKGREEN_MAX = 0.25 # 暗緑ベタ面の許容面積比（「深緑は文字・アクセント限定」）

def sizes(css, prop):
    return [float(x) for x in re.findall(prop + r"\s*:\s*([\d.]+)px", css)]

def check_html(path):
    s = open(path, encoding="utf-8").read()
    css = s[:s.index("</style>")] if "</style>" in s else s
    out = []
    fs = sorted(set(sizes(css, "font-size")))
    if not fs:
        return [(False, "font-size が読めない")]
    biggest = max(fs)
    smallest = min(fs)
    out.append((biggest >= MIN_BIGNUM, f"最大文字 {biggest:.0f}px（主要情報の下限{MIN_BIGNUM}px）"))
    out.append((smallest >= MIN_NOTE, f"最小文字 {smallest:.0f}px（注記の下限{MIN_NOTE}px）"))
    # 56px未満の本文級文字が何種類あるか（注記1〜2種は許容）
    small = [x for x in fs if MIN_NOTE <= x < MIN_SUPPORT]
    out.append((len(small) <= 2, f"補助文56px未満の字種 {len(small)}種 {small if small else ''}"))
    # 見出し
    h1 = sizes(css, "font-size")
    heads = [x for x in h1 if x >= MIN_H1]
    if heads:
        out.append((True, f"見出し級 {max(heads):.0f}px"
                    + ("" if max(heads) >= WANT_H1 else f" ⚠ 仕様の推奨{WANT_H1}〜150pxを下回る")))
    else:
        out.append((False, f"見出し級（{MIN_H1}px以上）が無い"))
    # 行間
    # 大数字（100px以上）は詰めた行間が正（正本テンプレも .year 114px/lh1.06）。
    # 行間を見るのは 30〜99px の本文・見出し級のみ。
    rules = re.findall(r"\{([^}]*)\}", css)
    tight = []
    for r in rules:
        m = re.search(r"font-size\s*:\s*([\d.]+)px", r)
        l = re.search(r"line-height\s*:\s*([\d.]+)\s*[;}]?", r)
        if m and l and 30 <= float(m.group(1)) < 100 and float(l.group(1)) < MIN_LH_HEAD:
            tight.append(float(l.group(1)))
    out.append((not tight, f"行間 {MIN_LH_HEAD}未満 {len(tight)}件 {sorted(set(tight)) if tight else ''}"))
    # 下部ゾーンの開始位置
    tops = [float(x) for x in re.findall(r"top\s*:\s*(\d+)px", css)]
    below = [t for t in tops if t >= 1200]
    if below:
        first = min(below)
        out.append((first >= BAND_END, f"帯より下の最初の要素 y{first:.0f}（{BAND_END}以降であること）"))
    return out

def check_png(path):
    try:
        from PIL import Image
    except ImportError:
        return []
    if not os.path.exists(path):
        return []
    im = Image.open(path).convert("RGB")
    w, h = im.size
    dark = tot = 0
    for y in range(0, h, 4):
        for x in range(0, w, 4):
            r, g, b = im.getpixel((x, y))
            tot += 1
            # 深緑ベタ（#0f3d27 / #1f5a3a / #1b543a 近傍）
            if r < 70 and 40 < g < 110 and b < 85:
                dark += 1
    ratio = dark / tot if tot else 0
    return [(ratio <= DARKGREEN_MAX,
             f"暗緑ベタ面 {ratio*100:.1f}%（許容{DARKGREEN_MAX*100:.0f}%・深緑は文字/アクセント限定）")]

def main(argv):
    if not argv:
        print("usage: check_image_design.py <name.html> ..."); return 1
    fail = 0
    for f in argv:
        print(f"\n== {os.path.basename(f)} ==")
        res = check_html(f) + check_png(os.path.splitext(f)[0] + ".png")
        for ok, msg in res:
            print(("  ✅ " if ok else "  🚨 ") + msg)
            if not ok: fail += 1
    print(f"\n-- 違反 {fail}件 --")
    return 1 if fail else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
