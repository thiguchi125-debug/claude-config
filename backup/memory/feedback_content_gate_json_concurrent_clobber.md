---
name: feedback-content-gate-json-concurrent-clobber
description: 安全ゲート記録 _content_gate.json は1ファイル上書き方式のため、夜間パックジョブと朝夕SNS便が重なると互いの通過記録を消し合う
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e5516304-87a8-4008-81ed-2d85a0dc5659
  modified: 2026-08-06T22:22:00.739Z
---

`~/.claude/scripts/gate.py --pass` は `~/.claude/hooks/_content_gate.json` を**追記ではなく上書き**で書く。並行して走るジョブがそれぞれ gate.py を実行すると、後から実行したほうの記録だけが残り、先に通したジョブのNotion書き込みが `content_safety_gate.py` に deny される。

**Why:** 2026-08-07、夜間パックジョブ（nightly_intake.sh 第2ステージ・3:24起動が7時台まで遅延）と朝便（sns_leg.sh morning_push・6:45起動）が重なって発生。パック側が gate.py を通した数秒後に朝便が自分の原稿で gate.py を実行し、パック側の指紋が消えて書き込みが deny された。朝便側も07:12と07:16に2回記録し直しており、同じ衝突を繰り返していた形跡がある。fact/riskは正しく通っているのに書き込みだけが落ちるので、「ゲート未通過」という表示に引きずられて原稿を疑うと原因を見失う。

**How to apply:**
- deny されたら、まず `python3 -c "import json,os;print(json.load(open(os.path.expanduser('~/.claude/hooks/_content_gate.json')))['approved'][0]['file'])"` で**記録されているファイル名が自分のものか**を見る。別ジョブのファイル名なら原稿の問題ではなく衝突。
- 相手ジョブが実行中（`ps aux | grep sns_leg` ／ `_sns_legs.log` に `end` 行がない）なら、こちらが gate.py を再実行すると相手を壊す。相手の `end` を待ってから再記録→**即座に**Notion書き込みする（TTLは120分あるが、衝突窓は数秒単位）。
- `--pass` は「fact-checker と risk-reviewer をこのセッションで実際に通した」という宣言。衝突による再実行で原稿本文が変わっていなければ再宣言してよいが、本文を1文字でも直したら両エージェントを通し直す。
- 恒久対策の候補（未実施・草川判断）: gate.py を追記＋ファイル名キー方式にする、または gate.py 実行〜Notion書き込みを `_leg.lock.d` と同種のロックで囲う。
