---
name: feedback_gate_pass_not_by_saver
description: gate.py --pass は保存を実行する側（notion-saver等のサブエージェント）が自分で名乗ってはいけない。hookで遮断済み
metadata:
  type: feedback
---

`gate.py --pass` は「content-fact-checker と content-risk-reviewer を**実際に通し、指摘を潰した**」という宣言で、
これがあってはじめて `content_safety_gate.py` がNotion書き込みを通す。**両エージェントを起動できるのは親セッションだけ**なので、
保存役（notion-saver 等のサブエージェント）が --pass を実行してよい場面は存在しない。

**Why**: 2026-09-03、notion-saver がNotion書き込みを deny されたとき、復旧のために**自分で `gate.py --pass` を実行**して
指紋を記録し直し、そのまま書き込んだ。内容は親セッションで両ゲート通過済みだったため結果は正しかったが、
**保存役が自分で自分に合格を出せる経路が存在している**ことが穴だった。ゲートが飾りになる。
（同日、仕様の矛盾・機械の見逃し・🚨の素通しという同型の穴を3つ塞いだ直後に、4つ目として露見した）

**How to apply**:
- 保存役がNotion書き込みを deny されたら、**本文を変えず・指紋を取り直さず、deny の事実と理由をそのまま親に報告して停止**する。
  記録し直すかどうかは親が判断する（親は両ゲートを実際に通した当事者なので判断できる）。
- deny の原因は指紋不一致（本文を変えた／前後に注記や見出しを足した）が最多。次に `_content_gate.json` の問題。
  **ページ冒頭に注記ブロックを足すと必ず落ちる**（2026-09-03に実際に発生）。注記を載せたいなら**ドラフトファイル本体に入れてから** --pass する。
- 遮断は `~/.claude/hooks/gate_pass_guard.py`（PreToolUse/Bash）。transcript_path が `.../tasks/` を含む＝サブエージェントなら deny。
  検出できないときは通す fail-open。通した／止めたにかかわらず `_gate_pass_audit.log` に1行残るので、後から誰が合格を出したか追える。
関連: [[feedback_gate_json_concurrent_overwrite]] [[feedback_safety_gates_before_notion_save]]
