---
name: drive-pdf-line-qr-page-overflow
description: 市政報告A4両面印刷物にDrive一次情報の図面（建物配置図・地図等）を挿入する手順、contact-boxにLINE公式QRを並列配置するCSSパターン、Page overflowを段階的に解消する圧縮優先順位を統合した再利用ノウハウ
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9bc910a0-00cb-4440-a1bc-d9d7ec9c1703
---

二本松版v6（2026-05-23制作）で確立した3つの再利用可能パターン。

## 1. Drive PDF → 印刷物用図面抽出フロー

**Why:** 大店立地法届出書のような一次情報PDF（コメリパワー亀山店地元説明会資料.pdf 等）から建物配置図・交通計画図を抽出して印刷物に挿入したいケースが定常化（出店案件・公共施設更新・道路工事計画等の市政報告で頻発）。

**How to apply:**
1. Drive MCP `download_file_content` → 1.5MB級は base64 が context制限超え。tool-results txt から `jq -r .content | base64 -d > 出力.pdf` で復元
2. `pdftoppm -r 150 -jpeg -jpegopt quality=85 入力.pdf 出力prefix` でページ別 JPEG 化
3. PIL でクロップ・回転・余白トリミング:
   ```python
   from PIL import Image
   img = Image.open('page-1.jpg')
   crop = img.crop((x1, y1, x2, y2))  # 図面領域
   crop = crop.rotate(90, expand=True)  # 必要なら CCW 90度
   crop = crop.crop((0, 290, w, h-10))  # 余白トリミング
   crop.save('out.jpg', 'JPEG', quality=88, optimize=True)
   ```
4. 中間素材（`_komeri_pages/` 等）は案件サブフォルダに保持して再編集可能に
5. 元PDFも案件フォルダに保存（後追い検証用）

## 2. contact-box への LINE QR並列配置パターン

**Why:** 公式LINE友だち登録は SNS の中で最も登録 friction が高い（QRが無いとほぼ登録されない）。市政報告印刷物の contact-box にQRを必ず入れる運用に切り替え。

**LINE公式QR URL:** `https://qr-official.line.me/gs/M_312kuncx_GW.png?oat_content=qr`（草川 = `M_312kuncx_GW`）

**How to apply（CSS+HTML パターン）:**
```css
.contact-box {
  display: flex; gap: 4mm; align-items: stretch;
  border: 2.5px solid #1f7a3a;
  padding: 2mm 4mm;
}
.contact-main { flex: 1; min-width: 0; }
.contact-qr {
  width: 26mm; flex-shrink: 0;
  border-left: 1.5px dashed #c89211;
  padding-left: 3mm;
  display: flex; flex-direction: column;
  justify-content: center; align-items: center;
}
.contact-qr img { width: 100%; }
.contact-qr .qr-caption {
  font-size: 7.5pt; font-weight: 900; color: #0e4d27;
}
```
```html
<div class="contact-box">
  <div class="contact-main"><!-- 既存テキスト --></div>
  <div class="contact-qr">
    <img src="line_qr.png" alt="公式LINE QR">
    <div class="qr-caption">公式LINEで<br>友だち登録</div>
  </div>
</div>
```
- QR画像は `curl -sSL <url> -o line_qr.png` で案件フォルダにダウンロード
- 幅26mm が読み取り精度と省スペースのバランス点（22mm未満は読取困難・35mm超は contact-text を圧迫）

## 3. Page overflow 段階圧縮の優先順位

**Why:** 二本松版v6 で章3+章4+contact-box が Page 2 から overflow（contact-box 下半分が切れる事象）。情報削減せずレイアウト最適化で 30mm 節約した手順。

**How to apply（効果大→小の順）:**
1. **写真ブロックを右float＋本文wrap化** — 章内 photo の幅を 42mm → 35mm に下げ、本文がwrap分量増 → 全体高さ7〜10mm削減
2. **2カラム infobox を解体し短い1行ボックスに圧縮** — 5項目 ul を「：」区切りの1行テキストに圧縮 → 15〜20mm削減
3. **figure block の max-width を絞る** — 配置図ブロック max-width: 145mm → 100mm に下げると高さ 75→50mm（差25mm）
4. **冗長な quote-strong ブロックを削除** — 「予告」型のブロックは情報密度低・削除候補 → 10〜12mm削減
5. **komeri-overview等の2カラム card の padding/font-size 微減** — 1.5mm→1.2mm、8pt→7.8pt、line-height 1.4→1.35 → 5mm削減
6. **kusagawa-comment 文字圧縮** — 同じメッセージで30〜80字短縮 → 4〜5mm削減

**禁止事項:**
- まず chapter ごと削除する策（情報量大幅劣化）
- font-size を 7.5pt 未満に下げる（高齢者向け視認性悪化）
- padding 0mm 化（contact-box の枠が窮屈に見える）

**検証方法:**
- 毎イテレーション後に `pdftoppm -r 110 ...` でPage 2を画像化、下半分（`crop((0, h*0.78, w, h))`）を Read して contact-box jichikai-note まで表示されているか目視確認
- `pdfinfo` で Pages 数が想定通りか（章末で意図せず Page 3 流入していないか）

## 関連メモリ

- 既存印刷物チェックリスト: [[feedback_print_publication_checklist]]
- 案件別フォルダ運用: [[feedback_publications_binary_storage]]
- 印刷物PDF自動open: [[feedback_auto_open_pdf_after_render]]
- 画像EXIF処理: [[feedback_image_exif_processing]]
