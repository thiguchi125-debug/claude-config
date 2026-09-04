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

# --- 判型ごとの規範（2026-09-04 追加）---------------------------------------
# 2026-09-04まで全判型を 9:16（1080x1920・ショート動画の挿入画像）として判定していた。
# そのため 16:9 のアイキャッチに、字幕セーフ帯（y1240-1460）と暗緑ベタ面25%という
# ショート動画専用の規則が当たり、通らないか、通っても意味がない状態だった。
# 16:9 の数値の出どころ＝サムネ正本 design_system/references/thumbnail/_karte.md
#   「メイン1行 原寸で最低100px（1600×900では約133px以上を推奨）、副1行 最低56px」
#   「下端12%に文字を置かない」「安全域＝中央800×800」
# ※Phase2で specs.json に集約する。ここが暫定の単一ソース。
SPECS = {
    "9:16": dict(name="ショート動画 挿入画像 1080x1920",
                 h1_min=MIN_H1, h1_want=WANT_H1, big_min=MIN_BIGNUM,
                 support_min=MIN_SUPPORT, note_min=MIN_NOTE,
                 band_end=BAND_END, band_from=1200,
                 darkgreen_max=DARKGREEN_MAX),
    "16:9": dict(name="アイキャッチ/OGP 1600x900",
                 h1_min=100, h1_want=133, big_min=100,
                 support_min=56, note_min=MIN_NOTE,
                 bottom_notext=0.12,     # 下端12%に文字を置かない（_karte.md）
                 darkgreen_max=None),    # ベタ面の制限はショート動画専用
    "1:1":  dict(name="SNS正方形",
                 h1_min=100, h1_want=120, big_min=100,
                 support_min=56, note_min=MIN_NOTE,
                 bottom_notext=0.10,
                 darkgreen_max=None),
}


def canvas_from_argv(argv):
    """--canvas 1600x900 / --format 16:9 を拾って (判型キー, W, H) を返す。既定は9:16。"""
    w = h = None
    fmt = None
    i = 0
    while i < len(argv):
        if argv[i] == "--canvas" and i + 1 < len(argv):
            try:
                w, h = (int(x) for x in argv[i + 1].lower().split("x"))
            except Exception:
                sys.exit("--canvas は 1600x900 の形式で指定してください")
            del argv[i:i + 2]; continue
        if argv[i] == "--format" and i + 1 < len(argv):
            fmt = argv[i + 1]
            del argv[i:i + 2]; continue
        i += 1
    if fmt is None:
        if w and h:
            r = w / h
            fmt = "16:9" if r > 1.25 else ("9:16" if r < 0.8 else "1:1")
        else:
            fmt = "9:16"
    if fmt not in SPECS:
        sys.exit(f"未知の判型 {fmt}（{'/'.join(SPECS)} のいずれか）")
    if not (w and h):
        w, h = (1080, 1920) if fmt == "9:16" else ((1600, 900) if fmt == "16:9" else (1080, 1080))
    return fmt, w, h

def sizes(css, prop):
    return [float(x) for x in re.findall(prop + r"\s*:\s*([\d.]+)px", css)]

def check_html(path, spec, H):
    s = open(path, encoding="utf-8").read()
    css = s[:s.index("</style>")] if "</style>" in s else s
    out = []
    fs = sorted(set(sizes(css, "font-size")))
    if not fs:
        return [(False, "font-size が読めない")]
    biggest = max(fs)
    smallest = min(fs)
    out.append((biggest >= spec["big_min"], f"最大文字 {biggest:.0f}px（主要情報の下限{spec['big_min']}px）"))
    out.append((smallest >= spec["note_min"], f"最小文字 {smallest:.0f}px（注記の下限{spec['note_min']}px）"))
    # 56px未満の本文級文字が何種類あるか（注記1〜2種は許容）
    small = [x for x in fs if spec["note_min"] <= x < spec["support_min"]]
    out.append((len(small) <= 2, f"補助文{spec['support_min']}px未満の字種 {len(small)}種 {small if small else ''}"))
    # 見出し
    h1 = sizes(css, "font-size")
    heads = [x for x in h1 if x >= spec["h1_min"]]
    if heads:
        out.append((True, f"見出し級 {max(heads):.0f}px"
                    + ("" if max(heads) >= spec["h1_want"] else f" ⚠ 推奨{spec['h1_want']}px以上を下回る")))
    else:
        out.append((False, f"見出し級（{spec['h1_min']}px以上）が無い"))
    # 行間
    # 大数字（100px以上）は詰めた行間が正（正本テンプレも .year 114px/lh1.06）。
    # 行間を見るのは 30〜79px の本文級のみ（80px以上は表示用数字とみなす）。
    rules = re.findall(r"\{([^}]*)\}", css)
    tight = []
    for r in rules:
        m = re.search(r"font-size\s*:\s*([\d.]+)px", r)
        l = re.search(r"line-height\s*:\s*([\d.]+)\s*[;}]?", r)
        if m and l and 30 <= float(m.group(1)) < 80 and float(l.group(1)) < MIN_LH_HEAD:
            tight.append(float(l.group(1)))
    out.append((not tight, f"行間 {MIN_LH_HEAD}未満 {len(tight)}件 {sorted(set(tight)) if tight else ''}"))
    # 下部ゾーンの開始位置
    tops = [float(x) for x in re.findall(r"top\s*:\s*(\d+)px", css)]
    if "band_end" in spec:
        below = [t for t in tops if t >= spec["band_from"]]
        if below:
            first = min(below)
            out.append((first >= spec["band_end"],
                        f"帯より下の最初の要素 y{first:.0f}（{spec['band_end']}以降であること）"))
    elif "bottom_notext" in spec:
        limit = H * (1 - spec["bottom_notext"])
        over = [t for t in tops if t >= limit]
        out.append((not over,
                    f"下端{spec['bottom_notext']*100:.0f}%（y{limit:.0f}以降）に置いた要素 {len(over)}件"
                    + (f" {sorted(over)}" if over else "")))
    return out

def check_png(path, spec):
    try:
        from PIL import Image
    except ImportError:
        return []
    if not os.path.exists(path):
        return []
    if spec.get("darkgreen_max") is None:
        return []   # 暗緑ベタ面の制限はショート動画（9:16）専用
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
    lim = spec["darkgreen_max"]
    return [(ratio <= lim,
             f"暗緑ベタ面 {ratio*100:.1f}%（許容{lim*100:.0f}%・深緑は文字/アクセント限定）")]

def main(argv):
    argv = list(argv)
    fmt, W, H = canvas_from_argv(argv)
    if not argv:
        print("usage: check_image_design.py [--canvas 1600x900|--format 16:9] <name.html> ...")
        return 1
    spec = SPECS[fmt]
    fail = 0
    print(f"判型: {fmt}（{spec['name']} / {W}x{H}）")
    for f in argv:
        print(f"\n== {os.path.basename(f)} ==")
        res = check_html(f, spec, H) + check_png(os.path.splitext(f)[0] + ".png", spec)
        for ok, msg in res:
            print(("  ✅ " if ok else "  🚨 ") + msg)
            if not ok: fail += 1
    print(f"\n-- 違反 {fail}件 --")
    return 1 if fail else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
