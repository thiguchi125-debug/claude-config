---
name: ai-interview-sns-posterエージェント新設
description: 2026-04-30新設。AIインタビュー(depth interview)要約をInstagram/X/Facebook向けの情熱型政策提案SNS投稿に変換する専用エージェント。同時に📋市民意見受付BOXへ自動登録
type: project
originSessionId: 92294fb5-0fe8-4273-a419-0917a8786207
---
# ai-interview-sns-poster エージェント

**新設日**: 2026-04-30
**保存先**: `~/.claude/agents/ai-interview-sns-poster.md`
**model**: opus / **color**: orange

## 役割
草川たくやのAIインタビュープロジェクト（https://depth-interview-kusagawa.vercel.app/）で集めた市民の声要約を、コピペ即投稿可能な情熱型SNS投稿（Instagram/X/Facebook）に変換する。

**Why**: AIインタビュー回答は「市民の生の声＋具体提案＋課題」がリッチに揃う宝の山だが、それをそのまま政策提案型SNS投稿に翻訳する専用フォーマットが必要だった。sns-content-creator（7媒体一括）とは別物として独立。

**How to apply**:
- AIインタビュー要約が手元にあるとき → 本エージェント起動
- 7媒体一括が必要なら従来通り sns-content-creator
- 重複起動はしない（用途で切り分け）

## 固定フォーマット
5ブロック構成（区切り線4本）:
1. 市民の声引用（属性付き、生のセリフ）
2. 政策提案（キャッチー命名）
3. 先進事例（事例DB or WebSearch、URL付き）
4. 亀山ローカル化（独自政策名）
5. AIインタビュー誘導（参加URL＋安野貴博氏／有賀啓介氏クレジット）

## 事例データベース
- **事例A: 香川県東かがわ市**（農家直接協定・分散備蓄）— 国交省PDF
- **事例B: 埼玉県宮代町**（民間委託・流通備蓄）— 公式サイト
- 範囲外は WebSearch fallback（公式サイト・省庁資料・新聞報道優先）

## レイアウト鉄則
- 段落間に空白行必須（壁ブロック禁止）
- 区切り線 `━━━━━━━━━━━━━━` を4本
- 絵文字（🐢💡🌾🔥✅⚠️🎤🏃‍♂️💨🤖✨）で視覚メリハリ
- 文末は「〜します！」「〜ですね！」言い切り
- 「できない理由」ではなく「How might we」スタンス

## 📋市民意見受付BOX 自動登録（Step 5）
SNS投稿生成と**同時実行**。エージェント間自動チェーンは存在しないため、本エージェント自身が `mcp__claude_ai_Notion__notion-create-pages` を直接呼ぶ。

- **data_source_id**: `354432ec-6c3a-4a71-b649-ce53c6b74427`
- **経路**: `その他`（AIインタビュー固有経路）
- **氏名**: 「AIインタビュー回答者（〇代・職業）」属性のみ（個人特定情報禁止）
- **連絡先**: 空（匿名前提）
- **次アクション**: SNS投稿の行動宣言と整合
- 受付ID をユーザーに1行で報告

## トリガーワード
- 「AIインタビューの要約をSNS化」
- 「depth interviewの結果を投稿に」
- 「AIインタビュー回答をInstagram/X/Facebook投稿に」
- 「ai-interview-sns-poster」

## クレジット必須
- 安野貴博氏（参院議員/AIエンジニア）depth interview ベース
- 有賀啓介氏（コンサルタント）支援
- 個人情報禁止注意書き
- 参加URL: `https://depth-interview-kusagawa.vercel.app/interview/kameyama_sougoukeikaku_bousai`

## Notion連携済み
- エージェントトリガー一覧（id:34ecf503...818a）コンテンツ生成系セクションに追記済み
- カスタムエージェント総数: 22本 → 23本
