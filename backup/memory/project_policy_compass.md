---
name: 政策コンパスシステム
description: 草川たくやの不変の3軸を蒸留・保守する政策コンパス。policy-compass-curatorエージェント＋ローカルmd＋Notionページの3点セット
type: project
originSessionId: 2ee4f9d6-fcf8-4aeb-a45d-5e5c2c19da16
---
2026-04-26新設。草川たくや（亀山市議会議員）の8年の活動を「不変の3軸」として蒸留し続ける政策コンパスシステム。

**Why**: 街頭演説・応援カード・選挙公報・ブログ・SNS・議会質問など、すべての発信に「草川は何を、なぜ、どこまでやるのか」の単一の真実が必要。これまで存在しなかった（policy-archive-minerはテーマ別生発言、🎯政策候補DBは未来形、政策まとめページは作業メモ、voice-dnaは表現面のみ）。

**How to apply**:
- 起動：「政策コンパスを蒸留して」「政策の軸をまとめて」「コンパス更新」等で `policy-compass-curator` エージェント発火
- 3点セット：
  1. エージェント `policy-compass-curator`（cyan, opus）— archive-miner themes 3本を読み込み、横断する3軸を蒸留
  2. ローカルmd `~/.claude/agents/knowledge/kusagawa_archive/policy_compass.md`（agent向け詳細版）
  3. Notion 🧭草川たくや 政策コンパス（id:34ecf503-a68f-8117-afca-ecab391eb84d、親=🎯政策アップデートハブ）
- Origin Story：「**一生応援部魂で、市民を全力応援したい**」（草川指定・確定）
- 状態：v0 骨格のみ（2026-04-26時点）。3軸は未蒸留、curator 初回実行で確定予定。3軸候補は7本観察済（運用ギャップ／行かない窓口／誰ひとり取り残さない／EBPM／子どもの権利／リニア活用／公共交通＋医療アクセス）
- 譲れない原則・やらないこと（境界線）も同コンパスで管理
- 消費側：daily-street-speech / speech-writer / print-designer / blog-writer / sns-content-creator / council-material-creator / policy-validator が起動時に必ず参照
- 更新は Notion・ローカル両方を同期（最終更新日一致が原則）
