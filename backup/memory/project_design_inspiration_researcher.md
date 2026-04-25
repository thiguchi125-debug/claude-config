---
name: design-inspiration-researcherエージェント新設
description: 2026-04-25新設。政治家広報物のデザイン事例を収集・分析・仕様化してprint-designerに渡す専任エージェント
type: project
originSessionId: 117eaaff-c146-4719-8294-a6baba4be080
---
2026-04-25、印刷物デザインの上流リサーチを担う3つ目のエージェント新設。

**役割**: ネット上の政治家リーフレット/チラシ/ポスター/応援カード等の高品質デザインを収集・8軸分析（color/layout/typography/photo/copy/visual/brand/production）、共通成功パターン抽出、草川向けに翻訳した具体CSS/HTMLスペックとしてprint-designerに引き渡す。

**Why**: 「もっと洗練させたい」「他の議員みたいに」という抽象フィードバックを、毎回ゼロから試行錯誤せず、参照事例ベースで具体仕様に変換するため。応援カードv1〜v7で発見したノウハウ（緑×金、写真クロップ位置、タイトル大型化）の上位概念を蓄積する場所として位置づけ。

**How to apply**: 
- ユーザーが「印刷物作りたい」と言った時、内容によって以下の流れ:
  - 既存パターン適用で良い → print-designer単独
  - 新しい方向性を探りたい → design-inspiration-researcher → print-designer
  - リニューアル全般 → design-inspiration-researcher（先行調査）→ photo-curator（写真選定）→ print-designer（生成）→ design-doc-reviewer（QA）
- 過去調査の蓄積場所: `~/.claude/agents/knowledge/design_references/`、INDEX.mdで管理
- 著作権配慮: 直接コピー禁止、参考レベルに留め草川独自表現に翻訳

**3エージェント連携系統**:
- design-inspiration-researcher（リサーチ・仕様化）
- photo-curator（写真選定）
- print-designer（HTML/CSS→PDF生成）
- design-doc-reviewer（既存、品質QA）
