---
name: design-directorエージェント新設
description: 2026-04-25新設。プロ級デザインへの昇格を担う上位ロール。design tokens設計＋pro-levelレビューでprint-designer出力をaward-caliberに引き上げる
type: project
originSessionId: 117eaaff-c146-4719-8294-a6baba4be080
---
2026-04-25、印刷物デザイン4エージェント体系に **design-director（デザインディレクター）** を追加し、5エージェント体制完成。

**役割**: print-designerが「実装」、design-directorは「戦略・原則・最終調整」の上位ロール。良いデザイン→プロ級への昇格を担当。

**4つのオペレーティングモード**:
1. **Mode A**: Upstream Design System (制作前) - design tokens 確定 (color/type/space/grid/radius/shadow)
2. **Mode B**: Design Brief (制作前) - 戦略方向性 + ムードボード + ヒエラルキー
3. **Mode C**: Pro-Level Refinement (制作後) - 8原則(C/R/A/P/B/H/W/U)で軸別レビュー → surgical修正指示
4. **Mode D**: A/B/C Variants - 戦略レベル3-5案で比較

**搭載知識**:
- 草川向け確定 design tokens（緑×金、CSS variables形式）
- タイポペアリング（ヒラギノ角ゴW6/W3/W8、明朝混植ルール）
- カラーハーモニー（60-30-10ルール、Split Complementary応用）
- グリッド（12カラム × 8pt-grid × baseline）
- 視線フロー（Z-pattern / F-pattern）
- 印刷入稿（CMYK変換、PANTONE指定、bleed/trim/DPI）
- Award referenceを意識（AIGA / Communication Arts / D&AD）

**5エージェント連携体系（完成）**:
```
design-inspiration-researcher → リサーチ
       ↓ (references)
design-director → design system + brief
       ↓ (tokens, instructions)
photo-curator → 写真選定
       ↓
print-designer → HTML/CSS実装
       ↓
design-director → pro-level refinement レビュー
       ↓ (surgical fixes)
print-designer → 修正実装
       ↓
design-doc-reviewer → 最終QA
```

**Why**: AI生成物特有の「ちょっと整いすぎ」「テンプレ感」を排除し、プロのデザイナーが作ったように見える品質を再現可能にするため。応援カードv8まではprint-designer単独で良好だが、より上位の品質（受賞作レベル）を目指す時に必須。

**How to apply**:
- 「もっとプロっぽくしたい」「デザインを格上げ」「最終チェック」発話 → design-director Mode C
- 「設計指針作って」「デザインシステム」 → Mode A/B
- 「3案比較したい」 → Mode D
- 制約: 赤禁止/絵文字禁止/voice-dna整合/AIっぽさ排除（意図的な非対称・呼吸感を残す）

**保存先**: design system markdown は `~/.claude/agents/knowledge/design_system/` 配下、参照事例は `~/.claude/agents/knowledge/design_references/` 配下
