---
name: slide-deck-prep
description: 草川たくや（亀山市議会議員）の30〜90分プレゼン（市政報告会・自治会総会・業界団体集会・後援会総会・議会報告会）のスライドを、NotebookLM向けのソース束＋マスタープロンプトとして ~/outputs/slide-deck-prep/ に用意する。Marp/Slidev等での直接生成は禁止・必ずNotebookLM経由。他議員氏名は記載しない。安全ゲート通過必須。Triggers: スライド作って/〇〇のスライド/市政報告会のスライド/自治会総会のスライド/後援会総会のスライド/NotebookLM資料準備/プレゼン資料/報告会の資料/slide-deck-prep。NOT: 1〜10分の挨拶→aisatsu-prep、報告会の運営一式→shisei-houkokukai
---

# slide-deck-prep スキル

## 目的
草川たくやが「市政報告会で40分話す」「自治会総会で60分」「業界団体集会で90分」と発言した瞬間から、**NotebookLMに渡すソース束＋プロンプトの2点セット**を1パスで完成させる。

memory feedback_slide_generation_via_notebooklm 準拠:
- **Marp/Slidev等で直接スライドを生成しない**
- 成果物は「ソース束＋プロンプト」の2点セット
- NotebookLMがスライド本体を生成

## 起動条件

以下のいずれかが含まれる発言で起動:
- 「スライド作って」「スライドを作って」「プレゼン資料」
- 「市政報告会のスライド」「自治会総会のスライド」「業界団体集会のスライド」
- 「後援会総会のスライド」「議会報告会のスライド」「報告会の資料」
- 「NotebookLM資料準備」「NotebookLMで作る」「NotebookLM用に」
- 「slide-deck-prep」「スライドキット」
- 「報告会のスライド」「集会の資料」

ただし以下は他skill/agentに委譲:
- 「1〜10分の挨拶」→ aisatsu-prep skill
- 「街頭演説」→ daily-street-speech agent
- 「式典・祝辞・弔辞・基調講演」→ speech-writer agent
- 「議会一般質問の通告書」→ general-question-prep skill

## 入力（草川から取得・推定可能なものは推定）

1. **場面/団体名**（必須）— 例: 楠平尾自治会 / 亀山建設労働組合 / 草川後援会
2. **場面区分**（推定可）— 市政報告会 / 自治会総会 / 業界団体集会 / 後援会総会 / 議会報告会
3. **持ち時間**（必須）— 30分 / 45分 / 60分 / 90分
4. **テーマ/重点**（必須または提案）— 例: 防災 / 子育て / インフラ / 公共交通 / 太陽光条例
5. **聴衆属性**（推定可）— 一般市民 / 業界専門家 / 後援会員 / 自治会役員 / 若年層 / 高齢者
6. **開催日**（必須）— スケジューリング・直近ニュース反映用
7. **任意**: 会場の特性（人数規模、プロジェクター有無、配布資料併用 等）

## 処理フロー

### Step 1: ヒアリング・場面区分推定
入力から場面区分を推定（または草川に確認）：

| 区分 | 典型構成 | 持ち時間目安 | 関連DB |
|---|---|---|---|
| 市政報告会 | 議会報告→重点政策→質疑応答 | 60〜90分 | 🎤市政報告会DB |
| 自治会総会 | 来賓挨拶→市政状況→地区別話題 | 30〜45分 | 🏘️自治会別訪問DB |
| 業界団体集会 | 業界連動の市政→政策提言→展望 | 45〜60分 | 🤝組織・業界団体接触ログ |
| 後援会総会 | 1年振返り→重点政策→決意 | 60〜90分 | 後援会DB |
| 議会報告会 | 議案賛否→一般質問報告→次期論点 | 30〜60分 | 📅ミーティングノートDB |

### Step 2: voice-dna読込

`~/.claude/agents/knowledge/kusagawa_archive/04_compass/voice-dna.md` を読み込み、トーン・常用語・NG表現・CTA レパートリーを把握。

### Step 3: ソース束自動収集（並列）

以下を並列で収集して `~/outputs/slide-deck-prep/<YYYY-MM-DD>_<テーマ>/sources/` に保存：

