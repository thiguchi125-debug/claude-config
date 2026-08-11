---
name: deny
description: 📮発信候補パック(39dcf503-a68f-8101-…)はcontent_safety_gate.pyのEXEMPT_PAGES未登録。夜間ジョブは_pack_body_<日付>.txt→gate.py --pass経由で書く。8/11分はdenyされ未更新のまま
metadata: 
  node_type: memory
  type: project
  originSessionId: 6121b579-e450-47dd-bfdf-29f918bf851c
  modified: 2026-08-11T18:26:30.261Z
---

夜間SNS候補パックジョブ（nightly_intake.sh 第2ステージ）の Step4 は 📮発信候補パック（page_id `39dcf503-a68f-8101-beac-c2883ed87e70`）の「## 本日の候補」節を全置換するが、このページは `~/.claude/hooks/content_safety_gate.py` の `EXEMPT_PAGES`（📥未分類インテーク・📮SNS便ステータスのみ・2026-08-11草川承認で追加）に**入っていない**ため、本文書き込みが必ず deny される。

**Why:** これで 2026-08-11 分の更新が落ち、Notion側は8/11朝〜8/12未明まで「収集日2026-08-10」の古い内容のまま置かれた（朝夕便が古い在庫判断を読む）。同じ deny で📥未分類インテークが5晩詰まった前例があり、内部運用ログが安全網に阻まれる同型の事故。

**How to apply:** 迂回して設定を書き換えない（EXEMPT_PAGES追加は公開経路の確認込みで草川判断）。2026-08-12夜の実走で確立した通し方＝①置換本文を `~/.claude/scripts/sns-routine/_pack_body_<日付>.txt` に書く（.txtなので機械チェックは素通し）②content-fact-checker→content-risk-reviewerの順に**全文**を渡して通す③`python3 ~/.claude/scripts/gate.py <file> --pass`（指紋TTL2時間）④notion-update-page。`--pass` は2エージェントを実際に通した時だけ付ける。なお gate.py は `_content_gate.json` を丸ごと上書きするので他ジョブと同時刻に走らせない（[[feedback_content_gate_json_concurrent_clobber]]）。関連＝[[feedback_safety_gates_before_notion_save]]／[[project_content_safety_gates]]
