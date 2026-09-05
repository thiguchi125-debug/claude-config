---
name: reference-senkyo-leaflet-v3-files
description: 2026選挙リーフレットv3 のファイル場所と主要アセット — 再利用・参照時の入口
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4c9cf456-6e5b-4e8c-a8dc-174f77501a83
---

# 選挙リーフレット v3 参照ポインタ

**Root**: `~/.claude/agents/knowledge/kusagawa_archive/02_publications/leaflets/2026-05_senkyo_leaflet_v3/`

## 主要ファイル

- `index.html` — メインHTML（A4両面、JSX prototype を静的化したもの）
- `選挙リーフレット_v3.pdf` — Chrome headless で生成した編集確認用PDF（14MB級、A4 2ページ、ベクター）
- **`選挙リーフレット_v3_rakusuru.pdf`** — **ラクスル入稿用PDF（裏面のみ400dpi JPEG ラスタライズ済み、5.9MB）**。基本的にラクスル入稿はこちらを使う（手順＝`~/.claude/scripts/rakusuru_back_rasterize.py`）
- `assets/` — 画像群（最適化済み）
  - `portrait.png` — 表面メイン portrait
  - `qr-line.png` — LINE QR
  - `qr-instagram-clean.png` — Instagram QR（緑#1f5a3a・誤り訂正H・980×980px・URL: https://www.instagram.com/kusagawatakuya?igsh=dHlmNHU4Mmx3aGln）
  - `profile-family-blurred.jpg` — 草川家族写真（娘の顔は楕円マスクで薄めぼかし）
  - `okuwa-site.jpg` / `taiokaji-solar.jpg` / `skatepark-meeting.jpg` / `school-lunch-new.jpg` / `anoda-crosswalk-v2.jpg` / `water-turbid.jpg` — 政策・実績写真
  - `_orig/` — 元画像バックアップ（最適化前）
- `uploads/IMG_8382.jpeg` / `IMG_9789.jpeg` — Pillar 01 / Pillar 02 の写真
- `_review/` — preview PNG（PDF→PNG、レビュー検証用）

## 元の design bundle

- `/tmp/design_pkg2/untitled/` — claude.ai/design からダウンロードしたhandoff bundle
  - `project/選挙リーフレット v3.html` — JSX prototype（React + Babel standalone）
  - `project/components/velocity-front-v2.jsx` — 表面コンポーネント
  - `project/components/velocity-back.jsx` — 裏面コンポーネント
  - `chats/chat1.md` 〜 `chat4.md` — claude.ai/design でのやり取り履歴

## PDF再生成コマンド（編集確認用ベクター版）

```bash
cd ~/.claude/agents/knowledge/kusagawa_archive/02_publications/leaflets/2026-05_senkyo_leaflet_v3
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-sandbox \
  --no-pdf-header-footer \
  --virtual-time-budget=20000 \
  --run-all-compositor-stages-before-draw \
  --paper-width=8.27 --paper-height=11.69 \
  --print-to-pdf=選挙リーフレット_v3.pdf \
  "file://$(pwd)/index.html"
```

## ラクスル入稿用PDF生成コマンド（裏面ラスタライズ版）

詳細手順は `~/.claude/scripts/rakusuru_back_rasterize.py` 冒頭のdocstring参照。

```bash
cd ~/.claude/agents/knowledge/kusagawa_archive/02_publications/leaflets/2026-05_senkyo_leaflet_v3
mkdir -p _bake
pdftoppm -png -r 400 -f 2 -l 2 選挙リーフレット_v3.pdf _bake/back
python3 <<'PY'
from PIL import Image
from pypdf import PdfWriter, PdfReader
import os
D = os.getcwd()
img = Image.open(f"{D}/_bake/back-2.png").convert("RGB")
img.save(f"{D}/_bake/back-hq.jpg", "JPEG", quality=95, optimize=True, subsampling=0)
Image.open(f"{D}/_bake/back-hq.jpg").save(f"{D}/_bake/back-raster.pdf", "PDF", resolution=400.0)
src = PdfReader(f"{D}/選挙リーフレット_v3.pdf")
back = PdfReader(f"{D}/_bake/back-raster.pdf")
w = PdfWriter(); w.add_page(src.pages[0]); w.add_page(back.pages[0])
with open(f"{D}/選挙リーフレット_v3_rakusuru.pdf", "wb") as f: w.write(f)
PY
```

## PNG プレビュー再生成

```bash
pdftoppm -png -r 150 選挙リーフレット_v3.pdf _review/preview
```

## 関連メモリ

- 完成記録: [[senkyo-leaflet-v3-2026]]
- デザイン原則: [[feedback-leaflet-design-principles]]
- 切れ字ルール・box-shadow下線: design_system/foundations/rules.md §2（2026-09-05にメモリから吸収）
- PDF画像最適化: design_system/foundations/rules.md §3（画像リサイズ）
