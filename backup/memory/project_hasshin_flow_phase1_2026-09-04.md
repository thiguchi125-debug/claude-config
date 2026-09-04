---
name: project_hasshin_flow_phase1_2026-09-04
description: 発信フロー構造改善フェーズ1（2026-09-04完了）＝学びの置き場の一本化・gate.pyの判型分岐・旧規格の一掃。フェーズ2以降の前提
metadata: 
  node_type: memory
  type: project
  originSessionId: 4f861515-9d04-4eb5-bae8-c410b56fda10
  modified: 2026-09-04T08:57:48.549Z
---

発信フロー（記事・SNS・動画原稿・画像・ゲート）の構造改善。設計書＝`~/.claude/projects/-Users-kusakawatakuya/drafts/2026-09-04_発信フロー構造改善_design.md`（改修A〜G・フェーズ1〜3・決定D1〜D6）。

**フェーズ1は2026-09-04に完了。以後は次の3つが前提になる。**

1. **エージェントの学びの置き場は `~/.claude/agent-memory/<agent>/` ただ1つ。** それ以外への書き込みは PreToolUse フック `hooks/agent_memory_path_guard.py` が deny する（Write/Edit/Bash）。作業フォルダに書き捨てられていた167件を回収済み。**追記したら同じフォルダの `MEMORY.md` に索引1行を必ず足す**——索引に無いファイルはagentから読まれない（回収時、正規フォルダにありながら索引漏れが116件あった）。

2. **`gate.py` は判型を自動判定する。** 同名PNGの実寸→HTMLの `html/body/.stage/.canvas` の width/height→既定9:16 の順。字幕セーフ帯ゲートは 1080×1920 のときだけ回る。**`--canvas` を手で渡す必要はもう無い**（引き継ぎメモにあった回避策は不要）。判型別の規範は `scripts/check_image_design.py` の `SPECS`＝フェーズ2で `specs.json` に移す予定の暫定単一ソース。

3. **サムネ・OGPの既定は 1600×900。** 「着手前に元写真の有無を聞く」旧ルールは廃止・ファイルごと削除済み（photo-curator で自分で選び切る）。正本は `design_system/references/thumbnail/_karte.md`。

**フェーズ2の入口**＝B（`SPECS`→`specs.json`）／A（発信系ルール全数棚卸し・正本一本化）／C（画像の制作順序を固定・nano-bananaルート削除）。

関連: [[feedback_thumbnail_crop_and_tone]] [[feedback_gate_kind_of_by_filename]] [[feedback_rules_reside_in_agents]]

**2026-09-05 追記**: 尺規定を「許容35〜50秒／目標45〜50秒」に統一（食い違い3種を解消）。フェーズ2のB完了＝規格値は `~/.claude/scripts/specs.json` が単一ソース（読み込み口 `specs.py`）。チェッカー4本（check_image_design／check_content_limits／check_overflow／gate）は数値を持たない。残＝A（発信系ルール棚卸し）・C（画像の順序固定・nano-bananaルート削除）・H（発信オーケストレーター＝未設計・草川の関心）。詳細は設計書§7。
