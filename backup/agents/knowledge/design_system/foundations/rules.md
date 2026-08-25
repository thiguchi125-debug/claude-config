# デザイン制作の恒久ルール集

> 草川たくや（亀山市議会議員）の印刷物・発信物デザインで**毎回守る**ルール。
> 出典は MEMORY.md の feedback 群。ここは制作時に一読する集約版（詳細は各 feedback_*.md）。

## 0. 品質基準

- **全デザイン制作物は「中庄夏祭りポスター2026」水準以上**（`templates/poster/template.html` が正本）。
  - 参照忠実再現：参考デザインがある場合はグリフ・配置単位で忠実に再現する
  - グリフ単位検品：レンダリング後PNGを自分の目で開き、文字の欠け・重なり・はみ出しを1文字単位で確認
  - レイヤー順：背景→装飾→写真→テキストの z-index 設計を意図的に組む
  - EYES-FIRST：コードを信用せず、Chrome headless で実画素を確認してから完成と言う
  - 完成処理込み：PDF化・トリミング・実測余白確認まで含めて「完成」

## 1. 禁止意匠

- **絵文字禁止**（発信物・印刷物HTML全般。AI臭の筆頭）。見出し装飾は CSSライムバー／角マーカー／罫線で。制作後にコードポイント検査（絵文字混入チェック）を行う。
- **AI製SaaS LP風の意匠禁止**：紫グラデ／浮き角丸カード（drop-shadow浮遊カード）／絵文字丸アイコン／ピルバッジ／LP構図（hero→3カラム特徴→CTA）。
  - 基調（配色・書体・構図）は**内容毎に作り分ける**。特定スタイルの標準化はしない。禁止はあくまで「AI臭」だけ。
- 架空エピソード・つくり話・情緒メタファー禁止。実体験・一次情報・公式データのみ。
- 他議員の氏名は対外配布物に載せない（内部資料はOK）。

## 2. CSS実装の確定パターン

- **lime下線は box-shadow inset 方式**：`box-shadow: inset 0 -0.28em 0 #c7ff4a;`
  linear-gradient のハード・ストップ（`background:linear-gradient(transparent 60%, #c7ff4a 60%)`）は**PDF変換で暗化するため禁止**。
- **切れ字（改行分断）対策は固有名詞だけ個別 `white-space:nowrap`**。汎用CSS（body全体 word-break 等）の変更は禁止。
- 印刷色再現：`-webkit-print-color-adjust: exact; print-color-adjust: exact;` を必ず入れる。
- ブランドカラーは `foundations/colors.html` 参照（ライム #c7ff4a／濃緑 #1f5a3a／最濃緑 #0f3d27／生成り #f3efe4）。家庭用プリンタ配布物はインク節約パレット（#1f7a3a／#0e4d27／#c89211・ベタ塗り3%以下）。
- 日本語はHTML/JSON内でも**直接書く**（unicode escape禁止）。「亀山」のtypo（亜山・亵山）絶対禁止 — JSON escape 由来の事故実績あり。

## 3. 画像・写真処理

- **写真ハードゲート（対外配布物・skip禁止）**:
  1. **実写真を1枚以上入れる**。AI生成写真での代替は禁止（実在感が消え、AI臭の主因になる）
  2. **写真・図版の占有率は参照カルテの数値を下限**として扱う（Step 4-B ④で採点。下回ったら差し戻し）
  3. 実写真が確保できない案件は、写真を薄く小さく入れて誤魔化さず**タイポグラフィを絵にする路線へ切り替える**（参照 brand01 / 様式 `style_ink_saving_report`）
  4. 例外はプレビュー・テンプレ共有物のみ（人物写真・個人情報を含めないため、プレースホルダー矩形で代替する）

- 画像最適化：`sips -Z 1500 -s formatOptions 90 <img>`（A4で300dpi目安）。
- EXIF：`PIL ImageOps.exif_transpose` で回転正規化＋EXIF strip（位置情報等の漏えい防止）。
- バイナリ素材は案件別サブフォルダ `<YYYY-MM>_<案件名>/` に隔離。中間版は最終確定後に削除。
- 写真は photo-curator（草川 ZPERSON=18）で選定。プレビュー/テンプレ共有物には人物写真・個人情報を含めない（プレースホルダー矩形で代替）。

## 4. レイアウト工程

- レイアウト作り込みは **print-layout-architect** に任せる（画像大きく・text-beside-image 2カラム・Chrome実測反復）。エージェントが0ツールで停止したら自分で実測ループ（scrollHeight−clientHeight=0 確認）。
- `margin-top:auto` でのフッター押し下げ禁止（オーバーフロー事故源）。横長地図は `aspect-ratio` ＋ `object-fit:cover`。
- 物理破綻チェックは **natural-design-reviewer**（写真切れ・枠外はみ出し・大空欄・連絡先切れ。2回目以降は新規指摘のみ）。
- 勝負所（選挙物・大判ポスター）のみ design-director で8軸昇格（草川承認制）。

## 5. PDF生成・入稿

- PDF生成コマンド例：
  ```bash
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless --disable-gpu --print-to-pdf=<絶対パス>.pdf --no-pdf-header-footer <絶対パス>.html
  ```
- **PDF生成後は `open <絶対パス>` を即実行**（草川が目視できる状態にする）。HTMLは自動openしない。
- **ラクスル入稿の裏面ラスタライズ**：フォント・エフェクト起因の入稿エラーは裏面を `pdftoppm -r 400` ＋ PIL でJPEG化→表面PDFと再結合して回避。
- 政治活動印刷物には**「討議資料」表記**を必ず入れる（公職選挙法対策。リーフレットv3 の `.f-discussion-mark` 参照）。

## 6. 印刷物チェックリスト（配布前・回収不能）

1. **レイアウト**：余白実測（上下差2mm以内）／はみ出し・切れゼロ／ページ配分に意図がある
2. **タイポ**：切れ字nowrap／ウェイト4段／本文line-height 1.7以上／固有名詞コピペ（手打ち禁止）
3. **写真**：300dpi相当／EXIF処理済／構図破綻なし／キャプション・出典
4. **章順・構成**：情報階層が3秒で読める／数字は一次資料照合済み
5. **安全ゲート**：content-fact-checker → content-risk-reviewer 通過（対外配布物は必須・skip禁止）
6. **俯瞰レビュー**：最終PDFを1枚絵として引きで見る（EYES-FIRST）／「討議資料」表記／他議員氏名なし／絵文字なし

## 7. 保存先

- 完成品は保存先マップ準拠（選挙・リーフレット素材→Drive `ZZ_選挙関連/`、市政報告レポート→Drive `ZZ_市政報告レポート/`、下書き→`~/.claude/projects/-Users-kusakawatakuya/drafts/`）。
- 出来が良ければテンプレ昇格：この design_system に部品化して還元し、claude.ai/design へ再push。
