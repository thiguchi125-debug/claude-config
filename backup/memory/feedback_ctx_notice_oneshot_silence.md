---
name: feedback-ctx-notice-oneshot-silence
description: 区切り警告が出ないまま大量消費した真因＝閾値ごとの一発通知。1回でも配達に失敗すると以後永久に沈黙する
metadata:
  type: feedback
---

`context_budget_notice.py` は閾値を跨いだ瞬間に1回だけ鳴らし、状態ファイルに到達レベルを書いていた。
2026-09-03 セッション f1035c7e は文脈332K・219回・44.3M まで伸びたのに 🔴200K も ⛔300K も一度も出ず、
状態ファイルだけが `level=300000` に進んでいた（＝生成はされたが草川に届かなかった）。
**Why:** 一発通知は「配達失敗＝永久沈黙」と同義。しかも session_id を共有するサブエージェント側の
呼び出しで鳴ると、通知は見えない場所へ行き状態だけが進んで本体を黙らせる。
**How to apply:** 修正済み（.bak-20260903 あり）。①transcript のファイル名が session_id と一致しない
呼び出し（＝サブエージェント）では計測も状態更新もしない ②200K台は40回ごと・300K超は15回ごとに鳴り直す。
「警告が出なかった」と言われたら、まず `~/.claude/hooks/state/<sid>.ctx` の level と
transcript 内の 🔴/⛔ の有無を突き合わせる。[[project-kugiri-session-split]] [[project-token-reduction-2026-08-20]]
