#!/bin/bash
# Canva資料テキスト化スクリプト
# 使い方:
#   ~/.claude/scripts/canva-import/canva_to_text.sh <PDF_PATH>
#   ~/.claude/scripts/canva-import/canva_to_text.sh --batch ~/Downloads/  (フォルダ一括)
#
# 出力先: ~/.claude/agents/knowledge/kusagawa_archive/canva/
#
# Canvaから「ダウンロード→PDF（標準）」でエクスポートしたPDFは
# テキストレイヤーがあるためpdftotextで完全抽出可能。
# 画像のみのPDFの場合は警告して手動OCR推奨。

OUT_DIR=~/.claude/agents/knowledge/kusagawa_archive/canva
mkdir -p "$OUT_DIR"

convert_one() {
  local pdf="$1"
  local base=$(basename "$pdf" .pdf | sed 's/[^a-zA-Z0-9一-龯ぁ-んァ-ヶー]/_/g')
  local out="$OUT_DIR/$(date +%Y-%m-%d)_canva_${base}.txt"
  
  pdftotext -layout "$pdf" "$out" 2>/dev/null
  
  if [ ! -s "$out" ]; then
    echo "❌ FAIL（空 = 画像PDFかも・OCR要）: $pdf"
    rm -f "$out"
    return 1
  fi
  
  local size=$(wc -c < "$out")
  if [ "$size" -lt 100 ]; then
    echo "⚠️  小（${size}B）= 画像PDFかも: $pdf"
    mv "$out" "$OUT_DIR/_low_${base}.txt"
    return 1
  fi
  
  # フロントマター付与
  local tmp="${out}.tmp"
  cat > "$tmp" << HEADER
---
source: Canva PDF export
src_path: $pdf
imported_at: $(date '+%Y-%m-%d %H:%M:%S')
char_count: $size
---

HEADER
  cat "$out" >> "$tmp"
  mv "$tmp" "$out"
  
  echo "✅ OK (${size}B): $base.txt"
}

if [ "$1" = "--batch" ]; then
  shift
  for pdf in "$1"/*.pdf; do
    [ -f "$pdf" ] || continue
    convert_one "$pdf"
  done
elif [ -f "$1" ]; then
  convert_one "$1"
else
  echo "Usage: $0 <pdf_path>  OR  $0 --batch <folder>"
  exit 1
fi

echo ""
echo "保管先: $OUT_DIR"
ls "$OUT_DIR" | wc -l | xargs echo "ファイル数:"
