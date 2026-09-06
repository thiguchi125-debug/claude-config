---
name: form-intake
description: "Googleフォーム「ご意見箱」3シートの新着を📝市民意見リストへ自動取込＋_citizen_voice/へマスク追記（毎晩3:30 launchdでも同手順）。返信案は作らない。Triggers: フォーム取り込んで/ご意見箱取り込んで/フォーム新着確認。NOT: コピペ受付→iken"
---

# ご意見箱フォーム取込スキル（form-intake）

Googleフォーム「ご意見箱」の回答シート3枚から新着市民意見を差分取込し、Notion登録＋ドメイン分類蓄積まで自動で行う。
2026-07-25にohayo §9（朝ポーリング）を夜間launchdへ前倒しして独立させたもの。**stateは旧§9と同じ
`iken_poller_state.json` を共用**するため、朝夜どちらで走っても二重登録しない。
**返信案・タスク化は本スキルの守備範囲外**（登録まで。続きはikenスキル後半 = 返信3案→Gmail下書き→Todoist提案）。

## 関連ファイル

- **状態（正本）**: `~/.claude/projects/-Users-kusakawatakuya/iken_poller_state.json`
  - シート3枚のfileId・column_map・`last_processed_timestamp`（Notion登録済み時点）・`etl_last_row`（ETL追記済み行数）・spam/testフィルタ設定
- 結果: `~/.claude/scripts/form-intake/_form_status.json` — ohayo表示用
- 死活: `python3 ~/.claude/scripts/sns-routine/update_status.py form_intake <ok|error> "<msg>"`
- ETL資産: `~/.claude/agents/knowledge/kusagawa_archive/03_themes/_citizen_voice/`（6ドメイン＋_other＋_index.md）
- Notion: 📝市民意見リスト data_source_id `c2c34bd8-1e16-492e-aab0-d3f497d18d4d`

## 手順

### Step 0: MCPツールロード（headlessでは必須）

ToolSearchで `mcp__claude_ai_Google_Drive__download_file_content, mcp__claude_ai_Notion__notion-create-pages, mcp__claude_ai_Notion__search` をロードする。
**headless実行ではMCPがdeferredで起動する。ToolSearchでスキーマをロードする前に「MCP未接続」と判定してはならない**（2026-07-17 SNS便不発事故の再発防止）。

### Step 1: 新着検出

1. `iken_poller_state.json` をRead。
2. 各シートを **`mcp__claude_ai_Google_Drive__download_file_content` で取得しbase64デコード**して読む。
   **⚠️ `read_file_content` は古いキャッシュを返すため使用禁止**（state内noteに記録済みの実事故）。
   大きいシートはデコード結果をファイルに保存し、Bashの `wc -l`/`tail` で末尾の新着行だけ読む（全文をコンテキストに載せない）。
3. 各シートで2種類の差分を取る：
   - **Notion新着** = `タイムスタンプ > last_processed_timestamp` の行
   - **ETL新着** = データ行番号（ヘッダ除く） > `etl_last_row` の行（行IDは `S<n>-<行番号>`・既存ETL資産と同じ採番）
4. **テスト投稿フィルタ**（state設定のとおり）: 名前にtest_keywords／連絡先がkusagawa_test_emails／本文がmin_opinion_length未満／spam_keywords含む → その行はNotion・ETLともスキップし、stateだけ進める（_form_status.jsonに「⊘ テスト投稿スキップ」1行）。
5. 両方とも新着0件 → `_form_status.json` に `{"date": 今日, "new_count": 0}` をWrite → `update_status.py form_intake ok "新着0件"` → **終了（Notion・ETLファイルは触らない）**。

### Step 2: 解析（ikenスキルStep1準拠）

新着1件ごとに column_map で列を読み、抽出：氏名（なければ「匿名」）／連絡先（メール・LINE ID・電話）／年代／本文／
分類タグ（道路/防災/福祉/子育て/教育/環境/公共交通/行政手続/その他から複数）／
地区（④お住まいの地域列＋本文中の地名から推定）／
緊急度（高=被害発生中・危険・時間制約／中=困りごと・要望／低=気づき・感想・提案）。
経路は全件「フォーム」→ 📝市民意見リストの経路selectでは **「その他」** にマッピング。

