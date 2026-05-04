#!/usr/bin/env bash
# Drive→ローカル同期スクリプト
#
# 使い方:
#   1. Drive ブラウザから新規議事録PDFを 99_raw/_drive_originals/transcripts/ にダウンロード
#   2. 新規市政報告レポートPDFを 99_raw/_drive_originals/reports/ にダウンロード
#   3. このスクリプトを実行
#      bash ~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_sync.sh
#
# 動作:
#   - 議事録PDF→pdftotext→草川パート抽出（_extract_kusagawa.py / _extract_committee.py）→01_council/に統合
#   - 市政報告PDF→pdftotext→02_publications/reports/に配置
#   - 既にローカル化済のファイルはスキップ（更新時刻比較）

set -e

ARCHIVE="/Users/kusakawatakuya/.claude/agents/knowledge/kusagawa_archive"
RAW="${ARCHIVE}/99_raw/_drive_originals"
SCRIPTS="${ARCHIVE}/99_raw/_scripts"
COUNCIL="${ARCHIVE}/01_council"
REPORTS="${ARCHIVE}/02_publications/reports"

cd "${RAW}/transcripts"

# ===== 議事録PDF→txt変換（差分のみ） =====
echo "===== 議事録 PDF→txt 変換 ====="
mkdir -p _text _kusagawa_only _needs_ocr
new_pdf=0
for f in *.pdf *.docx; do
  [ -f "$f" ] || continue
  base="${f%.*}"
  out="_text/${base}.txt"
  if [ ! -f "$out" ] || [ "$f" -nt "$out" ]; then
    if [[ "$f" == *.pdf ]]; then
      pdftotext -layout "$f" "$out" 2>/dev/null
      sz=$(wc -c < "$out" 2>/dev/null || echo 0)
      if [ "$sz" -lt 5000 ]; then
        mv "$out" "_needs_ocr/${base}.empty"
        cp "$f" "_needs_ocr/$f"
        echo "  [OCR要] $f"
        continue
      fi
    elif [[ "$f" == *.docx ]]; then
      python3 << PYDOCX
import zipfile, xml.etree.ElementTree as ET
with zipfile.ZipFile("$f") as z:
    target = next(n for n in z.namelist() if 'document.xml' in n and 'rels' not in n)
    xml_data = z.read(target).decode("utf-8")
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
tree = ET.fromstring(xml_data)
paras = []
for p in tree.iter(W+'p'):
    texts = [t.text or '' for t in p.iter(W+'t')]
    paras.append(''.join(texts))
open("$out", 'w', encoding='utf-8').write('\n'.join(paras))
PYDOCX
    fi
    new_pdf=$((new_pdf+1))
    echo "  [new] $f → $out"
  fi
done
# UTF-16 txt→UTF-8 変換
for f in *.txt; do
  [ -f "$f" ] || continue
  if file "$f" | grep -q "UTF-16"; then
    iconv -f UTF-16LE -t UTF-8 "$f" > "_text/$f" 2>/dev/null
  else
    cp "$f" "_text/$f"
  fi
done
echo "  新規/更新: $new_pdf 件"

# ===== 草川パート抽出（本会議＋委員会） =====
echo "===== 草川パート抽出 ====="
cp "${SCRIPTS}/_extract_kusagawa.py" .
cp "${SCRIPTS}/_extract_committee.py" .
python3 _extract_kusagawa.py | tail -10
python3 _extract_committee.py

# ===== 01_council/への統合 =====
echo "===== 01_council/ 統合 ====="
copied=0
for f in _kusagawa_only/*_kusagawa_only.txt; do
  [ -f "$f" ] || continue
  base=$(basename "$f")
  # YYYY-MM_セッション_種別_kusagawa.txt 形式へ命名統一は手動マッピング要
  # （元ファイル名から年月推定が複雑なため、新規ファイルは手動でリネーム）
  target="${COUNCIL}/${base}"
  if [ ! -f "$target" ]; then
    cp "$f" "$target"
    copied=$((copied+1))
    echo "  [new] $target"
  fi
done
echo "  新規統合: $copied 件"

# ===== 市政報告レポート変換 =====
echo "===== 市政報告レポート PDF→txt ====="
cd "${RAW}/reports"
mkdir -p _text _needs_ocr
new_report=0
for f in *.pdf; do
  [ -f "$f" ] || continue
  base="${f%.pdf}"
  out="_text/${base}.txt"
  if [ ! -f "$out" ] || [ "$f" -nt "$out" ]; then
    pdftotext -layout "$f" "$out" 2>/dev/null
    sz=$(wc -c < "$out" 2>/dev/null || echo 0)
    if [ "$sz" -lt 200 ]; then
      mv "$out" "_needs_ocr/${base}.empty"
      cp "$f" "_needs_ocr/$f"
      echo "  [OCR要] $f"
      continue
    fi
    cp "$out" "${REPORTS}/${base}.txt"
    new_report=$((new_report+1))
    echo "  [new] $f → 02_publications/reports/${base}.txt"
  fi
done
echo "  新規変換: $new_report 件"

echo
echo "===== 同期完了 ====="
echo "01_council/ 件数: $(ls "${COUNCIL}" | wc -l)"
echo "02_publications/reports/ 件数: $(ls "${REPORTS}" | wc -l)"
echo
echo "次の手順:"
echo "  1. 新規議事録ファイル名を 'YYYY-MM_セッション_本会議議事録_kusagawa.txt' 形式にリネーム"
echo "  2. INDEX.md / _council_search_index.md を更新"
echo "  3. 関連 themes/*.md があれば該当セクション追記"
