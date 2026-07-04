---
name: design-studio
description: 草川たくや（亀山市議会議員）のチラシ・ポスター・市政報告レポート・リーフレット等の印刷物デザインを「テンプレ選択→素材収集→実装（Chrome実測EYES-FIRST）→物理破綻レビュー→安全ゲート→PDF→正規保存→テンプレ昇格還元」まで1パスで完結させるデザイン制作オーケストレータースキル。「チラシ作って」「〇〇のチラシ」「ポスター作って」「リーフレット作って」「市政報告レポート作って」「デザイン制作」「design-studio」「印刷物作って」等で必ず起動。正本テンプレート集は ~/.claude/agents/knowledge/design_system/（claude.ai/design「草川たくやデザインシステム」とDesignSyncで同期）にあり、制作は必ずテンプレ候補2〜3提示→草川選択から始める。実装はprint-layout-architect（HTML/CSS→Chrome headless実測ループ）、レビューはnatural-design-reviewer（物理破綻・新規指摘のみ）、対外配布物はcontent-fact-checker→content-risk-reviewer必須通過、design-director（8軸プロ昇格）は選挙物・大判ポスター等の勝負所のみ草川承認制で追加起動。完成PDFは自動openし、保存先マップ準拠（~/publications/ or Drive正規置き場）＋出来が良ければテンプレ昇格提案→design systemへ部品化→claude.ai/design再pushの還元ループまで回す。Canva以上の品質を毎回再現するための構造。※ショート動画挿入画像→short-video-image-designer、スライド→slide-deck-prep/shisei-houkokukai、写真選定のみ→photo-curatorが正で本スキルは反応しない。
---

# design-studio スキル

## 目的
Canva以上のクオリティの印刷物デザイン制作を、Claude Code起点で毎回同じ品質水準で再現する。
過去に個別セッションで発生していた迷子（テンプレを一から作り直す／レビューループ抜け／保存先迷子／良作が使い捨てになる）を構造的に潰す。

**品質基準の正本 = 中庄夏祭りポスター2026水準**（参照忠実再現・グリフ単位検品・レイヤー順・EYES-FIRST・完成処理込み）。

## 起動条件

以下のいずれかで起動:
- 「チラシ作って」「〇〇のチラシ」「ポスター作って」「〇〇のポスター」
- 「リーフレット作って」「市政報告レポート作って」「印刷物作って」
- 「デザイン制作」「design-studio」
- 種別不明でも「〇〇の告知物を作りたい」等、紙もの制作の意図が明確なとき

## 委譲先（このスキルが呼ばないもの）
- ショート動画の挿入画像 → short-video-image-designer
- スライド → slide-deck-prep（NotebookLM経由）／市政報告会スライドのみ shisei-houkokukai Stage3
- 写真の選定だけ → photo-curator 単独
- SNS投稿文 → sns-content-creator
- YouTubeサムネ等のデジタル単発画像 → 本スキルの簡易経路（Step4-6を1枚絵向けに短縮）でも可

## 正本リソース

| リソース | 場所 |
|---|---|
| デザインシステム正本 | `~/.claude/agents/knowledge/design_system/` |
| テンプレート4種 | 同 `templates/{flyer_a4, poster, report_a4_duplex, leaflet_trifold}/` |
| 部品 | 同 `components/`（ライムバー見出し・QRフッター・photo-text行・数字ブロック） |
| 恒久デザインルール | 同 `foundations/rules.md`（**実装前に必読**） |
| ブランド色 | #c7ff4a／#1f5a3a／#0f3d27／#f3efe4（`foundations/colors.html`） |
| クラウド正本ミラー | claude.ai/design「草川たくやデザインシステム」（DesignSync同期） |
| 過去制作の分析 | `~/.claude/agents/knowledge/design_references/` |

## パイプライン（標準経路）

### Step 0: 要件ヒア（1回だけ・まとめて聞く）
AskUserQuestionで一括確認: ①種別（チラシ/ポスター/レポート/リーフレット/その他）②サイズ ③配布先・用途（対外配布か内部か）④印刷方法（自宅/ラクスル/コンビニ）⑤納期 ⑥素材の有無（写真・ロゴ・原稿）。
既に発言に含まれる項目は聞き直さない。

### Step 1: テンプレ選択
1. `design_system/templates/` から該当種別の template.html＋README を確認
2. **候補2〜3案を提示**（各案: どのテンプレ/部品構成か・完成イメージの言語化1〜2行）。過去類似案件が design_references にあれば挙げる
3. 草川が claude.ai/design のカード一覧で見たい場合はプロジェクトURLを案内
4. 草川選択 → 案件フォルダ作成: `~/publications/<YYYY-MM_案件名>/`（政治活動物）または drafts（試作）

