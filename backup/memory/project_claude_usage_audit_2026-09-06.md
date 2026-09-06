---
name: project-claude-usage-audit-2026-09-06
description: 2026-09-06 Claude Code活用棚卸し。実測（14日5.1G・改修3日で41%・ohayo4回）→ 1行通知・週1改修枠・休眠スキル凍結・skill_router を導入。残＝news_briefing.shの通知行（分類器deny）
metadata: 
  node_type: memory
  type: project
  originSessionId: f1d30a5a-6234-41b6-83cf-d8368330529f
  modified: 2026-09-06T10:54:46.013Z
---

## 実測（8/23〜9/6）
199セッション（自動約90・手動約110）／5.1G／サブ44%／起動固定費中央値78.6K／kugiri 38回／ohayo 4回。
改修3日（9/2〜9/4）で2.1G＝41%。夕便は週5日稼働（9/1スリープ見送り・9/2 API失敗）。

## 診断
①提案の出口が無い（ohayo開かれず・Discord納品は8/26廃止）②改修が本業を食う③自動ジョブがMac電源に依存④草川手番待ちで止まる自動化⑤休眠スキルが固定費⑥担当スキル/agentが自然な言い回しで起動されない（本体が直接答える）。

## 2026-09-06 に入れたもの
- `discord_api.py notify`（200字・#納品・INBOX_ONLYの唯一の例外）＋ `sns_leg.sh` 夕便完了の1行通知。`news_briefing.sh` 側も2026-09-07 00:30に適用済み（初回は9/7 6:05便）
- `content_safety_gate.py` EXEMPT_PAGES に📰ダイジェスト／dedupの2ページ（草川承認）
- CLAUDE.md トークン節約節に週1改修枠（[[feedback_maintenance_weekly_window]]）
- 休眠スキル4本を `~/.claude/skills_dormant/` へ（[[project_dormant_skills]]）
- `hooks/skill_router.py`（UserPromptSubmit・言い回し→担当の案内のみ・強制なし）。settings.json に登録
- 9/4夕便のNotion未保存1件を📣DBへ保存・`_notion_queue.jsonl` 消込済み（done側へ移動）

## 残（次の日曜改修枠）
エージェント48本の同じ棚卸し／ohayoに「昨夜の夕便を投稿した？」1問／10/18告示のゲート自動厳格化／9月議会答弁のtoben-tracker予約。関連: [[project_sns_routine_v2]] [[project_hasshin_flow_phase1_2026-09-04]]

## 2026-09-07 起動固定費削減（案3・案4を「今直して」で実施）
- 案3: MEMORY.md から完了・修理済み9行を `_backup_2026-09-07/MEMORY_retired_lines_2026-09-07.md` へ退避（26,008→24,662バイト）。個別ファイルは残置
- 案4: 入れ子 `.claude` 6か所（全て空・consolidate済み）を `~/Archive/_trash_pending_2026-09-07/nested_claude/` へ。偽エージェント4本の元.mdはディスクに無く、起動スナップショットの残骸＝次セッションで消える
- 発見: `consolidate_agent_memory.py` の夜間常設化が launchd/scripts/settings のどこにも登録されていない（memoryの記述と食い違い）→ 日曜枠で確認
- 案1・2・5・6 は Todoist #6hRFvqvcFPQwP9Rg（@日曜改修）に積んだ
