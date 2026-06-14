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
- **ヘルパー（2026-06-14作成・動作確認済）**: `python3 ~/.claude/scripts/todoist/td.py <cmd>`。cmd＝`morning`(3ブロック+監査)／`add "内容" [--due ...][--project ...][--priority 1-4][--label ...][--desc ...]`／`today`/`overdue`/`week`/`nodue`/`audit`/`list [PROJECT]`/`done <id>`/`rm <id>`/`projects`。ページネーション・プロジェクト名部分一致解決・ラベル付与すべて対応。
- **完了済（2026-06-14）**:
  - ✅ Todoist連携構築（token保存・read/write/move/delete 全確認）
  - ✅ 構成構築（5プロジェクト＋3ラベル、サンプル14件＋既定2プロジェクト削除）
  - ✅ eスポーツ講座タスク移行（→🏛議員活動）
  - ✅ **②ohayo/oyasumi をTodoist参照に書換**＝両SKILL.md 冒頭に「🔴タスクはTodoist参照」override追記（ohayo朝タスク＝`td.py morning`／oyasumi繰越・監査＝`td.py overdue`+`audit`）。プラグインキャッシュ編集は今回ブロックされず成功。
  - ✅ **CLAUDE.md恒久ルール化**＝「タスク・プロジェクトはTodoistに一本化（最上位）」追加＋市民相談/プロジェクト化判定の登録先をTodoistへ変更。
- **残作業（任意・未着手）**:
  1. Notion✅タスクDBの**既存未完了タスク**をTodoistへ移行（草川未依頼。必要になれば `td.py add` で領域別に投入）。それまでNotion旧タスクは参照のみ。
  2. nichijo / iken(citizen-inquiry) / task-audit スキル本体のNotionタスク記述も、必要時にTodoist override追記（現状はCLAUDE.md最上位ルールでカバー）。
- **方針**: Notionは市民意見ログ・プロジェクト記録など重いDB用途に限定。日々の行動タスクはTodoistに一本化。プラグイン更新でSKILL.md override が消えてもCLAUDE.md側で挙動確定。

関連: [[feedback_ohayo_oyasumi_task_db_query]] [[feedback_task_deadline_3days]] [[feedback_ohayo_task_3block_display]]（これらNotion前提のタスクルールはTodoist移行に合わせ要改訂）
