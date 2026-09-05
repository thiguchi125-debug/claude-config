---
name: content-pipeline
description: コンテンツパイプライン。録音・文字起こし・テキスト・ニュース記事URL・イベント情報・写真など任意の素材から、ブログ＋SNS7種（X/Threads/Instagram/Facebook/LINE/YouTube/TikTok）＋条件に応じてサムネ画像（アイキャッチ/OGP 1600×900）＋インスタ用ショート動画（Reels 9:16）まで一括生成し、安全ゲート通過後Notion・outputsに保存する。ブログ執筆モード（深掘り/ノーマル）は素材から自動判定。主要トリガー（短）：「発信一式」「発信セット」「一式作って」「フル展開して」「記事から発信」「これ全部作って」「ブログもSNSも動画も」。個別トリガー：「サムネ作って」「アイキャッチ作って」「インスタ用ショート動画作って」「コンテンツパイプライン」。後方互換：「録音をアップした」「文字起こしがある」「テキストからブログとSNSを作りたい」。素材を渡して複数フォーマットへの変換・発信物一式の制作が求められる場面は、スキル名が挙がらなくても発動する。※小さな種1つ→発信=spark、当日の全チャネル日次配信=daily-content-generatorが正で、本スキルは反応しない。
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
| `content-fact-checker` | Step 2.6 / 3.6 | **事実確認ゲート**（数値・固有名詞・法令を一次情報まで遡って検証） |
| `content-risk-reviewer` | Step 2.7 / 3.7 | **リスクレビューゲート**（公選法・個人情報・名誉毀損等の8軸精査・草川への問いかけ生成） |
| `sns-content-creator` | Step 3 | SNS投稿文生成（Threads/X/Instagram/Facebook/LINE/YouTube）※TikTok/Shorts台本は除く |
| `short-video-virality-architect` | Step 3 | **ショート動画（TikTok/Shorts/Reels）の台本＝主担当**。35〜50秒・目標45〜50秒厳守 |
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

## ステップ 2-0: ブログ執筆モードの自動判定（必須・提案→承認）

**素材の性質からモードを自動判定し、推奨モードを1行提示して草川の承認（またはワンタップ変更）を得る。** 白紙から毎回2択を聞くのではなく、AIが先に判定して提案する（2026-07-14 草川指示「毎回自動判定」）。

**自動判定ルール**:
- **ノーマルモード（blog-writer-normal）を推奨** ← 地域イベント告知・活動報告・お知らせ・現場レポート・市民向けの柔らかい話題（例：種まきイベント紹介・お祭り・視察報告・写真付きの現場報告）。判断語感＝「紹介」「告知」「報告」「お知らせ」「参加呼びかけ」。
- **深掘りモード（blog-writer）を推奨** ← 政策論・制度課題・議会論点・データ分析型（例：子育てDX・公共交通・防災政策）。判断語感＝「政策」「課題」「提言」「〜のあり方」「議会で問う」。
- 判定が拮抗する素材は**ノーマルを既定の推奨**にする（読者層が広く安全側）。

提示フォーマット（1行・承認前提）:
```
このテーマは【ノーマルモード（市民向け・800〜1500字・活動報告型）】で書くのが最適と判断しました。
このまま進めます。深掘り政策論考（1500〜2500字）にしたい場合は「深掘りで」とだけ返してください。
```

草川が何も指定しなければ推奨モードで進行、「深掘りで」「ノーマルで」で上書き。確定したモードを `blog_mode` 変数として保持し、ステップ 2 に進む。

⚠️ 「勝手に確定して生成完了まで走る」のではなく、推奨提示の直後にモードを確定してステップ2へ（軽い1往復。往復を増やさないためAskUserQuestionは使わず地の文で提示）。

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
- **pass（total 18+）** → ステップ 2.6 に進む
- **revise（total 13-17）** → blog-writer または blog-writer-normal（`blog_mode` に応じて）に revision_requests を渡して再生成 → 再度 content-editor レビュー（revision_count=1）
- **major_revise（total 0-12）** → research_summary の再取得を検討。該当する blog-writer 系エージェントに詳細フィードバックを渡して再生成
- **2周してもrevise** → `human_review_flag: true` として現状ベストをユーザーに提示し「人間レビュー必要」と伝えてステップ2.6以降に進む

---

## ステップ 2.6: ブログ記事の事実確認（必須）

**content-fact-checkerエージェントに委託する。** 一次情報まで遡って数値・固有名詞・法令等を検証する。

