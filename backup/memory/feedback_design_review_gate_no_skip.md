---
name: feedback_design_review_gate_no_skip
description: 印刷物デザインは確定前に必ずnatural-design-reviewerを通す。自分の目視だけで確定しない
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 68a37f74-27ea-4756-afee-ee4d6990d4f9
---

デザイン制作（design-studio／print-designer／print-layout-architect）で、**修正のたびに自分でレンダリング→自分で目視して確定してしまい、独立した批判エージェント（natural-design-reviewer）を通さなかった**ことを草川に指摘された（2026-07-05 三寺コスモス種まきチラシ制作中）。「客観視・批判エージェントが機能していないのでは？」と。草川は「確定前に必ず批判エージェントを通してからお見せする」運用に **「そうして」で同意**。

**Why:** 自分の目視は主観に寄る（対症療法の堂々巡りに陥りやすい＝スクリム濃くする↔フチ付ける、の往復）。独立した第三者エージェントのEYES-FIRST判定を挟まないと、物理破綻や「かえって悪化」を見逃す。design-studio SKILL Step4・rules.md §4に元々ある工程を、反復修正の途中で省略したのが失敗。

**How to apply:**
- 対外配布のデザイン物は、**草川に見せて確定を仰ぐ前に必ず natural-design-reviewer を1回通す**。初版だけでなく、レイアウト構造を変えた修正版・複数回いじった後も通す（微小な文言差し替えのみは任意）。
- 「自分で直して自分で見ただけ」で"完成"と言わない。批判エージェントの判定（破綻ゼロ or 指摘）を添えて提示する。
- 賑やかな写真の上に文字を直接重ねる構成が読みにくくなったら、対症療法（スクリム/フチ）で往復せず、**構造から分離**（写真はクリーン帯＋文字は無地地）を検討する。
- 関連: [[feedback_rules_reside_in_agents]]（design-studio/print系のルールは担当agent/SKILL末尾に常駐）
