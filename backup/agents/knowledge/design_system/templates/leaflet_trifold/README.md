# 後援会リーフレット テンプレート（leaflet_trifold）

## 用途
後援会・選挙前の政治活動リーフレット。**実態はA4両面**（表=顔＋スローガン＋名前特大／裏=3つの約束＋プロフィール＋活動実績5連）。ディレクトリ名の「trifold（三つ折り）」は歴史的呼称で、現行正本v3は二つ折りではなく両面1枚もの。

**ブランド4色（ライム #c7ff4a／濃緑 #1f5a3a／最濃緑 #0f3d27／生成り #f3efe4）を最も忠実に体現する正本作品。**

## 正本
- `template.html` = `kusagawa_archive/02_publications/leaflets/2026-05_senkyo_leaflet_v3/index.html` のverbatimコピー
- 画像（portrait.png・QR・実績写真群）は元ディレクトリの `assets/`・`uploads/` に相対参照。単体レンダリング時はディレクトリごと複製
- 完成PDF: 同ディレクトリ `選挙リーフレット_v3.pdf`／ラクスル入稿版 `選挙リーフレット_v3_rakusuru.pdf`
- 関連: 完成ファイル一覧＝memory/reference_senkyo_leaflet_v3_files／恒久ルールは本README末尾「恒久ルール」節が正本

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
- **ラクスル入稿**: 入稿は基本ラクスル。裏面だけ「システムで問題が発生しました」エラーになるので、入稿の度に `python3 ~/.claude/scripts/rakusuru_back_rasterize.py <案件名>.pdf` で裏面400dpiラスタ版 `<案件名>_rakusuru.pdf` を作って入稿（ベクター版の直接入稿禁止・表面もエラーなら `--pages 1,2`）

## 注意
- 政治表現は「規制→適正立地」等の中立語彙に置換済みの文言を尊重（勝手に強い言葉へ戻さない）
- 元装飾の尊重・段組の勝手な追加禁止（下記「恒久ルール」節）
- 他議員氏名なし／架空エピソードなし／content-fact-checker → content-risk-reviewer 通過必須
- 完成品・素材はDrive `ZZ_選挙関連/` へ

## 恒久ルール（2026選挙リーフレットv3制作・11セッションの往復から抽出。2026-09-05 メモリから吸収）

### 作法
- **客観確認を怠らない**: CSS値を信用せず preview PNG を自分で Read するか natural-design-reviewer に見せる。「鮮やかなlimeにした」もPDFで暗化していれば無価値
- **元装飾を勝手に消さない**: halftone／stripe／tape／sticker／lime影は草川が design-tool で積んだもの。レビュー推奨を反映しすぎて魅力が落ちたら、レビュー由来の変更を一括revertする
- **指示外の段組・大幅レイアウト変更禁止**: 「●ごと改行」の指示に `columns:2` を足して差し戻された。指示の文言どおり最小変更
- 内部メモ風の演出（filename・ファイルサイズ表示）は入れない

### 切れ字（個別 nowrap・汎用 `word-break:keep-all` 禁止＝foundations/rules.md §2）
- 「災害ケアマネジメント」「８０５０」「監督」「サーバー」「現・東京都知事」
- 「一般社団法人 亀山青年会議所 監事」「三重パラ陸上競技協会 理事」「亀山飲食業組合 顧問」「亀山市eスポーツ協会 事務局長」
- 「鈴鹿亀山道路ＩＣ周辺を大きく変える」（行末収め）

### 文言（OK表現とフレーム転換）
- OK: 「次は亀山だ」「あなたの声を、草川たくや と一緒に。」「ええやん 亀山。」（後援会CTA）「コストコ誘致を諦めない」「亀山に、希望の旗を立てる」
- 転換: 太陽光「規制条例」→「適正立地条例」／災害関連死は「TKB48単独」でなく「個別避難計画100%＋福祉避難所事前指定＋災害ケアマネジメント（在宅避難者まで見守り）」のセット／Pillar 03 産業誘致にスポーツ拠点（オリンピアン・パラリンピアン）を加える
- NG表現の横断ルール（距離比喩・「届かない〜」・「次の議会で追及」・議会宛て提言）は MEMORY.md 横断ルール節が正本

### 公選法
- 「討議資料」は紙面右上・白枠透過・白文字 font 8px／opacity .85。これで政治活動用文書扱い＝選挙運動期間外でも配布可
- 「投票してください」「もう一度」等の直接的な投票依頼表現は本文に入れない

### 写真
- 必要解像度の目安＝表示mm × 11.81px/mm × 2。例: 53×33mm枠 → 1500×900px JPEG90%で十分。4032px原寸のままだとChrome PDFが非圧縮埋込して80MB級になる
- 家族写真の子どもの顔は PIL `GaussianBlur(radius=18)` を**楕円マスク**で（矩形は背景に被って不自然）。草川本人はそのまま
- キャプション `.b-photo .mono`: 10.5px／italic／nowrap＋ellipsis。黒タグ（題名）と書体で役割分離

### A4規格の詳細
- Chrome headless は `--paper-width=8.27 --paper-height=11.69 --no-pdf-header-footer --virtual-time-budget=20000` を付ける
- `.page-label-wrap` は overflow:hidden＋page-break-after:always、`.leaflet{overflow:hidden}` で紙面外を切除
- 4行に収めたい本文は `<br>` で改行位置を固定。「2列に見える」「右が空欄」は grid columns と max-width の調整問題。写真サイズを変えたらテキスト箱幅と縦余白を両方再計算

### 保存先
- ローカル正本: `kusagawa_archive/02_publications/leaflets/<YYYY-MM>_<案件名>/`（PDFは直下・日本語名可）。元画像は `assets/_orig/`、最適化済みは `assets/`
- 規格値は `~/.claude/scripts/specs.json`、保存前に `gate.py` を通す