### Step 2: 素材収集
- 写真: photo-curator（草川本人= ZPERSON=18）。EXIF正規化（`PIL ImageOps.exif_transpose`＋strip）、`sips -Z 1500 -s formatOptions 90` で最適化
- 文言・実績: **アーカイブgrep必須**（`kusagawa_archive/{01_council,02_publications,05_resources,06_election}` ＋草川独自語彙並列）
- ロゴ等の定番: eスポーツ協会=`assets/esports_logo/logo_transparent.png` 等、rules.md の定番アセット表参照
- QR: 必要なら生成（誤り訂正H・ブランド緑）

### Step 3: 実装 — print-layout-architect
template.html を案件フォルダへ複製し、print-layout-architect に委譲:
- 指示に必ず含める: 「design_system/foundations/rules.md 準拠。Chrome headless実測（scrollHeight−clientHeight=0）→PNGを自分でReadして検品→修正のEYES-FIRSTループ。0ツール停止禁止・自分で実測ループ」
- 切れ字は固有名詞のみ個別 nowrap／lime下線は box-shadow inset

### Step 4: レビュー — natural-design-reviewer
物理破綻チェック（写真切れ・枠外はみ出し・大空欄・連絡先切れ）。2回目以降は新規指摘のみ。指摘→print-layout-architect修正→再レビューを破綻ゼロまで。

**勝負所判定**: 選挙関連物・A2以上の大判・長期掲示物・後援会リーフレットは design-director（8軸プロ昇格）の追加起動を草川に提案（承認制・トークン大）。

### Step 5: 安全ゲート（対外配布物は必須・skip禁止）
1. content-fact-checker — 日付・場所・数値・固有名詞・主催表記（例: 親子で米づくり=亀山JC主催）を一次情報照合
2. content-risk-reviewer — 公選法（政治活動物は「討議資料」表記）・個人情報・他議員氏名不掲載 等8軸
- HIGH以上はASK_USER、CRITICALは即停止
- 内部資料・私的用途のみの場合は草川に確認の上で省略可

### Step 6: 完成処理
1. PDF生成（Chrome headless）→ **`open <絶対パス>` 即実行**（HTMLは自動openしない）
2. 入稿仕様: ラクスル両面物は裏面ラスタライズ（`pdftoppm -r 400`＋PIL→再結合）
3. 保存: 案件フォルダに完成品＋中間素材（中間版は最終確定後に削除）。Drive正規置き場へミラー（選挙物=`ZZ_選挙関連/`、市政報告=`ZZ_市政報告レポート/`、他は用途に応じ保存先マップ準拠）
4. nichijo日次ログに制作1行を追記

### Step 7: テンプレ昇格還元（使い捨て防止・毎回判定）
完成品が既存テンプレに無い型・部品を含む場合、草川に1問: 「この○○（レイアウト/部品）をデザインシステムに昇格させる？」
- 承認時: `design_system/` に template/component として追加（preview.html は自己完結・個人情報/人物写真なし・1行目に `<!-- @dsCard group="…" name="…" subtitle="…" -->`）
- `design_references/` に制作レポート1本追記（何が効いたか・数値・反省）
- claude.ai/design へ差分push（下記）

## claude.ai/design 同期手順（DesignSyncツール）

- プロジェクト: 「草川たくやデザインシステム」（type=DESIGN_SYSTEM。初回は create_project）
- 手順: `list_files`（構造diff）→ 変更対象のみ `finalize_plan`（localDir=design_system、writes/deletesを部品単位で列挙）→ `write_files`（localPath方式）
- **wholesale replace禁止**。差分の部品単位でpush
- previewに個人情報・人物写真・他議員氏名が無いことをpush前に確認
- カードが自動認識されない場合のみ `register_assets` で明示登録
- 認可エラー時: 草川に「/design-login を実行してください」と案内（一回きり）

## 短縮経路（急ぎ・小物）
納期当日〜翌日 or 名刺サイズ等の小物: Step1のテンプレ候補は1案即決、Step4は1周のみ、Step7は省略可。**Step5安全ゲートは短縮経路でも削らない**。

## トークン規律（lean常時適用）
- テンプレ・rules.md・過去参照の読み込みは必要ファイルのみ（design_system全読み禁止）
- print-layout-architect への指示に「実測ループは自分で完結・往復報告は要点のみ」を含める
- 目標: チラシ1本 標準経路で90〜170K

## 📌 恒久ガードルール（このスキル常駐分）
- 絵文字禁止（発信物）／AI製SaaS LP風禁止（紫グラデ・浮き角丸カード・絵文字丸アイコン・ピルバッジ・LP構図）
- 架空エピソード・つくり話禁止（実体験/一次情報/公式データのみ）
- 他議員の氏名は対外印刷物に載せない
- 主催表記の正確性（親子で米づくり=亀山JC主催／昼生お花見=まち協×振興会 等、fact-checkerで必ず照合）
- デザイン品質基準=中庄夏祭りポスター2026以上
- 「亀山」typo（亜山・亵山）絶対禁止。日本語は直接書く（unicode escape禁止）
- イベント運営段取り表は幅390pxスマホ縦スクロールPDF（A4/長尺PNG不可）