#### 3-A. 一次資料スキャン（WebFetch / kameyama-researcher agent）
- 亀山市公式サイト：該当テーマの計画書・統計・条例
- 三重県公式サイト：関連県施策
- 国の最新動向：sources.yaml（policy-radar）参照、関連省庁の直近3か月発表

#### 3-B. archive grep（草川過去発言）
```bash
grep -rl "<テーマキーワード>" ~/.claude/agents/knowledge/kusagawa_archive/{01_council,02_publications,03_themes,05_resources,06_election}/
```
- 該当する 03_themes/*.md は全文
- 01_council/ から該当議事録の草川発言＋市答弁ペアのみ（他議員ブロックスキップ）
- 02_publications/ から該当ブログ・市政報告

#### 3-C. 関連発信（blog/SNS）
- Notion 📰ブログ・SNS投稿管理DB から該当テーマの既発信を取得
- 直近6か月の発信実績を「実績エビデンス」として収集

#### 3-D. 地区別関係性メモ（自治会総会の場合のみ）
- 🏘️自治会別訪問DB から該当自治会の過去訪問記録・要望事項
- 過去の市政報告会原稿（あれば）

#### 3-E. 業界別蓄積（業界団体集会の場合のみ）
- 🤝組織・業界団体接触ログから該当団体の過去接触
- 業界特有の制度・補助金・統計

#### 3-F. 直近ニュース（policy-radar / news-briefing連携）
- 開催日から逆算して直近2週間の関連ニュース
- 直近の議会動向（議案・条例制定状況）

### Step 4: テンプレート選択

`templates/<場面区分>.md` を読み込んで、章立てテンプレを取得：

- `templates/shisei_houkokukai.md`
- `templates/jichikai_soukai.md`
- `templates/gyokai_dantai.md`
- `templates/kouenkai_soukai.md`
- `templates/giji_houkokukai.md`

テンプレは「章名 → スライド枚数目安 → 中身要件」のフォーマット。

### Step 5: NotebookLMマスタープロンプト生成

`prompts/notebooklm_master.md` をベースに、収集したソース束情報・テンプレ情報・voice-dna要素を組み込んで完成プロンプトを生成。

出力: `~/outputs/slide-deck-prep/<YYYY-MM-DD>_<テーマ>/notebooklm_prompt.md`

### Step 6: 安全ゲート（必須）

ソース束本体（一次資料）はチェック対象外だが、**プロンプト内に含まれる引用・要約・固有名詞**は以下を通す：

1. **content-fact-checker** — 数値・固有名詞・計画名・条例名の一次情報照合
2. **content-risk-reviewer** — 8軸スキャン（公選法・個人情報・名誉毀損・差別・利益相反・品位・物議・他議員氏名）

特に注意:
- **他議員氏名禁止**（feedback_no_other_council_members_names） — 議事録引用時に「○○議員」表記が混入していないかチェック
- **架空エピソード禁止**（feedback_no_fabricated_stories）
- **議会・他議員への提言色禁止**（feedback_no_council_directed_proposals）— 提言は執行部宛のみ
- **禁止フレーズ**（kameyama_context.md「やらないこと」）— 「届かないを終わらせる」「最後の100m」等

### Step 7: 完成パッケージ提示

草川に以下の形式で完成パッケージを提示：

```
## 🎤 slide-deck-prep 完成

【会場】 <団体名>
【場面区分】 <区分>
【持ち時間】 <分>
【テーマ】 <テーマ>
【開催日】 <日付>

【ソース束】 ~/outputs/slide-deck-prep/<YYYY-MM-DD>_<テーマ>/sources/ 配下に <件> ファイル
  - 一次資料: <件>
  - archive: <件>
  - 過去発信: <件>
  - 地区/業界蓄積: <件>
  - 直近ニュース: <件>

【NotebookLM プロンプト】 ~/outputs/slide-deck-prep/<YYYY-MM-DD>_<テーマ>/notebooklm_prompt.md
  - 章立て: <章数> 章 / 推定 <枚数> 枚
  - voice-dna整合: ✅
  - 安全ゲート: ✅ fact-checker / ✅ risk-reviewer

【次の手順】
1. ~/outputs/slide-deck-prep/<日付>_<テーマ>/sources/ 配下のファイルをNotebookLMにアップロード
2. notebooklm_prompt.md の内容をNotebookLMにペースト
3. NotebookLMがスライド生成 → 草川がレビュー
4. 必要に応じて print-designer skill で配布資料化

【保存先振分け】
- A: 🎤市政報告会DB に登録（市政報告会の場合）
- B: 🏘️自治会別訪問DB に登録（自治会総会の場合）
- C: 🤝組織・業界団体接触ログに追記（業界団体集会の場合）
- D: 📅ミーティングノートDB に登録（議会報告会・後援会総会の場合）
- E: スキップ（~/outputs/slide-deck-prep/ ファイルのみ保存）

A〜Eで指示してください（複数可、例: A,D）。
```

### Step 8: 草川指示後のNotion保存

指示に応じてNotion DBに登録：
- タイトル先頭🎤付き
- リレーション: 会議体マスタ／自治会マスタ／組織マスタ
- 標準プロパティ（場面/日付/担当者/状態）
- 本文: ~/outputs/slide-deck-prep/ ファイルへのリンク + 章立てサマリ

## 設定ファイル

- `templates/<場面区分>.md` — 場面別の章立てテンプレ
- `prompts/notebooklm_master.md` — NotebookLM向けマスタープロンプト
- `~/outputs/slide-deck-prep/<日付>_<テーマ>/` — 場面ごとのソース束＋プロンプト一式

## 関連skill/agent

- `aisatsu-prep` — 1〜10分の短尺挨拶（本スキルとは別物）
- `community-rally-speaker` agent — 自治会総会・地区集会向けアジテーション原稿
- `speech-writer` agent — 式典・祝辞・弔辞・基調講演
- `print-designer` agent — 配布資料・チラシのHTML/CSS実装
- `photo-curator` agent — スライド・配布資料用の写真選定
- `policy-radar` skill — 直近の政策動向ソース取得
- `news-briefing` skill — 直近ニュースソース取得
- `kameyama-researcher` agent — 亀山公式サイトからの最新一次資料取得

## 関連DB

| DB | 用途 |
|---|---|
| 🎤市政報告会DB | 市政報告会の開催記録 |
| 🏘️自治会別訪問DB | 自治会総会・地区別市政報告会 |
| 🤝組織・業界団体接触ログ | 業界団体集会 |
| 📅ミーティングノートDB | 議会報告会・後援会総会 |
| 会議体マスタ | 全ての場面に共通 |

## 運用ルール（CLAUDE.md準拠）

- **議事録参照**: 草川発言＋市答弁ペアのみ（他議員ブロックはスキップ、voice-dna汚染防止）
- **架空エピソード禁止**: 「ある市民が泣いた」型は出さない、実体験/一次情報/公式データのみ
- **議会・他議員への提言色禁止**: 提言の宛先は執行部に限定
- **タイトル50字以内**（Notion保存時）
- **PDFバイナリは pdftotext**（WebFetch失敗時の標準フロー）
- **個人情報除外**: 市民相談で得た固有名詞は使わない（具体性は「ある保護者から」等の汎化）
- **公選法配慮**: 選挙公示後はスキップ、公示前でも投票依頼・寄附該当表現を含めない

## トラブルシュート

- **NotebookLMにアップロードしてもスライドが生成されない** → プロンプトの構造（章立て・スライド枚数指定）が曖昧、prompts/notebooklm_master.md を修正
- **生成されたスライドのトーンが草川らしくない** → voice-dna要素のプロンプト組込が不足、テンプレに具体例追加
- **古い情報源が混ざる** → archive grep の日付絞り込みが緩い、直近12か月優先に変更
- **章立てが場面に合わない** → templates/<場面区分>.md を修正

## 設計者メモ

- 本スキルの肝は「**ソース束の質**」。NotebookLMはソースが命なので、ソース集めで手を抜くと出力品質が崩れる。
- 「**1スライド1メッセージ**」原則をプロンプトで強制（NotebookLMがcompound化しないように）
- 「**数字・固有名詞・人名・期日**」をプロンプトに必ず含める（抽象化しすぎ防止）
- 写真・図表が必要な場合は別途 photo-curator / nanobanana-prompt-designer agent を呼ぶ
- 配布資料化が必要な場合は print-designer agent に渡す
- 章立てが「議会報告→政策→決意」の3部構成に偏らないよう、テーマや聴衆に応じて柔軟に変更
