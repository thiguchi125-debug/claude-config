---
name: project_oyasumi_headless_mcp_missing
description: 夜間oyasumi(claude -p)でNotion/Drive/Calendar MCPが読めずサマリ未作成が続いている（10/29分・10/30分）
metadata:
  type: project
---
2026-10-29分・10-30分の夜間oyasumiで、ToolSearchしても mcp__claude_ai_Notion/Drive/Calendar が出てこない。10/29 0:04の実行では使えていた。Todoist(td.py)だけは動く。控えは drafts/oyasumi_<日付>_mcp_fallback.md、status は error。
起動も23:30予定が翌日昼〜朝にずれている（Macスリープ）。

**Why:** デイリーサマリ・金曜週次レポート・朝ダッシュボードが止まり、草川の目に何も残らない。
**How to apply:** 対話セッションで /mcp でコネクタ接続・ログインを確認。直るまで夜間ジョブは控えファイル＋error記録で終える。関連 [[project_stalled_automation_revival_2026-08-20]]
