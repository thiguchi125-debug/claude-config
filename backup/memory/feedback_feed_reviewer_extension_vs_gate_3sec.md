---
name: feedback-feed-reviewer-extension-vs-gate-3sec
description: ショート動画で配信面ゲートの「表示が短すぎる」指摘に尺延長で応えると gate.py の3秒ルールに触れる。延長分は無ナレのホールドカットに分ける
metadata:
  type: feedback
---

`feed-visual-reviewer` が「テロップの秒数×文字数が超過」と指摘したとき、素直に1カットの表示時間を延ばすと **`gate.py` の「3.0秒超のカット」違反**になる（2026-09-07 JR境界ICまたぎで発生。a4を+1.2秒延長してカット20が3.5秒）。

**Why**: 2つの検査器が別の基準を持っている。feed-visual-reviewer は「読ませる字数に対して時間が足りるか」、gate.py は「1カットが長いと間延びする」。どちらも正しいので、時間を足すのではなく**カットを割る**のが解。

**How to apply**: 延長分を**ナレなしのホールドカット**として独立させる（同じ挿入画像を保持したまま、小文字帯や出典を読ませる間に使う）。カット数が増えるが gate.py の「カット数は尺÷2.5以上」は満たす方向なので問題ない。テロップの文字を削って解こうとする前に、その文言が安全ゲートで復活させたものでないか確認する（削ると歪曲に戻ることがある）。

関連: [[feedback_compression_drops_safety_clauses]] [[feedback_gate_fail_question_the_element_not_the_zone]]
