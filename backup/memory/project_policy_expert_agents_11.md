---
name: 政策エキスパート11エージェント新設
description: 2026-05-03、3本柱蒸留に先立って政策構築のための専門エージェント11本を一括新設。ドメイン6本・パッケージング1本・実現性2本・対外戦略2本のチーム編成
type: project
originSessionId: 3d6ddbd4-d2bf-409b-bad9-0583dd457c4c
---
2026-05-03 新設。草川3本柱（公約パッケージ）の蒸留に先立ち、政策構築専門のエージェントチームを11本一括整備。既存政策系（policy-archive-miner / policy-compass-curator / policy-synthesizer / policy-validator / policy-researcher / kameyama-researcher / agenda-analyzer）と非重複。

## 11本の構成

### A. 政策ドメインエキスパート（6本・専門深掘り）
1. **policy-expert-childcare-education** (pink) — 子育て・保育・幼児教育・学校教育・不登校・特別支援・いじめ・児童虐待・こども政策
2. **policy-expert-healthcare-welfare** (blue) — 医療・福祉・介護・障害・健康・地域包括ケア・母子保健・産後ケア・口腔ケア
3. **policy-expert-disaster-safety** (orange) — 防災・減災・通学路安全・要配慮者避難・ため池・太陽光適正導入・南海トラフ
4. **policy-expert-urbanplanning-industry** (green) — まちづくり・産業誘致・観光・リニア・コストコ・AIサーバー・DMO・日本遺産
5. **policy-expert-transport-infrastructure** (cyan) — 公共交通・関西本線電化・草津線・上下水道・橋梁・空き家・住宅
6. **policy-expert-digitaltransformation** (purple) — 行政DX・行かない窓口・生成AI業務導入・デジタル民主主義・Civictech

### B. 政策パッケージング（1本）
7. **policy-packaging-strategist** (red) — 散在政策候補→3本柱／公約パッケージへ束ねる戦略専門。triadic structure / narrative arc / oppositional framing / voter segment / voice-dna整合

### C. 実現性検証（2本）
8. **policy-fiscal-simulator** (yellow) — 自治体財政分析、特財・一般財源・基金・起債の試算、国庫補助金・県補助金探索、ROI・費用対効果
9. **policy-roadmap-designer** (teal) — 議会タイミング（3/6/9/12月定例会）・予算編成サイクル・4年任期内フェーズ設計・補助金申請サイクル

### D. 対外戦略（2本）
10. **policy-stakeholder-mapper** (brown) — 関係者洗い出し・賛否予測・折衝シナリオ設計・縦割り突破経路・既得権益との接点
11. **policy-comparison-benchmarker** (gray) — 類似自治体比較（いなべ・名張・桑名・木津川・御殿場等）の横並び8軸分析

## 各エージェントのファイル位置
全て `~/.claude/agents/policy-expert-*.md` / `~/.claude/agents/policy-{packaging|fiscal|roadmap|stakeholder|comparison}-*.md`

## 既存政策エコシステムとの位置関係

```
[一次調査層]
- policy-archive-miner (草川過去発言)
- kameyama-researcher (亀山現状)
- policy-researcher (国政・県政・他自治体・広く浅く)

[専門深掘り層 NEW]
- policy-expert-* (6本) ── ドメイン特化
- policy-comparison-benchmarker ── 類似自治体限定深掘り

[統合層]
- policy-synthesizer (個別政策候補)
- policy-packaging-strategist NEW (3本柱・公約パッケージ)

[検証層]
- policy-validator (EBPM 8軸)
- policy-fiscal-simulator NEW (財政専門)
- policy-roadmap-designer NEW (時間軸専門)
- policy-stakeholder-mapper NEW (関係者専門)

[コンパス基準]
- policy-compass-curator (3軸 voice-dna 原則)

[出口]
- council-material-creator (議会質問原稿)
- agenda-analyzer (議案カルテ)
- print-designer / design-director (印刷物)
- blog-writer / sns-content-creator (発信物)
```

## 使い分けルール

### 3本柱を作るとき
1. policy-archive-miner ＋ kameyama-researcher ＋ policy-researcher で素材収集
2. **policy-expert-*** （該当ドメイン）で深掘り
3. **policy-comparison-benchmarker** で横並びデータ
4. policy-synthesizer で個別候補化
5. **policy-fiscal-simulator** で予算試算
6. **policy-roadmap-designer** で時間軸設計
7. **policy-stakeholder-mapper** で関係者・折衝設計
8. policy-validator で EBPM 検証
9. **policy-packaging-strategist** で3本柱に束ねる
10. policy-compass-curator で3軸整合チェック

### 議会一般質問1本作るとき
1. policy-archive-miner で過去発言整合
2. policy-expert-* で論点深掘り
3. policy-comparison-benchmarker で「○○% vs ○○%」データ
4. policy-fiscal-simulator で財源弾を装填
5. policy-stakeholder-mapper で答弁逃げ予測
6. council-material-creator で原稿化
7. counter-argument-simulator で議場戦闘準備

## 設計の思想
- **重複回避**：既存7エージェントと役割明確化、各ファイル冒頭に「役割の境界」表
- **政策コンパス v2 整合**：全エージェントが Origin Story「声を、チカラに／私は、あなたの応援団」と3軸（伝える／繋ぐ／希望）に整合
- **EBPM 必須**：全エージェントの判断原則に「データ・他自治体比較なき提案はしない」
- **声の小さい人を優先**：政策コンパス v2 譲れない原則 #4「声の大きさで扱いを変えない」を反映
- **草川 voice-dna 整合**：「届かない」を、終わらせる／繋ぐ思いを、形にする／亀山の名を、刻む を結びに

## 次のステップ
1. 11エージェントを実運用にかける（3本柱蒸留タスク #6〜#8 で初使用）
2. Notion「エージェントトリガー一覧」DBに11本追記（既存18本→29本）
3. 運用後の改善点を半年後に refresh

## 関連メモ
- project_policy_compass.md — v2 政策コンパス
- project_policy_update_system.md — /policy-update スキル
- project_policy_archive_miner.md — 過去発言抽出
- project_policy_validator.md — EBPM 検証
- project_council_combat_agents.md — agenda-analyzer / counter-argument-simulator / video-content-strategist
