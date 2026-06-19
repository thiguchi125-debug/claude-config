---
name: feedback_print_layout_architect_stalls
description: print-layout-architectエージェントが0ツール実行で毎回停止する。印刷物レイアウトは自分で実測ループするのが確実
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 59399be9-ae7e-4144-95af-57b7906223ca
---

print-layout-architect エージェントは、Agentツールで起動しても **0 tool_uses で即停止**（bashコマンドを文字列でエコーするだけの空応答を返す）する事象が連続発生（2026-06-19/20 安知本版v11→v12制作で2回連続）。同セッションで natural-design-reviewer は正常稼働したため、このエージェント型固有の部分ロード不全（[[feedback_agent_registry_partial_load]] と同種）。

**Why:** 起動を期待して投げると毎回空振りし、草川を待たせる（「時間がかかりすぎる」不満の一因）。

**How to apply:**
- 印刷物のレイアウト作り込み（はみ出し解消・空白撲滅・写真/地図サイズ調整）は **print-layout-architect に頼らず自分で実装→Chrome実測→反復**する。
- 物理破綻チェックだけは natural-design-reviewer が使える（ただし「余計な空白」のような美的判断は拾えない＝v11を出荷可と誤判定した。最終判断は草川の目視）。
- 印刷物の「下端切れ」は `overflow:hidden` が破綻を隠すので、スクショ目視でなく **Chrome DOM で `scrollHeight - clientHeight = 0`** を実測するまで詰める。さらに `margin-top:auto` は「詰めた余りを1か所に大穴として溜める」ので、空白嫌いの草川案件では避け、コンテンツ実寸（写真・地図の拡大）でページを満たす。
- 横長地図など widthいっぱいにすると縦が伸びすぎる図は、`aspect-ratio`＋`object-fit:cover`＋`object-position` で不要側（空/山並み）だけクロップして全幅化し、左右の死に余白を消す。ラベルが切れないよう object-position を実レンダリングで確認。

関連: [[feedback_print_layout_architect_agent]]（このエージェントの当初新設記録）/ [[feedback_agent_registry_partial_load]]
