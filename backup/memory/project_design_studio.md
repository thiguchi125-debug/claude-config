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
- [x] /design-login → claude.ai/design push 完了（2026-07-05）。プロジェクト「草川たくやデザインシステム」projectId=`b84082a3-d0ff-40d6-a256-308e08910c3c`・20ファイル・カード10枚register済（v1_refinement_spec.mdはローカルのみ）。以後の更新は差分push（list_files→finalize_plan→write_files・wholesale replace禁止）
- [x] **v2初実走の顛末（2026-07-07〜08・最重要教訓）**: 市政報告レポート試作で「参照駆動」の初版（西宮市議の自作紙面を模写）を草川が「素人以下のAI臭さ。プロのデザイナーが作ったようなデザインが必要」と**却下**。教訓＝**参照の質が出力の天井**（プロ制作物のみ参照可・SKILL.mdに質ゲート恒久追記済み）。草川本人が広報かめおか見開きをベンチマーク指定→design-director仕様書（design_spec_kameoka.md・罫線囲みゼロ/ベタ帯ゼロ/明朝×ゴシック/ジャンプ率4倍+/非対称グリッド/円形ヌメラル1点/warm paper #fbfaf6）→かめおか型v2で組み直し→レビュー合格。**AI臭の正体＝箱の集合・ベタ帯反復・単一ゴシック・均等グリッド・純白+中央寄せ**（仕様書§0に却下理由5点明文化）。以後の印刷物はこの水準が基準。プロ参照は references_pro/（かめおか表紙+見開き・保持）
- [x] **v2センス強化（2026-07-07・仕様=design_system/v2_sense_upgrade_spec.md）**: 「硬い・暗い・AIっぽい」の根因＝種4作品が全部Claude自作の閉ループと診断。①design-studio Step1を**参照駆動制作**に改修（外部参考2〜3枚収集必須・print-layout-architectに参照Read模写指示・素材コピー禁止ガード）②`foundations/styles/` **スタイルレシピ5種**新設（淡色イラスト/ダーク×ライム/インク節約/写真大胆/和風。外部良作分析ベース・カード5枚push済）③`assets/illustrations/` **イラスト素材庫**新設（nano-bananaプロンプトカード20枚・**草川のGemini生成待ち**・いらすとやは政治利用禁止規約のため不使用・白背景素材はmix-blend-mode:multiplyで合成）

## 構築時の発見（制作時に効く注意）
- 市政報告レポートv22はブランド4色でなく「インク節約パレット」（緑#1f7a3a/深緑#0e4d27/金#c89211・ベタ塗り3%以下）。**1制作物1パレット・混用禁止**（colors.htmlに両パレット収録）
- lime下線の正本値=`box-shadow: inset 0 -0.28em 0 #c7ff4a`（gradient hard-stopはPDF暗化で禁止）
- flyer_a4正本はeスポーツflyer_a2.html採用（TUIRTLE公式ロゴ準拠）。旧flyer.htmlにはピルバッジ（AI-LP禁止信号）あり採用不可
- leaflet_trifoldは名前と裏腹に実態A4両面1枚もの（842×1190px×2面・印刷scale 0.9426）
- template.htmlはposter/flyer/leafletが元ディレクトリのassets/へ相対参照（reportのみbase64単体完結）→制作時は案件フォルダへassetsごと複製

関連: [[feedback_design_quality_bar_natsumatsuri2026]] feedback_print_layout_architect_agent [[feedback_flyer_avoid_ai_saas_aesthetic]] [[feedback_no_emoji_ai_smell]] [[reference_senkyo_leaflet_v3_files]]