```
Agent(subagent_type="content-fact-checker",
  prompt="以下のブログ原稿について、含まれるすべての事実主張を一次情報まで遡って検証してください。
  agents/content-fact-checker.md の手順に従って、5カテゴリ（数値/固有名詞/法令/議会・行政/他自治体）を網羅的に検証。
  
  content_type: blog
  draft: {blog_content_after_quality_review}
  research_summary: {policy_researcher_result + kameyama_researcher_result}
  theme: {theme}
  
  必ずWebFetch等で公式ソース（亀山市公式・e-Gov法令検索・各省庁等）を直接確認すること。
  research_summary の数字をそのまま信じてはいけない。
  検証結果を APPROVE / REVISE / REJECT で返してください。")
```

**判定に応じた分岐**:
- **APPROVE（INCORRECT 0件・MINOR 2件以下・UNVERIFIED 3件以下）** → ステップ 2.7 に進む
- **REVISE** → fact-checkerの修正指示をblog-writer系に渡して該当箇所のみ修正→再走行（最大2周）
- **REJECT（HALLUCINATION 3件以上 or 法令条数誤り）** → 人間レビュー必要フラグを立て草川に通知。SNS生成停止
- **2周してもREVISE** → `human_review_flag: true` で2.7に進む（草川判断を仰ぐ）

---

## ステップ 2.7: ブログ記事のリスクレビュー（必須）

**content-risk-reviewerエージェントに委託する。** 議員発信物としての物議・問題化リスクを8軸で評価する。

```
Agent(subagent_type="content-risk-reviewer",
  prompt="以下のブログ原稿について、議員発信物としての物議・問題化リスクを8軸で評価してください。
  agents/content-risk-reviewer.md の手順に従って、個人情報/機密/公選法/名誉毀損/差別/利益相反/品位/政治物議の各軸を精査。
  
  content_type: blog
  draft: {blog_content_after_fact_check}
  theme: {theme}
  context: {通常期 / 選挙期間中 / 議会会期中 等}
  fact_check_result: {ステップ2.6の結果}
  
  HIGH以上のリスクが検出された場合は草川への問いかけを生成。
  判定: APPROVE / REVISE / ASK_USER / REJECT")
```

**判定に応じた分岐**:
- **APPROVE** → ステップ 3 に進む
- **REVISE（MEDIUMのみ）** → 推奨修正案を blog-writer に渡して修正→再走行
- **ASK_USER（HIGH検出）** → **草川に問いかけて判断を仰ぐ**。ユーザー応答を待ってから次ステップ進行を決定
- **REJECT（CRITICAL検出）** → **即停止**。SNS生成・保存ともに進めず、草川に重大リスクを通知して差し戻し

---

## ステップ 3: SNS投稿文の生成

### ⛔ ショート動画台本は別委託（必須・skip禁止）

7種のうち **TikTok/YouTubeショートの台本だけは `sns-content-creator` に書かせない**。
必ず `short-video-virality-architect`（モード=SOLO）へ委譲する。草川基準＝**35〜50秒・目標45〜50秒厳守・1動画1メッセージ・数値羅列禁止**。
素朴生成の長尺（60秒級・数字詰め込み）は本人NGが確定している。
詳細＝memory/feedback_short_video_use_virality_architect_first.md

```
Agent(subagent_type="short-video-virality-architect",
      prompt="モード=SOLO／テーマ・fact束・voice-dna／草川基準=35〜50秒・目標45〜50秒厳守・1動画1メッセージ")
```

**sns-content-creatorエージェントに委託する。** 必ず references/voice-dna.md を読み込ませ、媒体ごとの切り口差別化を指示する。

