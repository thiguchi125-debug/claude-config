---
name: short-video-virality-architectエージェント新設
description: 2026-05-01新設。≤60秒ショート動画のバイラル設計専任。フック15分類＋retention engineering＋政治家ショート成功事例＋公選法ガード。Solo（スクラッチ）/ Polish（昇格）2モード。video-content-strategistとの差別化はretention科学への深掘り。8軸自己診断64点未満は再リビルド
type: project
originSessionId: f42f962f-311d-4042-9ba8-7db4e5594d95
---
# 概要

2026-05-01に新設した、≤60秒ショート動画特化のバイラル設計エージェント `short-video-virality-architect`。世界中のバズ政治家ショート動画を研究した知識ベースを内蔵し、TikTok/YouTube Shorts/Instagram Reelsのアルゴリズム最適化を行う。

## Why
2026-05-01に作成した「亀山版デジタル地域通貨」60秒台本の品質確認後、草川から「もっとバズりやすい視聴数があがるスキップされにくいショート動画原稿を作れるエージェント」要望。既存video-content-strategistはYouTube長尺〜Shortsまで包括的だが、≤60秒のretention科学が浅い。専用エージェントで深掘りする方針。

## How to apply

### ファイル構成
- **エージェント本体**: `~/.claude/agents/short-video-virality-architect.md`（model: opus, color: orange）
- **知識ベース3点**: `~/.claude/agents/knowledge/short_video_virality/`
  - `playbook.md`: フック15分類＋retention engineering＋プラットフォーム別アルゴリズム信号＋8軸自己診断
  - `case_studies.md`: 政治家ショート成功事例（Zelensky/AOC/Buttigieg/石丸伸二/安野貴博/米山隆一/玉木雄一郎/高市早苗）
  - `anti_patterns.md`: 失敗パターン＋公選法ガード＋AI生成検出マーカー

### 起動モード
| モード | 用途 | トリガー例 |
|---|---|---|
| Solo | スクラッチ生成 | 「〇〇でバズる動画作って」 |
| Polish | 既存原稿の昇格 | 「この動画原稿磨いて」「もっとバズらせて」 |

### ワークフロー（8ステップ）
1. 入力解析（mode判定／元素材WebFetch）
2. 並列リサーチ（kameyama-researcher＋WebSearch）
3. Voice-DNA＋政策コンパス読込
4. フック5〜8案生成（15分類から混合）
5. 3バリアント構築（A:フック最強／B:情緒／C:議論誘発）
6. 自己診断8軸スコアリング（64点未満は再リビルド）
7. 安全ゲート2連（content-fact-checker → content-risk-reviewer）
8. Notion📣SNS投稿管理DB保存（タイトル先頭🎬【ショート動画｜バイラル設計】）

### 既存エージェントとの棲み分け
- **short-video-virality-architect**: ≤60秒・retention科学深掘り
- **video-content-strategist**: YouTube長尺・包括戦略・サムネ・SEO・議会切り抜き

video-content-strategist出力を引き継いでpolishする連携可能（メモに「polished from: <元URL>」明記）。

### 8軸自己診断
1. 掴み力 / 2. 本人らしさ / 3. 具体性 / 4. 情緒 / 5. 媒体感 / 6. AI臭 / 7. 行動喚起 / 8. ローカル定着
- 各1〜10点、合計64点未満は再リビルド

### 公選法ガード（必須）
- 投票依頼禁止／選挙日言及禁止／寄附匂わせ禁止
- 名指し批判禁止（組織抽象まで）
- 「絶対」「必ず」「100%」過剰約束NG

## 検証テスト想定
- Polishモード: 2026-05-01「🎬亀山版デジタル地域通貨」原稿（Notion: 353cf503-a68f-817a-99f8-f976a29c6dea）の昇格
- Soloモード: 通学路安全テーマでスクラッチ生成
- 棲み分け: 「YouTube長尺台本」→video-content-strategist／「30秒ショート」→short-video-virality-architect
