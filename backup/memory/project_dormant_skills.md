---
name: project-dormant-skills
description: 起動固定費を下げるため休眠スキル4本を ~/.claude/skills_dormant/ に退避（2026-09-06）。戻すときは mv 1回。CLAUDE.md トリガー早見のショート動画/取込行は退避中
metadata: 
  node_type: memory
  type: project
  originSessionId: f1d30a5a-6234-41b6-83cf-d8368330529f
  modified: 2026-09-06T10:50:40.772Z
---

2026-09-06 棚卸し（14日で起動0回・他スクリプトから参照なし）で草川が選んだ4本を `~/.claude/skills/` から `~/.claude/skills_dormant/` へ移動した:
**slide-deck-prep／aisatsu-prep／daily-content-generator／drive-intake**。
残す判断をしたもの: ai-kusakawa・chiku-report・shisei-houkokukai（選挙前の報告会で使う可能性）。

**Why:** 起動固定費（毎セッション中央値78.6K）の大半はスキル・エージェント説明文。使わない説明文を毎回読ませない。

**How to apply:** 「〇〇スキルを戻して」で `mv ~/.claude/skills_dormant/<name> ~/.claude/skills/<name>`。退避中のトリガー語（「〇〇で挨拶したい」「スライド作って」「今日の発信」「取り込んで」）が来たら、戻すか代替（community-rally-speaker／shisei-houkokukai Stage3／content-pipeline／夜間 `_root_intake.py` 任せ）を1問で聞く。次の候補はエージェント48本の同じ棚卸し。関連: [[feedback_maintenance_weekly_window]]
