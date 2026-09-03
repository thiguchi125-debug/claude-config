---
name: feedback-ctx-notice-oneshot-silence
description: 区切り警告が閾値ごとの一発通知だったため、1回配達に失敗すると以後永久に沈黙した
metadata:
  type: feedback
---

2026-09-03 セッション f1035c7e は文脈332Kまで伸びたのに 🔴200K も ⛔300K も一度も出ず、
状態ファイルだけが `level=300000` に進んでいた（生成はされたが草川に届かなかった）。
**Why:** 一発通知は「配達失敗＝永久沈黙」と同義。次に鳴るのは400Kで、そこへ届く前に
セッションが終われば無警告のまま。※握り潰した機序自体は未特定（サブエージェントは独自の
転記ファイルを持つので、当初疑った経路ではない）。
**How to apply:** 修正済み（.bak-20260903）。①200K台は40回ごと・300K超は15回ごとに鳴り直す
②transcript名とsession_idが不一致な呼び出し（サブエージェント）では計測も状態更新もしない。
「警告が出なかった」と言われたら `~/.claude/hooks/state/<sid>.ctx` の level と
転記内の 🔴/⛔ の有無を突き合わせる。[[feedback-token-report-blind-to-subagents]]
