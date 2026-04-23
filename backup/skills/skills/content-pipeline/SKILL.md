---
name: content-pipeline
description: コンテンツパイプライン。録音ファイル・文字起こし・テキストなど任意のインプットから、ブログ記事・SNS投稿文（Twitter/X、Instagram、Facebook、Threads）を一括生成し、Notionに自動保存する。以下のような状況で必ず使用すること：「録音をアップした」「文字起こしがある」「ポッドキャストの内容をコンテンツ化したい」「テキストからブログとSNSを作りたい」「コンテンツパイプライン」など、既存の素材から複数のコンテンツフォーマットへの変換が求められる場合は、ユーザーが明示的にスキル名を挙げなくても積極的に発動すること。
---

# コンテンツパイプライン

録音・文字起こし・テキストなど「生の素材」を受け取り、公開可能なコンテンツ一式を自動生成するパイプライン。

## エージェント構成

このスキルは以下の8エージェント＋1参照ファイルをオーケストレートする：

| エージェント | 担当ステップ | 役割 |
|---|---|---|
| `policy-researcher` | Step 0-2 / Step 1.5 | 国の動向・他自治体先進事例・統計データ調査 |
| `kameyama-researcher` | Step 1.5 | 亀山市公式情報・議会議事録・三重県施策調査 |
| `council-material-creator` | Step 0-3/0-4 | 一般質問の論点整理・質問原稿作成（深掘りモード時） |
| `blog-writer` | Step 2（深掘りモード） | 草川たくや名義のブログ記事生成（1500〜2500字・5段構成・政策論） |
| `blog-writer-normal` | Step 2（ノーマルモード） | 草川たくや名義の市民向けブログ記事生成（800〜1500字・柔軟構成・読みやすさ重視） |
| `content-editor` | Step 2.5 / 3.5 | **品質ゲート**（ブログ・SNSを5軸スコアリング・不合格時は差し戻し） |
| `sns-content-creator` | Step 3 | SNS投稿文生成（Threads/X/Instagram/Facebook/LINE/YouTube/TikTok） |
| `kusakawa-voice-analyst` | 初回起動・任意 | 過去の公開投稿から声のDNAを抽出し `references/voice-dna.md` に保存 |
| `notion-saver` | Step 5 | Notionへの確実な保存（コンテンツページ＋ネタDB） |

**重要な参照ファイル**:
- `references/voice-dna.md` — 草川たくやの声の指紋（常用語・NG表現・文体癖・CTAレパートリー）。blog-writer / sns-content-creator / content-editor が**必ず読み込んでから作業する**

エージェントの詳細定義: `agents/` ディレクトリ参照

---

## インプットの受け取り方と起動モードの判定

ユーザーが提供するものに応じて柔軟に対応する：

- **ファイル（録音・テキスト）**: Read ツールで読み込む
- **文字起こしテキスト / 貼り付けテキスト**: そのまま処理する
- **URLや参照**: WebFetchでコンテンツを取得する
- **「こうすればよいのでは」「〜が気になる」などの仮説・アイデア**: → **ステップ 0（テーマ深掘りモード）**を起動する

**モード判定ルール**:
- まとまった素材がある → ステップ1へ進む
- 素材が「仮説・着眼点」の段階 → ステップ0から対話形式で深掘り

---

## ステップ 0: テーマの深掘り（仮説・アイデアから出発する場合）

### ステップ0-1: 仮説の深掘りと課題の明確化

「現在気になっていること、あるいは『こうすればもっと良くなるのでは？』と直感的に思っていることは何ですか？」とユーザーに尋ねる。

ユーザーが答えたら、以下の視点から確認して課題の解像度を上げる：
- 具体的に誰が（どの年代・属性・地域の人が）一番困っているか
- なぜこれまで放置されてきた（または実現しなかった）と思うか
- 亀山市のどの分野・担当課に紐づくか（教育・福祉・防災・産業・交通・環境など）
- 市民からの相談・現場での気づきがあればその具体的な内容

---

### ステップ0-2: 徹底した実態調査

**policy-researcherエージェントとkameyama-researcherエージェントを並列起動する。**

```
Agent(subagent_type="policy-researcher",
  prompt="以下のテーマについて調査してください。
  テーマ: {theme}
  調査内容:
  1. 国の政策・法制度の最新動向（法律名・通知名・年月日を明記）
  2. 統計データ（全国・三重県・亀山市の比較）
  3. 先進自治体の具体的な取り組み事例（最低3自治体・人口4.5万人規模優先）
     - 何をどんな予算・体制で・いつから・どんな効果が出たか
  4. 失敗事例・中止事例も調査すること
  議員が議場で使える具体的な数値・固有名詞・出典を揃えること。")

Agent(subagent_type="kameyama-researcher",
  prompt="テーマ「{theme}」について亀山市の現状を調査してください。
  agents/kameyama-researcher.md の手順に従い、以下を返してください:
  - 亀山市の現状・既存施策・担当課
  - 議会での過去の議論（草川たくや議員の質問含む）
  - 三重県レベルの関連動向
  - 政策提言の核心（あるべき姿とのギャップ）")
```