```
Agent(subagent_type="sns-content-creator",
  prompt="以下のブログ記事・研究結果をもとに、草川たくや名義のSNS投稿文を生成してください。
  必ず ~/.claude/agents/knowledge/kusagawa_archive/04_compass/voice-dna.md（声のDNA正本）を読み込み、声の指紋を完全に反映すること。
  
  テーマ: {theme}
  ブログ記事: {blog_content}
  policy-researcher調査結果: {policy_researcher_result}
  kameyama-researcher調査結果: {kameyama_researcher_result}
  亀山市の文脈: {kameyama_context}
  市民の声（あれば）: {citizen_voice}
  
  生成するメディア（6種類）: Threads・X（旧Twitter）・Instagram・Facebook・公式LINE・YouTube
  ※ **TikTok/YouTubeショートの台本は sns-content-creator に書かせない**。7枠目は別途 `short-video-virality-architect` へ委譲する（下記）
  
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
- **pass（total 18+）** → ステップ 3.6 に進む
- **revise（total 13-17）** → sns-content-creator に revision_requests を渡して再生成 → 再度レビュー（revision_count=1）
- **major_revise（total 0-12）** → 該当する媒体のみ再生成、または全面再生成
- **2周してもrevise** → `human_review_flag: true` として現状ベストをユーザーに提示しステップ3.6に進む（「人間レビュー必要」と明記）

---

## ステップ 3.6: SNS投稿文の事実確認（必須）

**content-fact-checkerエージェントに委託する。** 7媒体セットすべての事実主張を検証する。

```
Agent(subagent_type="content-fact-checker",
  prompt="以下のSNS投稿文セット（7媒体）について、各媒体の事実主張を一次情報まで遡って検証してください。
  agents/content-fact-checker.md の手順に従う。
  
  content_type: sns-bundle
  draft: {sns_content_after_quality_review}
  research_summary: {policy_researcher_result + kameyama_researcher_result}
  theme: {theme}
  
  注意: ブログ（ステップ2.6で検証済）と同じ数値・固有名詞を流用しているSNS投稿は、
  そのまま継承可とする（重複検証スキップ）。SNS独自の主張のみ重点検証。
  
  判定: APPROVE / REVISE / REJECT")
```

**判定に応じた分岐**:
- **APPROVE** → ステップ 3.7 に進む
- **REVISE** → sns-content-creator に修正指示を渡して該当媒体のみ再生成→再走行
- **REJECT** → 人間レビュー必要フラグ。3.7に進む（草川判断）

---

## ステップ 3.7: SNS投稿文のリスクレビュー（必須）

**content-risk-reviewerエージェントに委託する。** 7媒体セットを多軸で精査する。

```
Agent(subagent_type="content-risk-reviewer",
  prompt="以下のSNS投稿文セット（7媒体）について、議員発信物としての物議・問題化リスクを8軸で評価してください。
  agents/content-risk-reviewer.md の手順に従う。
  
  content_type: sns-bundle
  draft: {sns_content_after_fact_check}
  theme: {theme}
  context: {通常期 / 選挙期間中 / 議会会期中 等}
  fact_check_result: {ステップ3.6の結果}
  
  特にX（短文の断定）・Threads（カジュアルな表現）でリスクが顕在化しやすい。
  各媒体個別に評価し、最もリスクの高い媒体を全体判定の基準とする。
  
  判定: APPROVE / REVISE / ASK_USER / REJECT")
```

**判定に応じた分岐**:
- **APPROVE** → ステップ 5 に進む
- **REVISE（MEDIUMのみ）** → sns-content-creator に修正案を渡して該当媒体のみ修正→再走行
- **ASK_USER（HIGH検出）** → **草川に問いかけて判断を仰ぐ**。ユーザー応答後に次ステップ進行を決定
- **REJECT（CRITICAL検出）** → **即停止**。保存進めず、該当媒体を差し戻し or 削除

---

## ステップ 4: 発信ビジュアル（サムネ画像・ショート動画）— 条件付き

**発動条件**（いずれか）: ①素材がイベント告知・活動報告など視覚訴求向き ②写真が添付されている ③草川が「サムネ作って」「動画も」「インスタ用ショート」等と指示。該当しなければ本ステップはスキップしてステップ5へ。

該当時は**何を作るかを1行で確認**（例:「アイキャッチ用サムネ(1600×900)とインスタ用ショート動画(9:16)も作ります。よいですか？」）してから、`references/visual-assets-playbook.md` の手順で制作する。要点のみ再掲（詳細は必ず playbook を読む）:

### 4-A. サムネ画像（ブログのアイキャッチ / OGP / SNSカード）
0. **採寸を先に確定**: `~/.claude/scripts/specs.json` の `image.16:9`（読み込み口 `specs.py`）から判型・セーフ域・最小級数を読み、見出し級数・写真の切り取り枠・要素座標を**着手前に書き出す**。HTMLはその数値で書く。
1. **草川に写真の有無を聞かない。** photo-curator（ZPERSON=18）を起動してこちらで選び切る。テーマに合う写真が無いときだけタイポ＋モチーフ主体に落とし、事後に一行で報告する（2026-09-04 改訂）。顔は画面高25〜35%。
2. HTML/CSS→Chrome headless→PNG（**1600×900**・2倍版は3200×1800）。プロ級和文タイポ（ヒラギノW8/W9・`font-feature-settings:"palt"`・草川カラー #1f5a3a/#e0357a）。絵文字禁止（[[feedback_no_emoji_ai_smell]]・タイポ規範＝design_system/references/thumbnail/_karte.md）。
3. **機械採点が通るまで目視しない**: `python3 ~/.claude/scripts/check_overflow.py --canvas 1600x900 <html>` → `feed_preview.py still <png>`。FAILは数値を直して再レンダ。
4. **目視は最後の1回**（PNGを自分でRead）。破綻（見切れ・はみ出し・可読性）があれば数値を直して再レンダ→再度3から。勝負所のみ 4-B2 の feed-visual-reviewer。

### 4-B. ショート動画（Instagram Reels / TikTok / YouTube ショート）
1. 提供写真を ffmpeg autorotate で正立化 → コンタクトシート1枚を自Readして向き・内容をマッピング（縦写真は9:16フル、横写真は中央9:16クロップ）。人物・全景の取り違え防止に必ずRead（正本＝skills/photo-post/SKILL.md 📌節）。
2. テキストカードは透過PNG（1080×1920・Chrome headless・スクリム付き・ヒラギノ・Reels安全域=上下UI帯を避ける）。写真に overlay。
3. ffmpeg で各セグメント（≈2.8秒・ゆるやかKen Burnsズーム）→ concat →前後フェード。重い4Kズームは避け `-preset veryfast` で。合成フレームのコンタクトを自Readして可読性確認（EYES-FIRST）。
4. 音声は付けない（IGアプリ内で音楽追加を推奨と添える）。

### 4-B2. 配信面ゲート（必須・skip禁止）

原寸で破綻ゼロは合格の半分。**確定前に必ず縮小して読者の目で見る。**

```bash
python3 ~/.claude/scripts/feed_preview.py still <サムネ.png>      # 静止画
python3 ~/.claude/scripts/feed_preview.py short <カバー.png> ...  # 9:16
```
→ 出た1枚を持って **`feed-visual-reviewer`** を起動し `PASS` を取る。`FIX`／`REBUILD` なら直して再度通す。詳細＝`references/visual-assets-playbook.md` A-4。

### 4-C. 安全ゲート（サムネ・動画とも）
- 画像・動画に載る**文言**は content-fact-checker → content-risk-reviewer を通す。ただしブログ（2.6/2.7）と**同一事実・同一表現の流用は継承可**（重複検証スキップ）。動画/画像独自の新規主張・人物写真の写り込み（他者の顔・実名のぼり以外の第三者）のみ重点確認。公選法の寄附/おもてなし表現・他議員名なしを最終確認。

### 4-D. 保存
- サムネPNG: `~/outputs/thumbnails/<日付>_<テーマ>/`
- ショート動画一式: `~/outputs/short-video/<日付>_<テーマ>/`（完成mp4はスマホ編集用に Drive `📱動画素材` ミラーも検討）
- いずれも絶対パス（cwd依存禁止）。完成物は `open` で草川に提示。

---

## ステップ 5: Notionへの保存

⚠️**締めガード（必須）**: 生成した発信物は**チャット提示で終わらせず必ずNotion保存まで完了**させる。ブログ→📝ブログ/投稿管理DB、**SNS7種→📣SNS投稿管理DB（ds `1bd98deb-624f-402c-aeb3-bdaa4782b389`）へ1ページ**。手動オーケストレーション時も同様。ブログだけ保存してSNSを保存し忘れる事故があった（2026-07-14）。保存漏れゼロを最終確認してから完了報告する。

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

## 発信ビジュアル（ステップ4を実施した場合のみ）
- **サムネ画像**: [PNGパス（1600×900・2倍は3200×1800）]
- **ショート動画**: [mp4パス（9:16・尺）／Reels用・IGアプリで音楽追加を推奨]

---

## Notion保存
**5-A) コンテンツページ**: [notion-saverから返されたURL]
**5-B) 一般質問ネタDB**: [notion-saverから返されたURL]

[human_review_needed=true の場合のみ]
⚠️ **人間レビュー必要**: 2周の自動リトライでも品質基準を満たせませんでした。以下の課題を確認してください:
- [content-editor の revision_requests を箇条書き]
```
