---
name: project-spark-skill
description: sparkスキル（小さな種→発信）2026-07-03新設。ひらめき・ニュースURL・活動メモを軽量に発信化する入口
metadata: 
  node_type: memory
  type: project
  originSessionId: 48b517ea-57f4-46bc-9778-7f8ea4b58341
---

2026-07-03、新スキル **spark** を `~/.claude/skills/spark/SKILL.md` に作成（設計書=drafts/2026-07-03_sparkスキル設計_v1.md）。

**役割**: ひらめき一言・ニュースURL1本・活動メモ数行という「小さな種」を、①受付分類 ②アーカイブgrep接地（省略禁止）③切り口2〜3案提示（1回確認・各案に不足情報1行・💾貯めておく選択肢つき）③.5 調査ブースト（切り口確定後に不足だけ狙い撃ち。軽微=自前WebSearch／構造的=kameyama-researcher or policy-researcherをD5厳守で1回だけ／両方不足=content-pipeline委譲。結果は事実パックとして生成に渡す）④選択分だけ生成（sns-content-creator該当PFのみ/blog-writer-normal等へ委譲）⑤fact-checker→risk-reviewer→D1 drafts保存→承認後1回Notion保存→🔖台帳、で発信に育てる。

**棲み分け**: 「記録」→nichijo／「メモ:」保存意図→smart-intake／まとまった素材→content-pipeline／「今日の発信」→daily-content-generator。ストックは新DBを作らず📣SNS投稿管理DB（ds 1bd98deb-）にタイトル💡・ステータス未着手で登録し、daily-content-generatorの朝棚卸しが拾う設計。

**燃費目標**: 切り口提案まで≤15K・保存込み30〜60K。重い調査エージェントは呼ばない（要調査級はcontent-pipeline委譲を提案）。

**状態**: 本体＋CLAUDE.mdトリガー行追記済み。要セッション再起動で有効化。実運用での初回フィードバック待ち。関連: [[feedback_content_generation_default_flow]] [[feedback_sns_citizen_lifescene_first]]