両エージェントの結果を統合して内部メモとして保持する。

---

### ステップ0-3: 一般質問の論点整理と戦略設計

**council-material-creatorエージェントに委託する。**

```
Agent(subagent_type="council-material-creator",
  prompt="以下の調査結果を踏まえ、亀山市議会での一般質問の論点整理と質問戦略を設計してください。
  
  調査結果:
  {policy_researcher_result}
  {kameyama_researcher_result}
  
  設計内容:
  1. 質問の骨組み（4段構成）
  2. 執行部の反応予測と切り返し戦略（表形式）")
```

ユーザーに論点整理を提示し、合意を得てからステップ0-4へ進む。

---

### ステップ0-4: 質問原稿のドラフト作成

**council-material-creatorエージェントに委託する（ステップ0-3に続けて依頼）。**

調査した実数値・事例・法令を根拠として盛り込み、再質問3〜5本を含む原稿を作成する。

---

### ステップ0-5: さらなる深掘りへの投げかけ（必須）

質問原稿を提示した後、以下のフォーマットで5〜7つの問いを提示してから止まる。ユーザーの回答を受け取るまでステップ1以降には進まない。

```
---

## 🔍 さらに深掘りするための問い

調査と原稿を踏まえて、以下の視点もあわせて検討してみてください。

**① [問い1のテーマ]**
[問いの内容と、なぜこの視点が重要かの短い説明]

**② [問い2のテーマ]**
[問いの内容と背景]

（③〜⑦まで続ける）

---
どの視点が気になりましたか？深掘りが終わったら、「ブログとSNSを作って」と教えてください。
```

---

## ステップ 1: 深掘り分析

素材全体を読み込み、以下を内部メモとして整理する（ユーザーへの出力不要）：
- コアメッセージ（最重要アイデア1〜2つ）
- ターゲット読者
- 使えるデータ・エピソード・引用
- 最もインパクトある切り口

---

## ステップ 1.5: 亀山市ローカル調査（必須）

**policy-researcherとkameyama-researcherを並列起動する。**

```
Agent(subagent_type="policy-researcher",
  prompt="以下のテーマに関して他自治体の先進事例を調査してください。
  テーマ: {素材のテーマキーワード}
  - 人口4.5万人規模の自治体の事例を優先
  - 取り組み内容・予算・開始時期・効果を具体的に
  - 国の政策動向・法制度も併せて調査")

Agent(subagent_type="kameyama-researcher",
  prompt="テーマ「{素材のテーマキーワード}」について亀山市の現状を調査してください。
  agents/kameyama-researcher.md の手順に従い構造化して返してください。")
```

両結果を統合し、コンテンツ生成の骨格とする。

---

## ステップ 2-0: ブログ執筆モードの確認（必須・ユーザーに質問）

**ブログ生成に入る前に、必ずユーザーに以下の2択を提示して選んでもらう。** ユーザーの回答を得るまでステップ 2 には進まない。

```
---

## 📝 ブログ記事のモード確認

このテーマをブログ記事にします。どちらのモードで書きますか？

**① 深掘りモード（blog-writer）**
1500〜2500字・5段構成・政策論型。数値や制度名を多用し、議会でも引用できる骨太の論考。政策に関心のある層向け。

**② ノーマルモード（blog-writer-normal）**
800〜1500字・柔軟な構成・読みやすさ重視。専門用語を避け、小学生から高齢者まで読める親しみやすい報告型。普段政治に関心のない層向け。

**①深掘り / ②ノーマル** のどちらで書きますか？
---
```

ユーザーが選んだモードを `blog_mode` 変数として保持し、ステップ 2 に進む。

⚠️ 確認をスキップしない。毎回必ず聞く。深掘りとノーマルでは読者層も情報密度も大きく異なるため、勝手に判断せずユーザー判断を仰ぐ。

---

## ステップ 2: ブログ記事の生成

`blog_mode` の値に応じて **blog-writer（深掘り）** または **blog-writer-normal（ノーマル）** に委託する。

### 2-A. 深掘りモード（blog_mode = 深掘り）

**blog-writerエージェントに委託する。** agents/blog-writer.md と references/voice-dna.md の両方に従うよう明示する。

