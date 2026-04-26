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
- 状態：**v1 蒸留完了（2026-04-26 夜間自動）**。Origin Story refine済「一生、応援団であり続ける。／主役は、あなた。私はその背中を押し続ける。」。3軸確定：軸1「市民の声を、制度の最後の一歩まで運ぶ。」／軸2「命と暮らしの動線を、絶対に守る。」／軸3「学ぶ亀山から、選ばれる亀山へ。」。voice-dna 理想ボキャブラリー4本refine済。データ基盤：17/20セッション質問構造＋2023.9・2026.3議会フル原稿＋スピーチ3本＋SNS34・nichijo15・ブログ9＋選挙ドットコム5記事。朝レビュー待ち
- 譲れない原則・やらないこと（境界線）も同コンパスで管理
- 消費側：daily-street-speech / speech-writer / print-designer / blog-writer / sns-content-creator / council-material-creator / policy-validator が起動時に必ず参照
- 更新は Notion・ローカル両方を同期（最終更新日一致が原則）
