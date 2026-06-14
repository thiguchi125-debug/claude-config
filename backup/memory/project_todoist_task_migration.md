---
name: project_todoist_task_migration
description: 日々のタスク管理をNotion✅タスクDBからTodoistへ移行（2026-06-14決定）。token場所・API版・構成・残作業
metadata: 
  node_type: memory
  type: project
  originSessionId: db89e985-42f1-43bf-87c3-952f2cc20543
---

# Todoistへタスク管理移行（2026-06-14決定）

**Why:** Notion✅タスクDB(292cf503)が重い・視認性悪い・ノイズ多い・気軽に開けない、と草川が不満。さらにスマホをAndroid化したためApple リマインダー（Mac側に既存リストあるが）も同期不可で不採用。条件＝Mac＋Android両対応／軽い／Claude自動連携が大前提。→ Todoistに決定（APIトークン1枚で連携・Android純正級アプリ・標準「今日」ビューが軽い）。

**How to apply（運用恒久ルール）:**
- **APIトークン**: `~/.config/todoist/token`（chmod 600）。`TOKEN=$(cat ~/.config/todoist/token)` で読む。
- **APIは必ず `https://api.todoist.com/api/v1/`**。旧 `/rest/v2/`・`/sync/v9/` は廃止（HTTP 410）。認証は `-H "Authorization: Bearer $TOKEN"`。
  - 一覧: GET `/api/v1/projects` `/api/v1/tasks` `/api/v1/labels`（レスポンスは `{"results":[...]}`）
  - 作成: POST `/api/v1/tasks` JSON `{content, description, due_string, priority(1-4・4が最高=P1), project_id}`
  - 移動: POST `/api/v1/tasks/{id}/move` `{project_id}`
  - 削除: DELETE `/api/v1/tasks/{id}`（204）／完了: POST `/api/v1/tasks/{id}/close`
- **構成（2026-06-14構築）**:
  - プロジェクト: Inbox / 🏛 議員活動 / 📋 政策・一般質問 / 📣 発信 / 🏡 家族・プライベート
  - ラベル: @結果待ち（相手のボール）/ @保留（やる方向だが要検討）/ @アイデア（いつか）/ @読む（既存）
  - 状態管理は「進行中/今週中」専用プロジェクトを作らず、**期限＋標準ビュー(今日/次の7日間)＋ラベル**で表現（これが軽さの源）。
  - 🏛議員活動のid=6grRHfFfc2WQF46C（参考。変わり得るので都度API取得が安全）
- **移行済**: eスポーツ講座 全4回進行台本タスク（→🏛議員活動）。
- **残作業（未完了）**:
  1. Notion✅タスクDBの未完了タスクをTodoistへ移行（領域ごとに振り分け）
  2. **ohayo / oyasumi スキルをTodoist参照に書き換え**（朝=今日/期限切れ/今週を表示、夜=完了集計＋未完了繰越）。現状は両スキルともNotion✅タスクDBを叩く実装。
  3. citizen-inquiry→タスク登録、task-to-project昇格判定 等のNotion前提フローの扱いを整理（重いDB用途＝市民意見ログ・PJ記録はNotion残置、日々タスクはTodoist一本化の方針）。
- **方針**: Notionは市民意見ログ・プロジェクト記録など重いDB用途に限定。日々の行動タスクはTodoistに一本化。

関連: [[feedback_ohayo_oyasumi_task_db_query]] [[feedback_task_deadline_3days]] [[feedback_ohayo_task_3block_display]]（これらNotion前提のタスクルールはTodoist移行に合わせ要改訂）