```
Agent(subagent_type="blog-writer",
  prompt="以下の情報をもとに草川たくや名義のブログ記事を生成してください。
  必ず references/voice-dna.md を読み込み、agents/blog-writer.md の5段構成・ファクト基準・NG表現リスト全てに従うこと。
  
  テーマ: {theme}
  元素材: {source_title} / {source_url} / {source_date}
  
  policy-researcher調査結果:
  {policy_researcher_result}
  
  kameyama-researcher調査結果:
  {kameyama_researcher_result}
  
  市民の生の声（あれば）:
  {citizen_voice}
  
  要件（blog-writer.md の詳細は必読）:
  - タイトルは `【草川たくや 亀山市】` から始めるか、セリフ引用型（voice-dna.md §1）
  - `——` ダブルダッシュをタイトル副題・本文転換で使う
  - 5段構成厳守: ①現場の声 →②全国データ →③国の制度 →④亀山市でできること →⑤議会アクション宣言
  - `## 📌` 見出しで本文を3〜4セクション構造化
  - ファクト最低点数: 数値5・地名3・法令2・日付3・固有機関2
  - 1500〜2500字
  - 定型フッターを末尾に正確に挿入")
```

### 2-B. ノーマルモード（blog_mode = ノーマル）

**blog-writer-normalエージェントに委託する。** agents/blog-writer-normal.md と references/voice-dna.md の両方に従うよう明示する。

```
Agent(subagent_type="blog-writer-normal",
  prompt="以下の情報をもとに草川たくや名義の市民向けブログ記事（ノーマル版）を生成してください。
  必ず references/voice-dna.md を読み込み、agents/blog-writer-normal.md の構成指針・ファクト基準（緩め）・NG表現リストすべてに従うこと。
  
  テーマ: {theme}
  元素材: {source_title} / {source_url} / {source_date}
  
  policy-researcher調査結果（要点だけ抽出して使う）:
  {policy_researcher_result}
  
  kameyama-researcher調査結果（要点だけ抽出して使う）:
  {kameyama_researcher_result}
  
  市民の生の声（あれば）:
  {citizen_voice}
  
  添付メディア（あれば配置指示を本文に入れる）:
  {attachments}
  
  要件（blog-writer-normal.md の詳細は必読）:
  - タイトル冒頭に `【草川たくや 亀山市】` を必ず付ける（またはセリフ引用型）・50字以内
  - 一人称「私」で市民に語りかける誠実で丁寧なトーン
  - 構成は柔軟（3〜4セクション目安・5段構成は強制しない）
  - 専門用語は避け、使う場合は必ず平易な言い換えを括弧書きで添える
  - ファクト密度は控えめ（数値2〜3個・地名1〜2個程度。過密禁止）
  - 本文中に市民への問いかけまたは意見募集の一文を必ず含める
  - 800〜1500字
  - 定型フッターを末尾に正確に挿入
  - ハルシネーション厳禁")
```

---

## ステップ 2.5: ブログ記事の品質レビュー（必須）

**content-editorエージェントに委託する。** blog-writerの出力が公開レベルに達しているか5軸で判定する。

```
Agent(subagent_type="content-editor",
  prompt="以下のブログ原稿をレビューしてください。agents/content-editor.md の5軸スコアリングを適用。
  
  content_type: blog
  blog_mode: {blog_mode}   # 深掘り or ノーマル。ノーマルの場合はファクト密度より読みやすさ・問いかけ・親しみやすさを重視して採点
  draft: {blog_writer_output}
  research_summary: {policy_researcher_result + kameyama_researcher_result}
  voice_dna: references/voice-dna.md を読み込む
  revision_count: 0
  
  JSON形式で結果を返してください。")
```

**判定に応じた分岐**:
- **pass（total 18+）** → ステップ 3 に進む
- **revise（total 13-17）** → blog-writer または blog-writer-normal（`blog_mode` に応じて）に revision_requests を渡して再生成 → 再度 content-editor レビュー（revision_count=1）
- **major_revise（total 0-12）** → research_summary の再取得を検討。該当する blog-writer 系エージェントに詳細フィードバックを渡して再生成
- **2周してもrevise** → `human_review_flag: true` として現状ベストをユーザーに提示し「人間レビュー必要」と伝えてステップ3以降に進む

---

## ステップ 3: SNS投稿文の生成

**sns-content-creatorエージェントに委託する。** 必ず references/voice-dna.md を読み込ませ、媒体ごとの切り口差別化を指示する。

```
Agent(subagent_type="sns-content-creator",
  prompt="以下のブログ記事・研究結果をもとに、草川たくや名義のSNS投稿文を生成してください。
  必ず ~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/content-pipeline/references/voice-dna.md を読み込み、声の指紋を完全に反映すること。
  
  テーマ: {theme}
  ブログ記事: {blog_content}
  policy-researcher調査結果: {policy_researcher_result}
  kameyama-researcher調査結果: {kameyama_researcher_result}
  亀山市の文脈: {kameyama_context}
  市民の声（あれば）: {citizen_voice}
  
  生成するメディア（7種類全部）: Threads・X（旧Twitter）・Instagram・Facebook・公式LINE・YouTube・TikTok/YouTubeショート
  
  必須要件（sns-content-creator.md の詳細は必読）:
  - 媒体ごとに切り口を変える（使い回し禁止）
  - 各媒体にresearch_summaryの具体数値・地名・固有名詞を最低1点埋め込む（Instagramは3点以上）
  - Facebookは定型挨拶を使わず本題から直接入る（セリフ引用・現場エピソード・具体的問題提起のいずれか）
  - LINEは `こんにちは／こんばんは、草川たくやです。` で開始し `皆さんの声、これからもお聞かせください。` で終止
  - ハッシュタグは最大5つ厳守
  - NG定型句（断固・粉骨砕身・適切に対応してまいります等）は使わない
  - CTAを投稿間で被らせない")
```

---

## ステップ 3.5: SNS投稿文の品質レビュー（必須）

**content-editorエージェントに委託する。** 7媒体セットを一括で評価する。

```
Agent(subagent_type="content-editor",
  prompt="以下のSNS投稿文セット（7媒体）をレビューしてください。agents/content-editor.md の5軸スコアリングを適用。
  
  content_type: sns-bundle
  draft: {sns_content_creator_output}
  research_summary: {policy_researcher_result + kameyama_researcher_result}
  voice_dna: references/voice-dna.md を読み込む
  revision_count: 0
  
  各媒体を個別評価し、最も低い媒体のスコアを全体スコアとしてください。
  JSON形式で結果を返してください。")
```

**判定に応じた分岐**:
- **pass（total 18+）** → ステップ 5 に進む
- **revise（total 13-17）** → sns-content-creator に revision_requests を渡して再生成 → 再度レビュー（revision_count=1）
- **major_revise（total 0-12）** → 該当する媒体のみ再生成、または全面再生成
- **2周してもrevise** → `human_review_flag: true` として現状ベストをユーザーに提示しステップ5に進む（「人間レビュー必要」と明記）

---

## ステップ 5: Notionへの保存

**notion-saverエージェントに委託する。** 品質レビューの結果（合否・スコア・強み）もメモ欄に記録する。

```
Agent(subagent_type="notion-saver",
  prompt="以下のコンテンツをNotionに保存してください。
  agents/notion-saver.md の手順に従ってください。
  
  theme: {テーマ30字以内}
  source: {タイトル・URL・日付}
  field: {分野}
  priority: {優先度}
  department: {担当課（想定）}
  next_actions: {①②③形式の次アクション}
  target_session: {対象定例会}
  memo: {メモ・根拠 + 品質レビュースコア + ブログモード（深掘り or ノーマル）}
  
  blog_content:
  {ブログ記事全文}
  
  blog_review:
  {content-editor判定: pass/score/strengths}
  
  sns_content:
  {SNS投稿文7種全文}
  
  sns_review:
  {content-editor判定: pass/score/strengths}
  
  human_review_needed: {true/false}")
```

notion-saverから返されたURLを最終出力に含める。

**human_review_needed=true の場合**、Notion保存時にタイトル先頭に ⚠️ プレフィクスを付け、メモ欄に revision_requests を記載する。

---

## 出力のまとめ方

すべてのコンテンツをこの順で出力する。コンテンツ間に区切り線を入れること：

```
## ブログ記事
[blog-writerの出力全文]

**品質レビュー**: [content-editor判定（pass/revise）・スコア XX/25点・主な強み2点]

---

## SNS投稿文

【Threads】
【X（旧Twitter）】
【Instagram】
【Facebook】
【公式LINE】
【YouTube】
【TikTok / YouTubeショート】

**品質レビュー**: [content-editor判定・最低媒体スコア XX/25点・主な強み2点]

---

## Notion保存
**5-A) コンテンツページ**: [notion-saverから返されたURL]
**5-B) 一般質問ネタDB**: [notion-saverから返されたURL]

[human_review_needed=true の場合のみ]
⚠️ **人間レビュー必要**: 2周の自動リトライでも品質基準を満たせませんでした。以下の課題を確認してください:
- [content-editor の revision_requests を箇条書き]
```
