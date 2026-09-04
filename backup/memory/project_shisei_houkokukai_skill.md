---
name: project_shisei_houkokukai_skill
description: 市政報告会5ステージプロデューススキル（2026-07-04設計・実装）。企画相談→案内レポート→スライド→連動解説→前夜チェック。新設エージェント3本。初回実走フィードバック待ち
metadata: 
  node_type: memory
  type: project
  originSessionId: 04b5cad2-a2a6-42cd-b184-1f354d6249ec
---

# shisei-houkokukai スキル

2026-07-04 ブレインストーミング→批判的再検討10件反映→実装。設計書＝
`~/.claude/skills/shisei-houkokukai/design/2026-07-04-shisei-houkokukai-design.md`（正本スペック）。

- 5ステージ制・1起動1ステージ・草川承認ゲート・進捗正本 `_status.json`（Notion🎤報告会DBはミラー）
- 面白さ3軸＝参加型クイズ／自分ごと化／未来提示。解説＝ノート＋山場フル台本→スマホ縦PDF
- 新設エージェント: audience-experience-reviewer（テーマ価値＋聴衆冷読み・ペルソナは顔ぶれから生成）／
  district-issue-scout（地区×市政テーママップ・軽量パス唯一のagent）／district-hazard-analyst（地区防災カルテ・突合分析）
- Stage1は二段化（軽量→相談→深掘り）。逆算スケジュール→Todoist登録提案。短縮経路あり
- 次: 次回開催地区で実走→フィードバックをmemory化。engagement.mdは実開催の効きメモで更新する運用

関連: feedback_shisei_houkokukai_slides_claude_code feedback_shisei_houkokukai_voice_capture [[project_shisei_houkokukai_db]]
