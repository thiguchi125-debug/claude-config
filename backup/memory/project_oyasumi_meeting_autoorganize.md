---
name: oyasumi にAIミーティング自動振り分けStep追加
description: 2026-05-03、Notion AI Meetingで記録された会議をoyasumi Step 4.5で自動的に📅ミーティングノートDBへ転記する仕組みを追加
type: project
originSessionId: 3d6ddbd4-d2bf-409b-bad9-0583dd457c4c
---
2026-05-03 実装。Notion AI Meeting で録音した会議が📅ミーティングノートDBに転記されないまま孤立する問題を解消するため、oyasumiスキルに自動振り分けStepを追加。

## 背景
- 会議関連は3DB構造（重複ではない・親子関係）：
  - 🤖 AIミーティングノートDB（system collection・読取専用・Notion AI自動生成）
  - 📅 ミーティングノートDB（ds:26d7848d-）：構造化された会議記録、編集可・relation付き
  - 🏛 会議体マスタDB（ds:46414643-）：定例的会議体の登録簿、開催回数 rollup
- フロー: AI録音 → AIノートDB（自動）→ 📅DB（手動 or nichijo整理モード）→ 🏛DB（relation）
- 問題：「整理」「仕上げ」と打たないと nichijo整理モード R1-R5 が走らず、AIノートが孤立蓄積
- 草川希望：「おやすみ」打った夜に自動的に整理してほしい

## 実装した Step 4.5

oyasumi SKILL.md に Step 4.5「AIミーティングノート自動振り分け」を Step 4 と Step 5 の間に挿入。

### 設計方針（D + B 案、草川承認）
- **D**: nichijo整理モード R1-B / R2 / R4-A の subset を内部呼出し（重複定義避け）
- **B**: 会議体マスタとのマッチは確度0.8以上のみ自動紐付け、それ以下は relation 空で保存して翌朝レビュー対象に

### 内訳
- 4.5-1: 当日AIミーティングノート取得（`notion-query-meeting-notes` で `created_time = today`）
- 4.5-2: 既振り分け済みフィルタリング（📅DBの当日レコードの `AI元ノートURL` と照合）
- 4.5-3: 各AIノートの会議種別・重要度・フォローアップ要否を自動推定（キーワード判定）
- 4.5-4: 会議体マスタとマッチング（完全/包含=確度1.0、部分8割=0.8、曖昧=0.5以下→未紐付け）
- 4.5-5: 📅DBへ転記（`作成元 = nichijoスキル` 流用）。本文構造化はスキップ
- 4.5-6: サマリ集計（aim_total / aim_processed / aim_already_linked / aim_unmatched_kaigitai）
- 4.5-7: エラー処理（個別失敗は継続、全体失敗はスキップ）

## Step 6 デイリーサマリへの追加
「🤝 本日の会議自動整理（AIミーティング → 📅DB）」セクション追加。総数・処理件数・未紐付け件数・転記会議リストを表示。会議体未紐付けが1件以上なら朝レビューを促す追記。

## ohayo スキルへの連動追加
朝のダッシュボードに「🤝 昨夜の会議自動整理レビュー（会議体未紐付け N件）」セクション追加。📅DB から「開催日=昨日 ＋ 会議体=空 ＋ 作成元=nichijoスキル」で抽出して、紐付け候補と共に表示。0件ならセクション省略。

## 既存 nichijo整理モードとの関係
- nichijo整理モード（R1-R5）は明示トリガー時（「整理」「仕上げ」）に全DB横断振り分けを実行（重い処理）
- oyasumi Step 4.5 は AIミーティング限定の軽量処理のみ自動実行（毎晩自動）
- nichijo R1-R5 が走った日は、oyasumi Step 4.5 は「既紐付けスキップ」で空振りする（重複しない）

## 影響範囲
- /Users/kusakawatakuya/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/oyasumi/SKILL.md（Step 4.5追加・Step 6セクション追加）
- /Users/kusakawatakuya/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/ohayo/SKILL.md（朝レビューセクション追加）

## 関連メモ
- project_meeting_notes_organization_db.md（3DB構造の元設計）
- project_meeting_hub_renewal.md（会議ハブ刷新）
- project_nichijo_organize_mode.md（整理モードR1-R5の元実装）
- project_oyasumi_system.md（oyasumi本体）
