---
name: project-news-briefing-digest-gate-deny
description: news-briefingのダイジェスト更新・dedup追記・続報追記が安全ゲートで繰り返しdenyされる。原因はEXEMPT_PAGESの登録漏れで、草川の承認待ち
metadata: 
  node_type: memory
  type: project
  originSessionId: 52ac186a-41c5-49d4-a494-2e4f2490a0f1
  modified: 2026-08-21T21:18:28.886Z
---

news-briefing v4-local は📰ニュースDBへの新規登録（プロパティのみ）は通るが、
**ダイジェスト・dedupインデックス・続報の3つは本文書込のため `content_safety_gate.py` が deny する**。
`_news_briefing.log` で2026-08-11 / 08-14 / 08-18 / 08-22 と繰り返し発生（4回以上）。

**真因（2026-08-22 特定）**: `~/.claude/hooks/content_safety_gate.py` の `EXEMPT_PAGES` に
親の🌅朝のダッシュボード `722beb9e9827421aa5dbbef67c1c4688` は入っているが、
その子である以下2ページが入っていない。
- 📰今朝のニュースダイジェスト `391cf503a68f8194be35fec5aede8a5e`
- 📰dedupインデックス `391cf503a68f811088a7c5a70e6741c8`

**Why**: この2ページはEXEMPT_PAGESの登録条件（「対外公開されない」「草川本人しか見ない」「公開経路を持たない」）を
文字どおり満たす。ohayoが読むだけの内部台帳で、ブログ・SNSへの公開経路はない。
毎朝の自動ジョブが「安全網を書く行為」を止められている点で、
[[feedback_oyasumi_blocked_by_content_gate]] と同じ構造の事故。

**How to apply**: 修理は**草川の承認を取ってから**。安全ゲート本体の緩和なので勝手に触らない。
承認が出たら EXEMPT_PAGES に上記2つのIDをコメント付きで追加する。
📰ニュースDBの個別記事ページ（続報追記先）は**除外に入れてはいけない** —
記事本文はブログ・SNSへ流れる経路があるため、従来どおりゲートを通す。
それまでの回避策は本文をローカル退避（`drafts/<日付>_news_digest_PENDING.md`）して草川に手貼りしてもらう。

関連: [[project_content_safety_gates]] / [[project_hakushin_pack_gate_deny]] / [[project_news_briefing_system]]
