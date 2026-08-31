#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feed_preview.py — 発信ビジュアルを「配信面の実表示サイズ」で見るためのコンタクトシート生成。

feed-visual-reviewer エージェント専用の入力生成ツール。
作った側の目（原寸100%）ではなく、読者の目（フィードでの縮小表示）で見るための1枚を作る。

使い方:
  # 静止画（サムネ/OGP/SNS投稿画像）
  python3 feed_preview.py still thumb_1200x630.png [-o out.png]

  # ショート動画（9:16のカバー・挿入画。複数可）
  python3 feed_preview.py short cover.png a1.png a2.png [-o out.png]

出力:
  - コンタクトシートPNG（1枚。エージェントはこれだけをReadする＝トークン節約）
  - 標準出力に機械判定レポート（遮蔽ゾーンの前景占有率など）

ゾーン座標は「目安」であり各PFのUI更新で動く。調整はこのファイル冒頭の定数で行う。
"""
import argparse, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ── 実表示幅の目安 ────────────────────────────────────────────
# 静止画: Xカード/LINE/ブログ一覧 ≒ 400px、モバイル一覧・グリッド ≒ 200px
STILL_WIDTHS = [(400, "400px  Xカード・LINE・ブログ一覧"),
                (200, "200px  モバイル一覧・グリッド")]
# 動画カバー: TikTokプロフィールグリッド/YouTubeショート棚/IGリールタブ ≒ 180px
SHORT_GRID_W = 180

# ── 9:16(1080×1920) におけるプラットフォームUIの遮蔽ゾーン（目安・比率で保持）──
# 実座標 = 比率 × 実寸。PFのUI更新時はここだけ直す。
UI_ZONES = [
    ("上部ステータス・ナビ",      0.000, 0.000, 1.000, 0.115),
    ("右アクションボタン列",      0.833, 0.469, 1.000, 0.885),
    ("下部ユーザー名・キャプション", 0.000, 0.792, 0.870, 0.958),
    ("最下部プログレス・タブ",     0.000, 0.958, 1.000, 1.000),
]
EDGE_THRESHOLD = 40  # 輝度勾配がこれを超える画素を「前景（文字・図形の輪郭）」とみなす
FG_LIMIT = 1.5   # 遮蔽ゾーン内の前景占有率がこれを超えたら警告(%)

BG = (238, 238, 234)
INK = (26, 32, 28)
WARN = (200, 40, 60)
OK = (31, 90, 58)


def _font(size):
    for p in ("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
              "/System/Library/Fonts/Hiragino Sans GB.ttc",
              "/System/Library/Fonts/Helvetica.ttc"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def _fg_ratio(img, box):
    """box(px)内の前景占有率(%)。

    背景色との差分では、グラデーション背景そのものを前景と誤検出する。
    文字・図形は必ず輪郭（局所コントラスト）を持ち、なめらかな背景は持たない。
    よって輝度の勾配強度で前景を数える。既存 check_subtitle_band.py の
    ベタ背景前提を、全面グラデ背景でも成立する形に置き換えたもの。
    """
    g = np.asarray(img.convert("L"), dtype=np.int16)
    h, w = g.shape
    x0, y0, x1, y1 = [int(v) for v in box]
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(w, x1), min(h, y1)
    if x1 - x0 < 3 or y1 - y0 < 3:
        return 0.0
    c = g[y0:y1, x0:x1]
    dx = np.abs(np.diff(c, axis=1))[:-1, :]
    dy = np.abs(np.diff(c, axis=0))[:, :-1]
    return float(((dx + dy) > EDGE_THRESHOLD).mean() * 100.0)


def _scaled(img, width):
    return img.resize((width, max(1, round(img.height * width / img.width))), Image.LANCZOS)


def build_still(paths, out):
    src = Image.open(paths[0]).convert("RGB")
    thumbs = [(_scaled(src, w), label) for w, label in STILL_WIDTHS]
    pad, gap, head = 28, 34, 40
    W = pad * 2 + sum(t.width for t, _ in thumbs) + gap * (len(thumbs) - 1)
    W = max(W, 640)
    H = pad * 2 + head + max(t.height for t, _ in thumbs) + 30
    sheet = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(sheet)
    d.text((pad, pad), "実表示サイズ（この縮尺で読めない文字は情報量ゼロ）",
           font=_font(21), fill=INK)
    x = pad
    top = pad + head
    for t, label in thumbs:
        sheet.paste(t, (x, top))
        d.rectangle([x, top, x + t.width - 1, top + t.height - 1], outline=(170, 175, 168))
        d.text((x, top + t.height + 7), label, font=_font(15), fill=(90, 100, 92))
        x += t.width + gap
    sheet.save(out)
    print(f"[still] {os.path.basename(paths[0])}  原寸 {src.width}×{src.height}"
          f"  比率 {src.width / src.height:.2f}:1")
    for w, label in STILL_WIDTHS:
        print(f"  - {label} に縮小して収録")
    return sheet


def build_short(paths, out):
    cols = []
    report = []
    for p in paths:
        img = Image.open(p).convert("RGB")
        W, H = img.size
        # (1) UI遮蔽ゾーンを重ねた原寸→表示用縮小
        over = img.copy()
        od = ImageDraw.Draw(over, "RGBA")
        rows = []
        for name, rx0, ry0, rx1, ry1 in UI_ZONES:
            box = (rx0 * W, ry0 * H, rx1 * W, ry1 * H)
            r = _fg_ratio(img, box)
            hit = r > FG_LIMIT
            od.rectangle(box, fill=(220, 40, 70, 70) if hit else (40, 140, 90, 45),
                         outline=(220, 40, 70) if hit else (40, 140, 90), width=4)
            rows.append((name, r, hit))
        col = _scaled(over, 300)
        grid = _scaled(img, SHORT_GRID_W)
        cols.append((os.path.basename(p), col, grid, rows))
        report.append((os.path.basename(p), W, H, rows))

    pad, gap, head = 26, 26, 40
    cw = 300
    ch = max(c.height for _, c, _, _ in cols)
    gh = max(g.height for _, _, g, _ in cols)
    W = pad * 2 + len(cols) * cw + gap * (len(cols) - 1)
    H = pad * 2 + head + ch + 26 + gh + 46
    sheet = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(sheet)
    d.text((pad, pad), "左上=PF UI遮蔽ゾーン（赤=要素が入っている） / 下段=グリッド表示サイズ",
           font=_font(20), fill=INK)
    x = pad
    for name, col, grid, rows in cols:
        sheet.paste(col, (x, pad + head))
        y2 = pad + head + ch + 26
        sheet.paste(grid, (x, y2))
        d.rectangle([x, y2, x + grid.width - 1, y2 + grid.height - 1], outline=(170, 175, 168))
        bad = any(h for _, _, h in rows)
        d.text((x, y2 + gh + 8), f"{name}  {'遮蔽あり' if bad else '遮蔽なし'}",
               font=_font(15), fill=WARN if bad else OK)
        x += cw + gap
    sheet.save(out)

    for name, W0, H0, rows in report:
        print(f"[short] {name}  {W0}×{H0}  比率 {W0/H0:.3f}"
              f"{'  ⚠比率が9:16(0.5625)から外れる' if abs(W0/H0 - 0.5625) > 0.01 else ''}")
        for zname, r, hit in rows:
            print(f"    {'⚠FAIL' if hit else '  ok '}  {zname}: 前景 {r:.1f}%（上限 {FG_LIMIT}%）")
    return sheet


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["still", "short"])
    ap.add_argument("images", nargs="+")
    ap.add_argument("-o", "--out", default=None)
    a = ap.parse_args()
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.images[0])),
                                f"_feedcheck_{a.mode}.png")
    (build_still if a.mode == "still" else build_short)(a.images, out)
    print(f"\n→ {out}")


if __name__ == "__main__":
    sys.exit(main())
