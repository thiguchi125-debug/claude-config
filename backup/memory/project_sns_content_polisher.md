---
name: sns-content-polisherエージェント新設
description: 2026-05-01新設。SNS原稿の品質昇格専任。8軸診断＋AI-fingerprint排除＋surgical rewriteで「無難に良い」を「読まずにいられない」レベルへ
type: project
originSessionId: ac8f63d8-7555-414e-a1ff-91a24ac99d7e
---
2026-05-01新設。`~/.claude/agents/sns-content-polisher.md`。

## 経緯
sns-content-creatorが生成したSNS投稿7媒体（木育祭防災一輪車レース／2026-05-01テスト）が「クオリティ低い」と判断された。AI-fingerprint（——多用、3点並列、詩的体言止め、抽象賛美、テンプレCTA）が残存し、本人らしさが希薄。

## 役割
- content-editor＝合否判定→差し戻し（ゲート役）
- sns-content-polisher＝**直接書き換え→昇格出荷**（エレベーター役）
- 元原稿を温存しないリビルド前提

## 8軸診断
1. 掴み力 / 2. 本人らしさ / 3. 具体性 / 4. 情緒 / 5. PFネイティブ感 / 6. AI臭排除 / 7. 行動喚起 / 8. ローカル定着

## AI-fingerprint 即削除リスト
- 「——」2個以上、3点並列、詩的体言止め、抽象賛美「素敵」「貴重」、テンプレCTA「話し合ってみては」、絵文字機械配置、「皆様」連呼

## トリガー
「SNS品質改善」「もっと刺さる投稿に」「AI臭をなくして」「SNS投稿が低クオリティ」「もっと草川らしく書き直して」「SNS文を磨いて」「sns-content-polisher」「投稿文がイマイチ」「バズらせて」「エンゲージメント高くして」

## 連携
- sns-content-creator/ai-interview-sns-poster の出力を昇格
- voice-dna.md 必須参照
- 保存はnotion-saver

## 次にやるべきこと（要検討）
- エージェントトリガー一覧Notion(34ecf503...818a)に追加登録
- claude-configリポへバックアップ
- 既存ai-interview-sns-poster/sns-content-creatorのプロンプトに「生成後にsns-content-polisherを通す」運用を入れるか検討
