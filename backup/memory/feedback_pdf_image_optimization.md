---
name: feedback-pdf-image-optimization
description: Chrome の --print-to-pdf は大画像を非圧縮埋め込みする問題。印刷向けは元画像を300dpi目安に事前リサイズして容量を削減する
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4c9cf456-6e5b-4e8c-a8dc-174f77501a83
---

# Chrome PDF 出力時の画像最適化必須

**ルール**: A4印刷向けHTMLをChrome headless で PDF 化する時、**元画像が4000px級だと非圧縮で埋め込まれて80MB級になる**。事前に `sips -s format jpeg -s formatOptions 90 -Z 1500` 等で印刷300dpi目安にリサイズしてからレンダリング。

**Why**: 2026年5月の選挙リーフレット v3 制作中、PDF が 80MB に膨らんだ。`pdfimages -list` で確認すると、4032×3024 ICC profile 付き画像が3つ「非圧縮 (image enc)」で埋め込まれており、それぞれ22-27MB を占めていた。Chromeの`--print-to-pdf`は画像品質オプションがなく、ICC profile 付きやファイルサイズが大きい画像を再エンコードしきれないことがある。

**How to apply**:
1. 印刷物制作前に、全画像を**「実表示mm × 11.81px/mm × 2倍」**を上限に sips でリサイズ
2. 例: 200×124px枠 (53×33mm) → 1500×900px JPEG quality 90
3. オリジナルは `assets/_orig/` にバックアップ
4. リサイズ後にPDF再生成 → 80MB → 10-15MB 級に削減

## 印刷mm別 推奨pixel（300dpi基準）

| 表示mm | 必要pixel | 推奨保存pixel (2倍余裕) |
|---|---|---|
| 50×30mm（活動実績サムネ） | 600×360 | **800×500 JPEG 85** |
| 60×40mm（chip用） | 720×480 | 1000×700 JPEG 88 |
| 90×60mm（中型写真） | 1080×720 | **1500×900 JPEG 90** |
| 150×100mm（メイン写真） | 1800×1200 | 2000×1400 JPEG 92 |
| portrait （A4縦長メイン） | 1500×2100 | 1500×2100 PNG/JPEG 95 |

## Bash 実装テンプレート

```bash
# バックアップ
mkdir -p assets/_orig
cp -n assets/*.jpg assets/_orig/

# 最適化（短辺1500px、JPEG 90）
for f in assets/main-photo.jpg; do
  sips -s format jpeg -s formatOptions 90 -Z 1500 "$f" --out "$f"
done

# Activity strip 小型サムネ（短辺 800、JPEG 85）
for f in assets/strip-{1..5}.jpg; do
  sips -s format jpeg -s formatOptions 85 -Z 800 "$f" --out "$f"
done
```

## 確認方法

```bash
# PDF内の重い画像TOP10
pdfimages -list <PDF> | awk '$1==2 && $3=="image"' | sort -k14 -n -r | head -10
```

「enc」列が `jpeg` ならOK、`image` (非圧縮) なら元画像が大きすぎる兆候。

Related: [[feedback-leaflet-design-principles]] [[senkyo-leaflet-v3-2026]]