### Step 3: 重複ガード（Notion新着のみ）

`mcp__claude_ai_Notion__search`（data_source `c2c34bd8-` 内）で本文冒頭の特徴語を検索し、
同一内容の既登録（日中に草川が手動ikenでコピペ済み等）があればその行のNotion登録をスキップ
（ETL追記は行い、_form_status.jsonに「既登録スキップ」と記す）。

### Step 4: 📝市民意見リストへ登録（Notion新着のみ）

ikenスキルStep 3のプロパティ仕様に完全準拠（`~/.claude/skills/iken/SKILL.md` 参照）：
件名=意見冒頭60字＋（氏名様 or 匿名）／受付日=フォームのタイムスタンプ／相談者・連絡先／経路=その他／
地区／分類タグ／緊急度／意見内容=原文（1900字上限）／次アクション=「返信要否確認」／匿名checkbox。
意見内容の末尾に `（ご意見箱フォーム自動取込 S<n>-<行>）` を付記。

### Step 5: ドメイン分類ファイルへ追記（ETL新着のみ・個人情報マスク必須）

1. 6ドメイン（childcare_education / transport_infrastructure / dx_administrative / disaster_safety / healthcare_welfare / urbanplanning_industry / _other）に分類（分類スキームは `_citizen_voice/_index.md` 参照）。
2. 該当 `<domain>.md` の「個別意見一覧」末尾に既存形式で追記：
   `**N.** (YYYY/MM/DD、年代、地区 / S<n>-<行>) 本文冒頭100字程度…`
   **マスク必須**：メールアドレス・電話番号・LINE IDは削除、フルネームは氏のみ or「匿名」。
3. 冒頭の該当件数と「主要要望（頻出順サマリ）」の該当項目件数を更新。
4. `_index.md` のドメイン別件数表・合計・取込日を更新。

### Step 6: 結果記録

1. `_form_status.json` をWrite：
```json
{"date": "YYYY-MM-DD", "new_count": N, "items": [
  {"row_id": "S2-196", "date": "2026/07/20", "district": "井田川", "domain": "childcare_education",
   "urgency": "中", "summary": "1行要約", "notion_url": "...", "skipped": false, "urgent": false}
], "errors": []}
```
2. state更新：`last_processed_timestamp` は **Notion登録（またはスキップ判定）が成功した行のタイムスタンプまで**、`etl_last_row` は **ETL追記が完了した行まで** 進める。途中失敗した行以降は進めない（翌夜再処理）。noteに処理サマリ1行を追記。
3. `update_status.py form_intake ok "新着N件登録（スキップM件）"` を実行。

### Step 7: 対話実行時のみ — 結果報告

手動起動（「フォーム取り込んで」）の場合は、新着一覧（行ID・要約・緊急度・NotionURL）を表示し、
「返信案が必要な意見があれば番号で指定してください（→ ikenの返信3案フローへ）」と締める。
headless実行時はこのステップ不要（翌朝ohayoが表示する）。

## エラーハンドリング

- Drive/Notion MCP不通（ToolSearch後も本当に無い場合）→ `update_status.py form_intake error "MCP不通"` で終了。stateは進めない。
- Notion登録が一部失敗 → 成功分だけstateを進め、`_form_status.json` の errors に残す。
- 緊急度「高」の意見は `"urgent": true` を付け、ohayoが目立たせられるようにする。

## 📌 恒久ガードルール

- **`read_file_content` 使用禁止・必ず `download_file_content`＋base64デコード**（古いキャッシュで新着を見落とす実事故あり）。
- 返信案・タスク登録・自治会紐付け（iken Step3.5）は夜間に自動でやらない（草川承認ルールとの整合）。
- ETL追記時の個人情報マスクはNotion登録と独立に必ず実施（_citizen_voice/はgrep対象の学習層のため）。
- 「新着0件」の夜はNotion・ETLファイルに一切書き込まない。
- stateの `last_processed_timestamp` と `etl_last_row` は用途が違う（前者=Notion登録済み・後者=ETL追記済み）。混同して片方で上書きしない。
