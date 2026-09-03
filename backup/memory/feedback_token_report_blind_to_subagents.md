---
name: feedback-token-report-blind-to-subagents
description: トークン実測がサブエージェントを数えておらず、消費の68%が見えていなかった
metadata:
  type: feedback
---

サブエージェントの転記は `<projects>/<session_id>/subagents/*.jsonl` に別置きされる。
`token_report.py` は `*.jsonl` しか見ておらず、**消費の68%を数えていなかった**。
実測差：9/2＝289M→**835M**、9/3＝79M→**543M**、f1035c7e＝44M→**224M**（うちサブ176M）、
e02e916f＝100M→**226M**。「真因＝長時間セッション」「軽い呼び出しの回数」という過去の
結論はこの穴の上に立っていた。真の主因は **Agent の fan-out**。
**Why:** 本体の文脈が小さいままサブ側で燃えるため、文脈サイズを見張る⛔は原理的に鳴らない
（05e764db は本体111Kのまま232M）。
**How to apply:** 修正済み（token_report.py に親合算＋サブ比率表示／.bak-20260903）。
`context_budget_notice.py` は Agent・Task・Workflow の完了時にサブ累計を数え、30Mごとに🧨。
重いタスクは「本数を絞る・範囲を狭める」が最優先で、区切りやBash束ねはその次。
[[feedback-ctx-notice-oneshot-silence]] [[project-token-reduction-2026-08-20]]
