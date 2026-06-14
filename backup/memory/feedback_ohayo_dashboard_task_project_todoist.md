---
name: feedback_ohayo_dashboard_task_project_todoist
description: ohayoの朝ダッシュボード「今日のタスク」「進行中プロジェクト」もTodoist由来にする（Notionタスク/プロジェクトDBに紐づけない）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 685e154a-41e9-4875-a2ac-b7bb82177210
---

ohayo の朝ダッシュボード（page 722beb9e）の **`## ✅ 今日のタスク`** と **`## 🔗 進行中プロジェクト`** セクションは、Todoist 由来の内容で書く。Notion ✅タスクDB(292cf503) / 🗂️プロジェクトDB に**紐づけない・mention-page リンクも張らない**。

**Why:** タスク・プロジェクトは Todoist 一本化済み（[[project_todoist_task_migration]]・CLAUDE.md 最上位ルール）。それなのにダッシュボードのこの2セクションだけ旧Notion DBに紐づいたまま残っており、しかも前日のNotionタスク表（古い6/14データ）が表示され続けていた。草川が「今後そのDBには接続しないよう求めたはず。Todoistから抽出するように」と再指摘（2026-06-15）。SKILL.md冒頭の🔴Todoist override は「チャットの3ブロック＋監査」しかカバーしておらず、§4のダッシュボード書込み（§4セクション3 進行中プロジェクト／✅今日のタスク）は依然Notion DBクエリを指示していたのが穴。

**How to apply:**
- ohayo §3-1b/§3-5/§4 で Notion タスクDB view・プロジェクトDB view を**叩かない**。タスクは `td.py morning` の出力、プロジェクトは `td.py projects`（主要グループ＝🏛議員活動／🎪地域・イベント／🎮eスポーツ／🗳選挙2026 等）から書く。
- ダッシュボードの両セクション末尾は「→ タスク/プロジェクトはTodoistで管理（td.py / Todoistアプリ）。Notion ✅タスクDB/🗂️プロジェクトDBは新規登録に使わない」で締める。
- mention-page で Notion タスクDB/プロジェクトDB へリンクし直さない。
- 情報ハブ一覧の「📁 プロジェクト・タスク」内Notionリンク3本は**参照専用ブックマーク**として残置可（草川手動管理・読むだけ）。蓄積母艦は [[project_notion_project_platform]]（🗂Notionプロジェクト・プラットフォーム）。
