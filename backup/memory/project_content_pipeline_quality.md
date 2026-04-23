---
name: コンテンツパイプライン品質改善（2026-04-22）
description: blog-writer/sns-content-creator の原稿品質を上げるため、voice-dna.md＋content-editor品質ゲートを導入した構成
type: project
originSessionId: 4106fbb9-d1d3-4a51-82e0-d79536592b47
---
2026-04-22 にコンテンツパイプラインを大幅改修。SNS原稿・ブログ記事の品質低下を受けて、エージェントの刷新＋品質ゲート追加＋声のDNA抽出を実施。

**Why:** 旧構成では blog-writer / sns-content-creator の指示が抽象的で、research結果が原稿に反映されず、媒体ごとの切り口も差別化されておらず、レビュー工程もなかったため、一般論だけの政治家ぽい原稿になりがちだった。

## 構成の変更点

### 新規ファイル
- `~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/content-pipeline/references/voice-dna.md` — 草川たくやの声の指紋（常用フレーズ・NG表現・文体癖・CTAレパートリー・媒体別定型）
- `~/.claude/plugins/cache/.../content-pipeline/agents/kusakawa-voice-analyst.md` — voice-dna を更新する1回起動型エージェント
- `~/.claude/agents/content-editor.md` — 原稿を5軸でスコアリングする品質ゲート

### 書き直したファイル
- `~/.claude/plugins/cache/.../content-pipeline/agents/blog-writer.md` — 5段構成固定・ファクト最低基準・NG表現リスト・voice-dna参照を組み込んだ版
- `~/.claude/agents/sns-content-creator.md` — 7媒体の切り口差別化・LINE公式アカウント対応・research_summary活用を明記した版

### パイプライン配線
- Step 2（blog生成）→ **Step 2.5（content-editor レビュー）** → Step 3
- Step 3（SNS生成）→ **Step 3.5（content-editor レビュー）** → Step 5
- 不合格時は revision_requests を writer に返して最大2周の再生成。2周してもrevise判定なら `human_review_flag: true` で保存（⚠️プレフィクス付与）

## How to apply
- 原稿品質が低いと指摘された場合、まず voice-dna.md が最新か（サンプル数・更新履歴）を確認。Notion 公開済み投稿が50件増えたら kusakawa-voice-analyst を再実行
- content-editor の5軸: ①ファクト密度 ②亀山市接続性 ③声の一貫性 ④媒体適合度 ⑤読者エンゲージ（各5点・合計25点・18点未満はrevise）
- 即ペナルティ条件: NG定型句使用／他者批判／ハッシュタグ6+／ハルシネーション／定型フッター/挨拶の欠落
- LINEの定型: `こんばんは、草川たくやです。` で開始し `いつも応援ありがとうございます😊` で終わる（ブロードキャスト前提なので `[お名前]さん` は不可）
- Facebookの定型開始: `市民の皆さん、こんにちは。亀山市議会議員の草川たくやです。`
- ブログタイトル構文: `【草川たくや 亀山市】[問い]——[補足]` or `「[生のセリフ]」——[論点]、[副題]` のいずれか
- voice-dna.md の指紋（——／セリフ引用／📌見出し／議会宣言締め／具体数値太字）を外すと content-editor がrevise判定を出す

## 関連ファイル一覧
- voice-dna.md ... 声の指紋
- agents/blog-writer.md ... ブログ生成
- agents/kusakawa-voice-analyst.md ... voice-dna更新
- agents/notion-saver.md ... 保存（既存・未改修）
- agents/kameyama-researcher.md ... 亀山市調査（既存）
- ~/.claude/agents/policy-researcher.md ... 国・他自治体調査（既存）
- ~/.claude/agents/sns-content-creator.md ... SNS生成
- ~/.claude/agents/content-editor.md ... 品質ゲート
- ~/.claude/agents/council-material-creator.md ... 一般質問原稿（既存）
