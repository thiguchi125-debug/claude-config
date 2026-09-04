#!/usr/bin/env python3
"""ラクスル入稿用: A4両面PDFの裏面(2ページ目)だけを400dpi JPEGにラスタライズし、表面ベクターと再結合する。

背景: Chrome --print-to-pdf のPDFをラクスルへ入稿すると裏面だけ「システムで問題が発生しました」エラー
（box-shadow inset / mix-blend-mode / 多重transform をラクスルの自動チェッカーがパースできない）。
Preview.app再エクスポートでは直らない。入稿は毎回このスクリプトで作った *_rakusuru.pdf を使う（ベクター版の直接入稿禁止）。
表面がエラーになる場合は --pages 1,2 で両面ラスタ化。

使い方: rakusuru_back_rasterize.py <案件名>.pdf [--dpi 400] [--quality 95] [--pages 2]
出力:   同ディレクトリに <案件名>_rakusuru.pdf（中間ファイルは _bake/）
品質:   dpi400(ラクスル推奨350以上)・quality95・subsampling=0(色シャープ維持)。ぼやける→--dpi 500〜600／大きすぎる→--quality 90
依存:   pdftoppm(poppler)・Pillow・pypdf
"""
import argparse, os, subprocess, sys
from PIL import Image
from pypdf import PdfReader, PdfWriter

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("--dpi", type=int, default=400)
ap.add_argument("--quality", type=int, default=95)
ap.add_argument("--pages", default="2", help="ラスタ化するページ番号(1始まり・カンマ区切り)")
a = ap.parse_args()

src = os.path.abspath(a.src)
d = os.path.dirname(src); base = os.path.splitext(os.path.basename(src))[0]
bake = os.path.join(d, "_bake"); os.makedirs(bake, exist_ok=True)
out = os.path.join(d, f"{base}_rakusuru.pdf")
raster = {int(p) for p in a.pages.split(",")}

reader = PdfReader(src)
writer = PdfWriter()
for i in range(len(reader.pages)):
    n = i + 1
    if n not in raster:
        writer.add_page(reader.pages[i]); continue
    prefix = os.path.join(bake, f"p{n}")
    subprocess.run(["pdftoppm", "-png", "-r", str(a.dpi), "-f", str(n), "-l", str(n), src, prefix], check=True)
    png = next(os.path.join(bake, f) for f in sorted(os.listdir(bake)) if f.startswith(f"p{n}") and f.endswith(".png"))
    jpg = f"{prefix}-hq.jpg"; pdf = f"{prefix}-raster.pdf"
    Image.open(png).convert("RGB").save(jpg, "JPEG", quality=a.quality, optimize=True, subsampling=0)
    Image.open(jpg).save(pdf, "PDF", resolution=float(a.dpi))
    writer.add_page(PdfReader(pdf).pages[0])
with open(out, "wb") as f:
    writer.write(f)
print(out, f"{os.path.getsize(out)/1e6:.1f}MB")
