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

**2026-09-05 夜 追記**: フェーズ2のA完了＝A-1仕分け（昇格7／吸収53／破棄29／対象外81）→A-2吸収53/53。発信系ルールの正本＝各agent/SKILL末尾📌節＋design_system＋GUARDRAILS【1】【8】＋fact_ledger/verified_facts.tsv（事実14行）。旧メモ85件は `~/Archive/_trash_pending_2026-09-05/` に退避・未削除（草川承認後にrm）。進捗ログ＝`drafts/2026-09-05_A1_発信系ルール仕分け表.md` §6。残＝C（画像順序固定・nano-bananaルート削除）→H（発信オーケストレーター・未設計）。⚠字幕帯座標が specs.json image.9:16 band_from=1200 と check_subtitle_band.py 1240 で40px不一致＝草川判断待ち。

**2026-09-05 夜 追記（C完了）**: 画像制作の固定順序（採寸→写真→レンダ→機械採点が通るまで目視しない→目視1回→勝負所のみreviewer）を short-video-create Step5／content-pipeline 4-A＋visual-assets-playbook A-3／photo-post Step4／short-video-image-designer 制作ループに書き込み。nano-banana（AI画像生成）ルートは発信画像から全廃＝short-video-create ルートB・daily-content-generator 4-8・image-designer・photo-post・slide-deck-prep・sns-routine/video_stage_prompt・short_video_templates/README から削除。agent本体 `nanobanana-prompt-designer.md` は `~/Archive/_trash_pending_2026-09-05/agent_nanobanana-prompt-designer.md` へ退避（ai-kusakawa キャラ生成と design-studio 装飾素材庫のプロンプトカードは素材の一回生成として残置）。字幕帯は草川決定で specs.json band_from=1240 に修正・全正本整合。修正案＝`drafts/2026-09-05_C_画像順序固定_修正案.md`。**残＝H（発信オーケストレーター・未設計）**＝着手前に brainstorming で草川の関心を1問ずつ確認。Notion「エージェントトリガー一覧」の nanobanana 行は未削除（次にNotionを開くとき1行消す）。

- 2026-09-05 夜（再開セッション）: C再検証＝字幕帯 specs.json／check_subtitle_band.py とも y1240-1460 で一致確認。short-video-image-designer 説明文の nanobanana-prompt-designer 参照を削除（残参照0）。退避86件は「まだ置いておく」を草川選択（削除は後日1問で再確認）。

**2026-09-05 夜 追記（E実装）**: Hは並行セッションで4件に分解済（①夜間便修理／②検証台帳E／③単一入口spark拡張／④司令塔＝候補パック再設計含む）。②を案A（派生版は1テーマ1回の派生ゲート）で実装＝フック `fact_ledger_autolog.py` がテーマ内台帳 `_ledger.json`（claims/approved_texts/gate_runs）を自動生成、content-gate-lite に派生モード節、呼び出し側8本に `ledger:` 配線。詳細＝設計書§7「E 実装」。**実運用未**＝次の発信1本で gate_runs≤3 を確認。残＝③④（未設計・要ブレスト）。
