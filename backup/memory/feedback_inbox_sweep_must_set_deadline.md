---
name: feedback-inbox-sweep-must-set-deadline
description: Inbox棚卸しで「箱へ」移すときは必ず期限も付ける。td.py mv だけでは見えなくなるだけ
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a68bc720-07c3-4354-a565-bc86eaf1aee5
  modified: 2026-09-11T00:52:25.928Z
---

ohayo §5 の Inbox棚卸しで「箱へ」を選んだ項目は、`td.py mv` で終わらせず**必ず同じパスの中で期限まで確定させる**。移動だけだと期限なしタスクの山に積み増すだけで、3ブロック表示（期限超過／本日／今週中）に構造的に出てこなくなる。台帳へ移す場合も `yobo.py update --due` まで通す。

**Why:** 2026-09-11の棚卸しで、7件中3件を `td.py mv` だけで箱へ移そうとしたところ草川から「振り分けてるけど期限は設定してるの？見えなくなるだけじゃない？」と指摘。同じ朝の監査で期限なしが16→25件（+9）に増えており、実際に「振り分け＝不可視化」が起きていた。草川の指示は「こんごのインボックス整理の際は必ず期限もつけること」。

**How to apply:**
1. 4択の「箱へ」を選んでもらった直後に、その場で task-add の突合（想定所要→カレンダー突合→✅/⚠️/🚫）を回す
2. 期限案を ✅/⚠️/🚫 付きで提示し承認を取る（`td.py mv` は期限を触らないので別操作が要る）
3. 既存タスクへの期限付けは `~/.claude/skills/task-add/_verified.json` に content と due を書いてから Todoist MCP `update-tasks` の `dueString` で設定する（`td.py` に update は無い／`_verified.json` が無いと `todoist_calendar_guard.py` が deny）
4. 「期限なしでいい」も選択肢として出してよいが、期限なしタスクの現在件数を添えて選ばせる

関連: [[feedback_ohayo_deadline_null_blindspot]] / [[feedback_ask_destination_and_deadline_before_register]] / [[project_task_add_calendar_gate]]
