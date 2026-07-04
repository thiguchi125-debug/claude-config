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
- [x] ローカルデザインシステム構築（2026-07-05・21ファイル・カード10枚。preview系は外部参照ゼロ検証済）
- [x] design-studioスキル作成（登録済・トリガー「チラシ作って」等）
- [x] CLAUDE.md・print-designer/print-layout-architect「テンプレ第一手」追記
- [ ] /design-login → claude.ai/design push（**草川操作待ち**。認可後に create_project「草川たくやデザインシステム」→差分push→カード表示確認）

## 構築時の発見（制作時に効く注意）
- 市政報告レポートv22はブランド4色でなく「インク節約パレット」（緑#1f7a3a/深緑#0e4d27/金#c89211・ベタ塗り3%以下）。**1制作物1パレット・混用禁止**（colors.htmlに両パレット収録）
- lime下線の正本値=`box-shadow: inset 0 -0.28em 0 #c7ff4a`（gradient hard-stopはPDF暗化で禁止）
- flyer_a4正本はeスポーツflyer_a2.html採用（TUIRTLE公式ロゴ準拠）。旧flyer.htmlにはピルバッジ（AI-LP禁止信号）あり採用不可
- leaflet_trifoldは名前と裏腹に実態A4両面1枚もの（842×1190px×2面・印刷scale 0.9426）
- template.htmlはposter/flyer/leafletが元ディレクトリのassets/へ相対参照（reportのみbase64単体完結）→制作時は案件フォルダへassetsごと複製

関連: [[feedback_design_quality_bar_natsumatsuri2026]] [[feedback_print_layout_architect_agent]] [[feedback_flyer_avoid_ai_saas_aesthetic]] [[feedback_no_emoji_ai_smell]] [[reference_senkyo_leaflet_v3_files]]
