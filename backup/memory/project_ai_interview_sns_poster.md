---
name: ai-interview-sns-posterエージェント新設
description: 2026-04-30新設(同日Step 6追加)。AIインタビュー(depth interview)要約をInstagram/X/Facebook向け情熱型政策提案SNSに変換。📋市民意見受付BOX＋📣SNS投稿管理DB両DBへ自動登録
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

## 📣SNS投稿管理DB 自動登録（Step 6, 2026-04-30追加）
SNS投稿原稿そのものを📣SNS投稿管理DBへも残し、投稿履歴・ステータス追跡を有効化する。Step 5（市民の声記録）とは別レコード。

- **data_source_id**: `1bd98deb-624f-402c-aeb3-bdaa4782b389`
- **投稿タイトル**: 「【AIインタビュー】〇〇テーマ」
- **ステータス**: `未着手`（生成直後・未投稿）→ 投稿実施後に手動で `完了` 更新
- **プラットフォーム**: 指定の multi_select（既定: Instagram/X/Facebook 3つ）
- **ネタ元**: `市民相談`（AIインタビュー＝市民の声起点として固定）
- **分野**: テーマ別 select 1つ
- **投稿予定日**: 当日
- **メモ**: AIインタビュー由来＋提案者属性＋📋意見BOX受付IDリンク
- **content**: 投稿原稿全文（区切り線・空白行・絵文字保持）

**Why**: 旧設計はSNS投稿原稿がコピペで終了し、Notion上に投稿履歴が残らなかった。content-pipeline生成の通常SNSは📣DB保存される一方、AIインタビュー経由のSNSだけが闇に消える整合性ギャップを解消。

**注意**: `feedback_blog_sns_db_status_options.md` の通り📣DBステータスは未着手/進行中/完了のみで「下書き完成」相当の選択肢はない。生成直後は `未着手` で運用。

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
