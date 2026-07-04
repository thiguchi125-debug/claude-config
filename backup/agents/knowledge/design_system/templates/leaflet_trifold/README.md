# 後援会リーフレット テンプレート（leaflet_trifold）

## 用途
後援会・選挙前の政治活動リーフレット。**実態はA4両面**（表=顔＋スローガン＋名前特大／裏=3つの約束＋プロフィール＋活動実績5連）。ディレクトリ名の「trifold（三つ折り）」は歴史的呼称で、現行正本v3は二つ折りではなく両面1枚もの。

**ブランド4色（ライム #c7ff4a／濃緑 #1f5a3a／最濃緑 #0f3d27／生成り #f3efe4）を最も忠実に体現する正本作品。**

## 正本
- `template.html` = `kusagawa_archive/02_publications/leaflets/2026-05_senkyo_leaflet_v3/index.html` のverbatimコピー
- 画像（portrait.png・QR・実績写真群）は元ディレクトリの `assets/`・`uploads/` に相対参照。単体レンダリング時はディレクトリごと複製
- 完成PDF: 同ディレクトリ `選挙リーフレット_v3.pdf`／ラクスル入稿版 `選挙リーフレット_v3_rakusuru.pdf`
- 関連ルール正本: feedback_leaflet_design_principles／reference_senkyo_leaflet_v3_files

## 紙サイズ・dpi
- 本体 842×1190px × 2面。`@media print` で `transform:scale(0.9426)` によりA4（210×297mm）にフィット
- 写真は300dpi相当（`sips -Z 1500 -s formatOptions 90`）。人物写真はEXIF正規化必須

## デザイン語彙（この様式の識別子）
- 斜め緑マッシブ（rotate(-14deg) の #1f5a3a 塊＋#0f3d27 インセット枠＋ハーフトーンフェード）
- 黒枠写真＋ライム影（`border:黒` ＋ `box-shadow: Npx Npx 0 #111418, ... #c7ff4a`）＋わずかな回転
- 明朝特大名前（Shippori Mincho B1 900・240px/200px）＋ Anton 番号（text-shadow黒オフセット）
- ライム下線ハイライト＝`box-shadow:inset 0 -0.28em 0 #c7ff4a`（**gradient hard-stop禁止**）
- 紙目グレイン（`.grain` multiply オーバーレイ）／黒リボン帯／切手風スタンプ／ミシン目

## 差し替えポイント
- 表面: VOL番号・スローガン（`.f-headline`）・タグ3枚・人物写真（`.f-portrait img`）・スタンプ文言・連絡先／QR2枠
- 裏面: 3つの約束（`.b-policy01`看板政策5セル／`.b-subs`サブ政策2箱／`.b-pillar` p02・p03）・プロフィール・活動実績5連（写真＋タイトル）
- 「討議資料」表記（`.f-discussion-mark`）は**削除禁止**（公選法対策）

## PDF生成・入稿
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=/絶対パス/leaflet.pdf /絶対パス/index.html
open /絶対パス/leaflet.pdf
```
- **ラクスル入稿**: 裏面がフォント・エフェクト起因でエラーになる場合、裏面のみ `pdftoppm -r 400` ＋ PIL でJPEGラスタライズ→表面と再結合（feedback_rakusuru_back_rasterize）

## 注意
- 政治表現は「規制→適正立地」等の中立語彙に置換済みの文言を尊重（勝手に強い言葉へ戻さない）
- 元装飾の尊重・段組の勝手な追加禁止（feedback_leaflet_design_principles）
- 他議員氏名なし／架空エピソードなし／content-fact-checker → content-risk-reviewer 通過必須
- 完成品・素材はDrive `ZZ_選挙関連/` へ
