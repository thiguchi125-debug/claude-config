---
name: feedback-rakusuru-back-rasterize
description: ラクスル入稿で裏面エラー「システムで問題が発生しました」発生時の対処 — 裏面のみ400dpi JPEG にラスタライズして表面と再結合
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4c9cf456-6e5b-4e8c-a8dc-174f77501a83
---

# ラクスル入稿時の裏面ラスタライズ手順

**ルール**: 草川リーフレットの**入稿は基本ラクスル**。Chrome `--print-to-pdf` で生成したPDFをラクスルに入稿すると、**裏面のみ「システムで問題が発生しました。時間をおいて再度お試しください。またはオペレーターチェック入稿をご利用ください。」エラー**が出る。これは自動チェッカーが複雑なベクター要素のパースに失敗した汎用エラー。**裏面だけを400dpi JPEGにラスタライズして表面と再結合**することで解消する。

**Why**: 2026年5月の選挙リーフレットv3でラクスル入稿時に発生。原因は裏面の複雑なベクター要素の多重重なり：
- `box-shadow:inset` の lime下線（複数のPillar title）
- `linear-gradient` 半透明 lime ハイライト
- `mix-blend-mode:multiply` の `.grain` レイヤー
- `transform:rotate(X) translateY(Y)` の写真複合変換 × 多数
- chips の box-shadow + 多重 background-color

表面は portrait + 大きな文字のみのシンプル構成なので通過。裏面のみ詰まる。**Preview.app での再エクスポートでは解消しない**（Apple PDF engine も同じ vector を保つため）。**Quartz Filter で完全ラスタ化も時間かかる**。最も確実なのは裏面だけPNG→JPEGに焼き付けて再結合する方法。

**How to apply**:
1. 入稿前に裏面ラスタライズ版を**必ず生成**してから入稿する（一度ベクター版で試して失敗してから対処、ではなく最初からラスタ版）
2. 表面はベクター維持（草川名・タイトル等の文字が美しい）
3. 裏面は400dpi JPEG（写真画質維持、印刷品質350dpi以上クリア）

## 実装スクリプト

ファイル名は `<案件名>_rakusuru.pdf` で別保存。元の `<案件名>.pdf` は編集用に維持。

```bash
DEST=~/.claude/agents/knowledge/kusagawa_archive/02_publications/leaflets/<案件dir>
SRC_PDF="$DEST/<案件名>.pdf"
OUT_PDF="$DEST/<案件名>_rakusuru.pdf"
mkdir -p "$DEST/_bake"

# 1) 裏面ページを 400dpi PNG にレンダリング
pdftoppm -png -r 400 -f 2 -l 2 "$SRC_PDF" "$DEST/_bake/back"

# 2) PNGを高品質JPEG化 → PDF埋め込み → 表面と結合
python3 <<'PY'
from PIL import Image
from pypdf import PdfWriter, PdfReader
import os

DEST = os.path.expanduser("<DEST絶対パス>")

# A4 at 400dpi = 約 3306x4678px
img = Image.open(f"{DEST}/_bake/back-2.png").convert("RGB")

# JPEG quality 95 + subsampling 0（chromaサブサンプリングOFFで色シャープネス維持）
back_jpg = f"{DEST}/_bake/back-hq.jpg"
img.save(back_jpg, "JPEG", quality=95, optimize=True, subsampling=0)

# PDFに埋め込み (resolution 400dpi でA4サイズ確保)
back_pdf = f"{DEST}/_bake/back-raster.pdf"
Image.open(back_jpg).save(back_pdf, "PDF", resolution=400.0)

# 表面ベクター + 裏面ラスタ で結合
src = PdfReader(f"{DEST}/<案件名>.pdf")
back = PdfReader(back_pdf)
writer = PdfWriter()
writer.add_page(src.pages[0])      # 表面（ベクター維持）
writer.add_page(back.pages[0])     # 裏面（ラスタ）
with open(f"{DEST}/<案件名>_rakusuru.pdf", "wb") as f:
    writer.write(f)
PY
```

## 必要なツール

- `pdftoppm` (poppler-utils, 通常Mac標準) — PDF → PNG レンダリング
- `python3` + `Pillow` + `pypdf` — JPEG化・PDF結合
  - `pypdf` 6.x: `pip install pypdf` （Macは標準で入っている可能性高い）
  - `Pillow`: `pip install pillow`

## 品質パラメータ（推奨値）

| パラメータ | 値 | 理由 |
|---|---|---|
| pdftoppm -r | 400 | ラクスル推奨350dpi以上クリア |
| JPEG quality | 95 | 印刷品質維持、ファイルサイズ 5-6MB に抑える |
| subsampling | 0 | chroma サブサンプリングOFFで色シャープネス維持 |
| resolution (PIL→PDF) | 400.0 | A4 ぴったりサイズに |

## トラブルシューティング

- **画質が甘い・ぼやけている**: `-r 400` を `-r 500` or `-r 600` に上げる、JPEG quality を 98 にする
- **ファイルサイズが大きすぎる**: JPEG quality を 90 に下げる（5.9MB → 3MB級）
- **画像化したくない要素がある**: 表面と同じ vector 維持で別ページ追加（部分ラスタ化は複雑）
- **表面も同じエラーが出る場合**: 表面もラスタ化（両ページラスタ）

## 編集サイクルの注意

1. HTML を編集
2. `--print-to-pdf` で `<案件名>.pdf` 再生成（**ベクター版・編集確認用**）
3. **入稿前に裏面ラスタライズ → `<案件名>_rakusuru.pdf` 再生成**（入稿用）
4. ラクスルに `_rakusuru.pdf` をアップロード

**入稿の度にスクリプト実行**。ベクター版PDFを直接入稿してはいけない。

Related: [[feedback-leaflet-design-principles]] [[feedback-pdf-image-optimization]] [[senkyo-leaflet-v3-2026]] [[reference-senkyo-leaflet-v3-files]]
