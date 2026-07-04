---
name: project-design-studio
description: Canva超えデザイン制作環境 — 草川デザインシステム(claude.ai/design正本)＋design-studioスキルの設計と進行状況
metadata: 
  node_type: memory
  type: project
  originSessionId: 2bf8c927-8f74-4470-b195-5ffa765f5c70
---

# 草川デザインスタジオ環境（2026-07-04 設計確定・実装）

## 目的
Canva以上のクオリティのチラシ等デザイン制作を、Claude Code起点で1パス実行できる環境。
claude.ai/design のテンプレート群を「正本」とし、既存デザイン系エージェント9本をフル稼働させる。

## 確定した設計判断（草川承認済 2026-07-04）
1. **claude.ai/design＝正本**。「草川たくやデザインシステム」プロジェクトをDesignSyncでローカルと同期。ブラウザでカード一覧からテンプレを選ぶ（Canvaのテンプレ一覧に相当）。
2. **初期範囲＝印刷物コア4種**：チラシA4／ポスターA3・A2／市政報告レポートA4両面／リーフレット三つ折り。SNS画像・スライドは拡張フェーズ。
3. **品質ループ＝標準型**：print-layout-architect（Chrome実測EYES-FIRST）→natural-design-reviewer→安全ゲート→PDF。design-director（8軸）は選挙物・ポスター等の勝負所のみ承認制で追加。

## 3層構成
- **層1 デザインシステム正本**: `~/.claude/agents/knowledge/design_system/`
  - `foundations/`（ブランド色 #c7ff4a/#1f5a3a/#0f3d27/#f3efe4・タイポ・禁止事項=絵文字/AI製SaaS LP風）
  - `components/`（ライムバー見出し・QRブロック・討議資料フッター・text-beside-image行等）
  - `templates/`（flyer_a4／poster／report_a4_duplex／leaflet_trifold）
  - プレビューHTMLは1行目に `<!-- @dsCard group="…" -->` マーカー → claude.ai/designでカード化
  - 種: 木下v22（print_templates/district_report/）・中庄夏祭りポスター2026（drafts/2026-08_中庄夏祭りポスター/poster.html）・選挙リーフレットv3（kusagawa_archive/02_publications/leaflets/2026-05_senkyo_leaflet_v3/）
- **層2 design-studioスキル**: `~/.claude/skills/design-studio/SKILL.md`
  - トリガー「チラシ作って」「ポスター作って」「〇〇のチラシ」等
  - 要件ヒア1回→テンプレ候補2〜3提示→photo-curator/アーカイブgrep→print-layout-architect→natural-design-reviewer→fact-checker→risk-reviewer→PDF自動open→保存先マップ準拠保存→**テンプレ昇格還元**（良作をdesign systemへ部品化しclaude.ai/designへ再push）
- **層3 運用接続**: CLAUDE.mdトリガー早見表・print-designer/print-layout-architectにデザインシステム第一手参照を追記

## 同期運用
- push: DesignSync（list_files→差分→finalize_plan→write_files）。wholesale replace禁止・部品単位。
- 草川の一回きり操作: **/design-login**（未実施だとDesignSync未認可）

## 進行状況
- [x] 設計承認（2026-07-04）
- [ ] ローカルデザインシステム構築
- [ ] design-studioスキル作成
- [ ] CLAUDE.md・エージェント追記
- [ ] /design-login → claude.ai/design push（草川操作待ち）

関連: [[feedback_design_quality_bar_natsumatsuri2026]] [[feedback_print_layout_architect_agent]] [[feedback_flyer_avoid_ai_saas_aesthetic]] [[feedback_no_emoji_ai_smell]] [[reference_senkyo_leaflet_v3_files]]
