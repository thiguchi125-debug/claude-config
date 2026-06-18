---
name: feedback_print_layout_architect_agent
description: 印刷物のレイアウト作り込み（画像の大型化・text-beside-image・余白撲滅）はprint-layout-architectエージェントに任せる。natural-design-reviewerは破綻チェックのみで不十分
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2ba09108-7a9c-4b72-b133-41913e6313f1
---

印刷物（市政報告レポート／チラシ等 HTML→PDF）のレイアウト品質で草川が繰り返しダメ出しする論点＝「画像が小さくて読めない」「中途半端な余白」「文章を狭めて画像の横に」を、毎回手で直さずに済むよう専用エージェント **print-layout-architect**（`~/.claude/agents/print-layout-architect.md`）を新設した（2026-06-19）。

**Why:** natural-design-reviewer は「物理破綻（切れ/はみ出し）」しか見ず「出荷可」を出すが、草川の求める水準（主役ビジュアルの可読サイズ・死に余白ゼロ・エディトリアルな対面構図）には届かず、安知本版で何度も手戻りが発生した。

**How to apply:** 印刷物のデザインを「整えて/作り込んで/画像大きく/余白なくして/プロ水準に」系の依頼が来たら、レビューでなく **print-layout-architect を起動して実装まで完了**させる。絶対原則＝①地図/図解/注記付き画像はラベルが判読できるサイズ（横長地図はコンテンツ幅60〜100%）②死に余白は text-beside-image の2カラム対面（grid align-items:stretch＋object-fit:cover）で撲滅③必ずChromeレンダリング→PNGをReadで実画素確認→合格まで反復④ページ配分は全体最適で組み替え可。新設直後はレジストリ未登録のことがあるため、その場合は general-purpose に該当.mdをReadさせて成り代わらせる（[[feedback_agent_registry_partial_load]]）。安知本版v10で実証（地図58mm→166mm幅・章1/章3対面2カラム化・両面下端まで充填）。
