---
name: ohayo/oyasumi タスクDB実クエリ必須
description: ダッシュボード旧表からの流用禁止。タスクDBは「すべて」viewで毎朝必ず実DBクエリし、Done/Archive除外＋本日inbox包含を必ず行う
type: feedback
originSessionId: 531fda17-c6fd-481e-9528-1dacd49bdec2
---
# ohayo/oyasumi タスクテーブルは実DBクエリ必須

朝のダッシュボードのタスクテーブルや、デイリーサマリの繰越し件数は、**毎朝/毎晩 必ずタスクDBに最新クエリを投げて作る**こと。前日のダッシュボード表からのコピペ流用は禁止。

**Why:** 2026-04-30、ohayo/oyasumi 統合実行時に古いダッシュボードのタスクテーブルをそのまま流用した結果：
- 既に Archive 済みの「酒井さん返信」「北東分署前横断歩道」がダッシュボードに残存
- 既に Done 済みの「【メール確認】Googleフォーム回答2件」が残存
- 一方、本日4/30期限の重要タスク（小下訪問初日／保健師大河内さん／選挙人口PDF／菅内太陽光）と、超過タスク14件（小下版レポート／e スポーツ参加返信／みずきが丘予約／中部中視察 ほか）を**まるごと取りこぼし**
- 草川から「すでにremindから外れている予定も超過に残っている」「今日の期限になっているinboxのタスクも拾ってください」と指摘あり

**How to apply:**

### 必ず使うクエリ
- ✅タスクDB「すべて」view: `https://www.notion.so/292cf503a68f814eafcdec9eed56f273?v=292cf503a68f811e9555000c1fce8ad5`
- `notion-search` は data_source_url 指定でも0件返却（既知の不具合）。**`notion-query-database-view` の view_url 直叩きを必須**。

### ローカルフィルタ手順（必須）
1. `ステータス` ∈ {`Done`, `Archive`} は除外
2. `date:期限:start` ≤ 今日 のものを「未完了」として抽出（超過＋本日）
3. `ステータス` = `inbox` かつ 期限=今日 のものを明示的に拾う（よく取りこぼす）
4. 期限なしinboxはダッシュボードには出さない（積み残しセクションで件数だけ集計）

### 表示ルール
- 期限超過は表示時のみ ⚠️ プレフィクス（DBタイトルへの永続書き込みは禁止・二重マーカー化リスク）
- 本日期限はそのまま、必要に応じて ⭐ で重要度マーク
- 期限列を必ず追加（「本日 4/30」「4/27 (3日超過)」など人間可読）

### 関連スキル更新
- `~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/ohayo/SKILL.md` 3-1b セクション
- `~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/oyasumi/SKILL.md` 1-D + Step 3
- いずれも 2026-04-30 に書き換え済み
