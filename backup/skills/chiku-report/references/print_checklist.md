# 市政報告レポート（A4両面）制作チェックリスト＋レイアウト定型

> 2026-05 太岡寺版 v1→v19（19回反復）と二本松版 v6 で確立。旧 memory/feedback_print_publication_checklist ＋ feedback_print_diagram_qr_layout を 2026-09-05 に吸収。
> **数値の正本は `design_system/templates/report_a4_duplex/template.html`**。ここの実測値と食い違ったら template を優先し、この文書を直す。

## 0. なぜ要るか
局所修正の累積で全体バランスが壊れる（氏名が小さい／数字セル拡大で空欄／章2タイトル2行折返し／章ごとにフォント不揃い／他地区プロローグのコピペ残存）。事前に潰せば各3回の往復が1回で済む。

## 1. レイアウト規範（木下版v22・太岡寺版v19の実測）
- A4両面2ページ厳守（3ページ目溢れ禁止）。ページpadding上下 約10〜14mm・左右 約11mm
- ヘッダ顔写真 36〜38mm円形。氏名「草川たくや」42pt級ゴシック太字（22ptは小さすぎで差戻し済）
- 連絡先ボックスの電話／メール／ご意見箱ラベルは金枠角丸
- 配色は緑 #1f7a3a・金 #c89211・濃緑 #0e4d27（この様式ではライム系は使わない）

## 2. タイポ階層
氏名42pt／章タイトル16pt（章2が1行に収まらない時だけ14pt＋letter-spacing -0.01em＋nowrap）／プロローグh2 12pt級／数字セル value 22pt（縮小不可）・unit 11pt・label 9pt／**章本文は全章9.5pt統一**／行間1.6（章2のみ1.45可）

## 3. 写真・図表
- 章2主役写真は横長80×54mm（縦長48×64mmは脇役見えで却下済）。章1バス写真64×42mm。章3地図・工事写真75×50mm
- 数字グリッドは flex:1 で残り幅フル展開（width固定は右に空欄）
- キャプションは「▲タイトル」＋改行＋「※聞き取り内容をもとに草川が作成したイメージ図です」（イメージ図は注記必須）
- iPhone写真は PIL exif_transpose で正規化→EXIF strip（design_system/foundations/rules.md §3）

## 4. 文章チェック
- プロローグh2の主語が当該地区か（神辺共通プロローグを使う時も地区独自段落を1つ足す。「神辺地区は『選ばれる地域』」コピペ残存が致命事故）
- 他地区名の残存を grep（"神辺" "木下" "御幸" など）
- 特定案件を直接想起させる表現を避ける（「無秩序な設置リスク」は事業者への名誉毀損リスク）
- 「常に」「全て」等の最上級は根拠1件なら使わない（「いち早く」「〜の動きが続いてきた」へ）
- 自治会員個人名は載せない（要望書に会長名があっても「自治会から」）

## 5. 章順
表面＝ヘッダ→プロローグ→章1→章2（地区主役テーマ）／裏面＝章3→連絡先。**主役テーマは表面**（太岡寺版は太陽光条例を章2へ格上げ）

## 6. 安全ゲートと俯瞰
- content-fact-checker → content-risk-reviewer。**プロローグ書換え等の大幅変更後は再通過**（v14で飛ばしてv19から逆戻り）
- natural-design-reviewer を制作中に複数回。規格値は `~/.claude/scripts/specs.json`、保存前に `gate.py`

## 7. 保管・配布
- `kusagawa_archive/02_publications/reports/<YYYY-MM>_<地区名>版_市政報告/`。中間素材（抽出ページ画像等）と元PDFも同フォルダに残す
- 配布前に自治会長へ一報推奨。告示日（2026-10-18想定）180日以内は事前運動疑義の精査
- 規範PDF: 木下版 `2026-05_木下版_市政報告/市政報告_木下版_2026-05-13_v22.pdf`／太岡寺版 `2026-05_太岡寺版_市政報告/市政報告_太岡寺版_2026-05-15_v19.pdf`

---

## A. Drive一次資料PDFから図面を抜く（配置図・交通計画図など）
1. Drive MCP `download_file_content` は1.5MB級でbase64が文脈超過 → tool-results の txt から `jq -r .content | base64 -d > 出力.pdf`
2. `pdftoppm -r 150 -jpeg -jpegopt quality=85 入力.pdf prefix` でページ別JPEG
3. PIL で `crop((x1,y1,x2,y2))` → 必要なら `rotate(90, expand=True)` → 余白トリム → `save(..., quality=88, optimize=True)`
4. 中間素材は案件サブフォルダ（例 `_komeri_pages/`）に保持、元PDFも保存

## B. contact-box に LINE公式QR を並列配置
- URL: `https://qr-official.line.me/gs/M_312kuncx_GW.png?oat_content=qr`（`curl -sSL … -o line_qr.png`）。QRが無いとほぼ登録されない
- 幅 **26mm**（22mm未満は読取困難・35mm超は本文を圧迫）
```css
.contact-box{display:flex;gap:4mm;align-items:stretch;border:2.5px solid #1f7a3a;padding:2mm 4mm}
.contact-main{flex:1;min-width:0}
.contact-qr{width:26mm;flex-shrink:0;border-left:1.5px dashed #c89211;padding-left:3mm;display:flex;flex-direction:column;justify-content:center;align-items:center}
.contact-qr img{width:100%} .contact-qr .qr-caption{font-size:7.5pt;font-weight:900;color:#0e4d27}
```
```html
<div class="contact-box"><div class="contact-main">…</div>
<div class="contact-qr"><img src="line_qr.png" alt="公式LINE QR"><div class="qr-caption">公式LINEで<br>友だち登録</div></div></div>
```

## C. Page overflow の段階圧縮（効果大→小。章削除は最後の手段でなく禁止）
1. 写真を右float＋本文wrap、写真幅42→35mm（7〜10mm）
2. 2カラム infobox を「：」区切り1行に（15〜20mm）
3. figure の max-width 145→100mm（約25mm）
4. 「予告」型の quote-strong を削除（10〜12mm）
5. card の padding 1.5→1.2mm・8→7.8pt・line-height 1.4→1.35（5mm）
6. kusagawa-comment を30〜80字短縮（4〜5mm）
- 禁止: 章ごと削除／7.5pt未満／padding 0
- 検証: 毎回 `pdftoppm -r 110` でPage2を出し下部22%を切り出してReadし contact-box 末尾まで見えるか確認。`pdfinfo` でページ数
