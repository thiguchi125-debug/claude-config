---
name: project-task-add-calendar-gate
description: task-addスキル＋PreToolUse hookによるTodoist登録のカレンダー突合ゲート（2026-08-03構築）。判定は30分コマ換算・終日予定は原則ブロックしない
metadata: 
  node_type: memory
  type: project
  originSessionId: aec522ed-d6b7-4b01-b322-5a398531ce3c
  modified: 2026-08-04T14:38:03.144Z
---

2026-08-03 構築・稼働中。期限付きTodoist登録の前にGoogleカレンダーと突合し、実施可能性を判定してから登録する仕組み。

**構成**
- `~/.claude/skills/task-add/SKILL.md` — 手順（所要見積→カレンダー取得→判定→提案→承認→`_verified.json`書込→`td.py add`）
- `~/.claude/skills/task-add/sessions.py` — 空き枠算出と3値判定の実装。**手計算禁止・必ずこれを使う**
- `~/.claude/hooks/todoist_calendar_guard.py` — PreToolUse hook。突合なしの `td.py add --due` / MCP `add-tasks` を deny
- テスト: hook 40件・sessions 12件（`python3 -m unittest discover`）

**判定モデル**
- 1コマ=30分、1セッション=1時間=2コマ、**1日に同一タスクへ割けるのは最大4コマ**
- 稼働帯 全曜日9:00-21:00、30分未満の隙間は捨てる
- 判定 ✅=確保≧必要×1.5 ／ ⚠️=必要以上×1.5未満 ／ 🚫=必要未満 or 残り日数<最低所要日数（`ceil(必要コマ÷4)`）

**実データで判明した2つの罠（設計段階では見落としていた）**
1. **終日予定を一律に作業不可日にしてはいけない。** 草川のカレンダーは終日予定の大半が目印（グラウンドゴルフ・憩いの場・地域行事）で、実際の拘束は時間指定予定に入っている。一律ブロックするとほぼ全日が0コマになる。「議会/視察/出張/研修/入院/旅行/終日」を含むものだけ不可日にする。`【参考】`で始まる予定は完全に無視
2. **粒度は1時間ではなく30分。** 1時間単位で切り捨てると「30分だけ空いている日」が0コマになり、電話1本が実施不可と判定される

**運用上の注意**
- `list_events` は2週間分でも7万字超でコンテキストに載らない。自動保存されたファイルのパスをそのまま `sessions.py` に渡す（読み下さない）
- **ゲート対象は add だけではない**（2026-08-04 実装確認・旧記述「reschedule/update は対象外」は誤り）。settings.json の matcher = `Bash | add-tasks | update-tasks | reschedule-tasks`
  - `td.py add --due` / MCP `add-tasks` → 期限があれば常にゲート
  - MCP `update-tasks` → **件名と期限の両方を渡した時だけ**ゲート。件名を渡さず期限だけ更新する呼び出しは照合不能なので素通し（`need_content=True`・意図的）
  - MCP `reschedule-tasks` → **明後日以降への移動だけ**ゲート。今日・明日への移動＝朝の繰越・即日対応は素通し（`CARRYOVER_GRACE_DAYS=1`）
  - 期限を外す指定（remove/none/null/空）は方向が逆なので素通し
- 突合記録の照合方式: add/update は「件名＋期限日」の一致、**reschedule は件名を持たないので期限日の一致のみ**。TTL 30分
- **残る穴＝「期限なしで登録 → `update-tasks` に id と期限だけ渡す」**（件名を省くと素通しする）。旧記述の穴は塞がっておらず、位置が変わっただけ。v1では許容
- `td.py add --due` を叩く既存7スキル（gyakusan/ohayo/nichijo/iken/smart-intake/task-audit/shisei-houkokukai）には task-add 経由の但し書きを入れ済み
- hooks/ は当初 sync-to-git.sh のバックアップ対象外だった→6.5.1節を追加して同期済み。`_verified.json` は除外

関連: [[feedback_ask_destination_and_deadline_before_register]] [[project_todoist_task_migration]] [[project_gyakusan_skill]]
