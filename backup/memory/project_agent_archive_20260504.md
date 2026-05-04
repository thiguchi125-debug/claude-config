---
name: エージェント24本を_archive/へ退避
description: 2026-05-04トークン節約対応。45本中24本を~/.claude/agents/_archive/へ移動して説明文を非ロード化。news-briefing毎朝6:00 cronも無効化
type: project
originSessionId: fd0375ac-61da-45e6-a6f6-48fa04965700
---
2026-05-04に消費トークン削減のため実施。**統廃合（削除/マージ）はしていない**、説明文の自動ロードを止めるための単純な退避。必要時は `mv _archive/<name>.md ./` で即復活。

## アクティブ（21本・~/.claude/agents/直下）
content系: blog-writer / blog-writer-normal / sns-content-creator / sns-content-polisher / content-editor / content-fact-checker / content-risk-reviewer / notion-saver
リサーチ系: kameyama-researcher / policy-researcher / policy-synthesizer / policy-validator
議会系: agenda-analyzer / council-material-creator / counter-argument-simulator
発信系: daily-street-speech / speech-writer / video-content-strategist
市民対応: citizen-inquiry-responder
印刷系: print-designer / photo-curator

## アーカイブ（24本・_archive/）
- AIインタビュー2本（ai-interview-config-designer / ai-interview-sns-poster）
- デザイン系3本（design-director / design-doc-reviewer / design-inspiration-researcher）
- dev tool系3本（bug-quality-checker / skill-validator / kusakawa-voice-analyst）
- 政策エキスパート11本（policy-expert-* 6本 + fiscal-simulator / packaging-strategist / roadmap-designer / stakeholder-mapper / comparison-benchmarker）
- archive/research系2本（policy-archive-miner / policy-compass-curator）
- 選挙系1本（electoral-district-strategist）— 2026-10-25選挙近づいたら復活検討
- 集会系1本（community-rally-speaker）

## 廃止したcron
- trig_01WXgkt4JqANvhi1YuQLGsEQ「毎朝ニュースブリーフィング 6:00 JST」 → enabled:false
- 復活時はhttps://claude.ai/code/routines/trig_01WXgkt4JqANvhi1YuQLGsEQ で enabledトグル

## 残存cron（4本）
- trig_01MoNQUK1w6oS6HacCSCXxJv（プロジェクト化判定1週間レビュー、2026-05-08一発）
- trig_01KfnWW7sA6xGTH3ZX251p5b（選挙週次レビュー、毎週金曜）
- trig_01KazqqjgMaw1H7w1rsjgfTq（policy-update-monthly、毎月1日）
- trig_01TfKn6JL5o6JjTLdLaT8Zin（policy-update-weekly、毎週日曜）

## 棚卸し未完了
草川判断待ち：(1)policy-expert 11本の統廃合、(2)アクティブ21本の更なる削減余地、(3)選挙近づいた際のelectoral-district-strategist復活タイミング
