---
name: rules-reside-in-agents
description: タスク特化ガードルールはMEMORY.md索引でなく担当agent/SKILL本文に常駐させる（2026-07-04大移設の運用規約）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ed827cf3-b41b-4305-a638-19d97fd693a5
---

2026-07-04、MEMORY.md索引の肥大（32.9KB・毎セッション約3万トークンの固定税）を解消するため、特定agent/スキルでしか使わないガードルール60本を「働く現場」へ移設した。

**Why:** MEMORY.mdは全セッションに自動読込されるが、サブエージェントには届かない。ルールは実際にそれを使うagent定義/SKILL.md本文に置くほうが、(a)常駐トークンを削減でき、(b)サブエージェント実行時に確実に効く。[[feedback-system-closing-loops-rot]]（記憶依存＝腐る）のコンテキスト版。

**How to apply:**
- 新しいfeedbackを保存するとき、それが**特定のagent/スキル実行時にしか効かないルール**なら：①memoryファイルは通常どおり作成（正本・履歴用）②同じ内容の1行要約を対象agent .md／SKILL.md末尾の「## 📌 恒久ガードルール」節に追記③MEMORY.md索引には個別行を足さず、既存の「📦 移設済みルール束」の該当束にカウントを反映するだけ
- **全タスク横断のルール**（禁止表現・帰属事故・Notion罠・タスク運用等）だけをMEMORY.md索引の個別行にする
- 移設済み7束: ohayo/oyasumi16本・ショート動画7本・印刷物16本・ブログ5本・SNS/AIインタビュー7本・news-briefing5本・街頭演説4本

**未了フォロー:**
1. ~~字幕セーフ帯座標統一~~ ✅2026-07-04完了：正本=y1240-1460（2026-07-02京都直通で草川承認済のため新しい方に統一。旧y1150-1470は帯を内包する広め運用＝既存テンプレinsert_image_v1はそのままで互換）
2. ~~X140字掃除~~ ✅2026-07-04完了（3agent・16箇所・grep残存ゼロ）
3. ~~oyasumi td.py化~~ ✅2026-07-04完了（13箇所修理・CLAUDE.mdのoverride文言も撤去）。oyasumiの繰越は「期限据え置き→翌朝morning承認」設計に確定。週次完了集計はTodoist MCP find-completed-tasks使用（td.pyにcompletedコマンド追加は将来判断）
