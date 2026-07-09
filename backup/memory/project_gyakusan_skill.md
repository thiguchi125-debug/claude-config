---
name: project_gyakusan_skill
description: イベント逆算・準備漏れ拾いスキル gyakusan の構築記録（2026-07-09）
metadata: 
  node_type: memory
  type: project
  originSessionId: a7b8d821-7fc1-4265-bff8-9f4453960fc6
---

2026-07-09構築。発端＝toben-trackerのTodoist回収タスク提案を草川が不要と判断（「予定イベントから逆算して忘れられているタスクを追加してくれるスキルが欲しい」）。

**gyakusan**（skill・`~/.claude/skills/gyakusan/SKILL.md`）: Google Calendar（kusakawa.taku@gmail.com）＋Notion 3DB（🎤市政報告会df08b5ea／📅ミーティングノート26d7848d／会期ハブ16842e7f）から60日先までのイベント収集→種別別逆算テンプレ（報告会5ステージ・印刷入稿D-14・挨拶原稿D-3・主催イベントD-30許可等）→既存Todoistと突合→**不足分のみ一覧提案→承認分だけtd.py登録**。

設計の要＝**二層フィルタ**: 0〜14日先は全逆算／15〜60日先は「期限が14日以内に落ちるリードタイム長タスク」のみ（60日スキャンのノイズ抑制）。却下は`_declined.json`に記録し再提案しない。市政報告会は`_status.json`の完了ステージを除外、議会会期はgeneral-question-prepと重複提案しない。

**月曜ohayo連携**: ohayo SKILL.md末尾に「📌月曜の逆算チェック」節を追加（候補表示モード・5件超は畳む・火〜日は実行しない）。CLAUDE.mdトリガー表にも1行追加済み。

初回実運用フィードバック待ち。関連: [[project_toben_tracker]] [[feedback_ask_destination_and_deadline_before_register]] [[feedback_system_closing_loops_rot]]
