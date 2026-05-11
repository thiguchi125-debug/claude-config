---
name: ohayoのタスク監査シグナル（v2.3）
description: ohayoに「🧹 タスク監査シグナル」セクションを組み込み、5指標の件数表示と閾値超え時のtask-auditスキル誘導を行う。本格処理はtask-auditで実行。
type: feedback
originSessionId: 9c9062cc-6632-43ec-90c3-a45338c48e0c
---
# ohayoのタスク監査シグナル（v2.3）

**Why**：2026-05-11、これまで手動でやってきた「期限なし棚卸し→PJ化判定→停滞PJ再起動」の流れを定期的に回す仕組みが必要。ただ ohayo は燃費圧迫が常時課題のため、ohayoに「シグナル件数表示」だけ載せ、本格処理は別スキル `task-audit` で手動起動する設計に。

**How to apply**：
- ohayo §3「📋 積み残し確認」の直後に「🧹 タスク監査シグナル」セクションを追加
- 5指標：期限なしinbox／停滞inbox／長期Waiting／停滞PJ／PJ化候補
- 閾値（⚠️点灯条件）：
  - 期限なしinbox > 5件
  - 4日以上停滞inbox > 10件
  - 60日超Waiting > 3件
  - 停滞PJ > 3件
  - PJ化候補 > 2件
- 誘導文は**条件分岐で表示制御**：
  - ⚠️ゼロ → 誘導文なし（毎朝の冗長表示を回避）
  - ⚠️1個以上 → 「👉 ⚠️ N件あります。『タスク棚卸し』で詳細棚卸しを起動」
  - ⚠️3個以上 → 「🚨 ⚠️ N件あります（要対応）。『タスク棚卸し』で即起動推奨」
- task-audit本体は `~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/task-audit/SKILL.md`
- task-auditのモード：quick（40-60K）/ standard（80-120K）/ full（150-250K）
- cron化禁止（草川の認知制御を保つため手動起動のみ）

**関連メモ**：
- `feedback_ohayo_task_3block_display.md`（3ブロック表示）
- `feedback_ohayo_deadline_null_blindspot.md`（期限なし放置の穴）
- `feedback_task_deadline_3days.md`（期限デフォルト今日+3日）
