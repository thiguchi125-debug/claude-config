---
name: feedback-publications-binary-storage
description: 印刷物の生バイナリ素材（PDF/HTML/画像）保管時、reports/leaflets直下のtxtフラット構造を汚さず案件別サブフォルダで隔離する規約
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7cd7b9e5-6eea-4583-9b48-2db2de37a44a
---

印刷物バイナリ素材（完成版PDF・HTML源泉・写真素材・QRコード等）を `~/.claude/agents/knowledge/kusagawa_archive/02_publications/` 配下に保管する時は、**reports/ leaflets/ 直下に直接置かず、`<YYYY-MM>_<案件名>/` のサブフォルダに隔離**する。

**Why:** reports/ と leaflets/ は既存txt群（700件超）がフラットに並ぶgrep最適化レイヤーで、ここにバイナリ素材を直接置くと（1）grep結果が汚れる（2）テキスト資産とバイナリ素材が混在して可読性が落ちる（3）案件単位での参照性が崩れる。サブフォルダ運用ならテキストgrep資産は無傷のままバイナリも案件別にまとまる。2026-05-14 Desktop整理時に確立。

**How to apply:**
- 案件別フォルダ命名: `<YYYY-MM>_<案件名>/`（例: `2026-04_亀山建設労働組合_市政報告/`、`2026-05_木下版_市政報告/`、`2026-04_応援カード/`）
- 配下構成は案件によって自由（`HTML源泉/`、`写真素材/`、`画像/` 等の機能別小分類は推奨）
- 完成版PDFは案件フォルダ直下、素材は機能別サブフォルダへ
- 中間版（v2〜v11等の試行錯誤PDF）は最終確定後に削除、最終版＋直前版1本のみ保持
- 学習素材（NotebookLM出力等）は `05_resources/notebooklm/<テーマ>_<R年度>/` へ
- Desktop直下にバイナリ素材を散らかさず、印刷物制作完了時にこの規約で archive 化する
- 関連: [[feedback-archive-grep-keyword-expansion]]
