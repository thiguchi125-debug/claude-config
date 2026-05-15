---
name: feedback-image-exif-processing
description: iPhone等で撮影した写真をHTML/PDFに埋め込む際、EXIF orientationの二重回転問題を防ぐ確実な処理手順
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c21b0b76-b034-484f-a916-65da438b4f5d
---

# 画像EXIF処理のテクニック

## ルール本体

**iPhoneや一眼デジカメで撮影した写真をHTML/CSSのprint-designerでPDFに埋め込む場合、必ず以下の処理を施してから使う**：

```bash
python3 -c "
from PIL import Image, ImageOps
img = Image.open('元画像.jpeg')
img = ImageOps.exif_transpose(img)  # EXIF orientationを画素に焼き込み
img.save('処理後.jpg', 'JPEG', quality=92, exif=b'')  # EXIFを完全strip
"
```

## Why（この feedback の根拠）

2026-05-15 太岡寺版v9生成時、太陽光発電施設の写真 `IMG_8577.jpeg`（4032×3024 横長保存・EXIF orientation 6=Right-top）を `sips -r 90` で時計回り90度回転した結果、**ブラウザ側でEXIFが残っていたため二重回転**が発生。草川から「太陽光パネルの写真は向きがおかしい」と指摘を受けた。

**原因**:
- iPhone写真は物理ピクセルでは横長保存され、EXIF orientationタグで「縦向き表示すべき」と指示される
- `sips -r 90` は物理ピクセルを回転するが、EXIFタグはそのまま残る
- Chrome headless等のレンダラーがEXIFを読んでさらに回転 → 結果として180度逆 or 90度逆になる
- macOS Preview / Read tool は内部で正規化して表示するため、目視確認では問題に気づきにくい

## How to apply

### 確実な処理（PIL + EXIF strip）
```bash
python3 -c "
from PIL import Image, ImageOps
img = Image.open('IMG_xxxx.jpeg')
img = ImageOps.exif_transpose(img)  # 正しい向きに正規化
print(f'処理後サイズ: {img.size}')   # 確認
img.save('output.jpg', 'JPEG', quality=92, exif=b'')  # EXIFゼロで保存
"
```

### 確認手順
```bash
# 物理ピクセルサイズが期待通りか確認
sips -g pixelHeight -g pixelWidth output.jpg

# Read tool で実際の向きを目視確認
# → Claude Code の Read tool は EXIF を読まないため、ピクセルそのままの向きで表示される
```

### NG（やってはいけない）
- `sips -r 90` 単独使用（EXIF残存で二重回転）
- ImageMagick `mogrify` でEXIF strip忘れ
- JPEGに EXIF=b'' 指定を忘れる
- 「macOS Previewで正しく見える」だけで判定する（PreviewはEXIFを読む）

### 関連ライブラリ
- macOS 標準 Python3 には PIL/Pillow 同梱（`pip3 install pillow` 不要なケース多い）
- 確認: `python3 -c "from PIL import Image; print(Image.__version__)"`

## 関連
- [[feedback-print-publication-checklist]] — 印刷物制作チェックリスト
- 実例: `~/.claude/agents/knowledge/kusagawa_archive/02_publications/reports/2026-05_太岡寺版_市政報告/IMG_8577.jpeg`（元画像）→ `taikoji_solar.jpg`（処理後）
