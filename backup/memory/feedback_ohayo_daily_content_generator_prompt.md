---
name: feedback-ohayo-daily-content-generator-prompt
description: ohayoとdaily-content-generatorの連結はオプションB（プロンプト型誘導）で実装。自動連結禁止、テーマ提案トリガー成立時のみ末尾に誘導プロンプト1行を出す
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e23e2241-014f-4e0b-b286-efaeb93a1f3a
---

# ohayo → daily-content-generator 連結はB（プロンプト型誘導）で実装

**Why**: 草川指示「ohayoとdaily-content-generatorの連結はオプションB（プロンプト型誘導）で実装」（2026-05-21）。理由：
1. ohayoは毎朝走る（cron化）— 自動フル展開すると300〜500Kトークン消費・既発信重複・草川承認なしでの暴走リスク
2. テーマ選定は草川の判断を経るのが本来適切（3案中どれを当日打つかは情勢次第）
3. `feedback_ohayo_token_efficiency_v3` で「目標70〜90K」と決めてあり、daily-content-generator自動起動はこれを破壊する

**How to apply**:
- ohayo SKILL.md v2.5-d ブロック参照（実装位置: `📝 今日のブログ・SNS発信おすすめテーマ` セクション直後に「💫 今日のフルパッケージ作りますか？」誘導ブロック1個）
- 発火条件: v2.5 D2のテーマ提案トリガー成立時のみ（「演説テーマ提案して」「ブログテーマ出して」「SNSテーマ案出して」「発信テーマ」等で§3-6が起動済み）
- 通常ohayo（テーマ提案未発火）では誘導プロンプトも出さない
- 草川返信パターン: 「A1でフルパッケージ」「Aとブログ深掘り1でフル」「全部作って」等の自然言語をdaily-content-generator起動指示と判定
- 返信なし＝スキップ・暴走しない
- daily-content-generator起動後も content-fact-checker → content-risk-reviewer は通過必須（CLAUDE.md §6 安全ゲート）

**追加コスト**: +0K（既出データ再利用・新規fetchゼロ・Notion本文置換ゼロ）

**A/C/D案を採用しなかった理由**:
- A（現状維持）: 草川が毎回「daily-content-generator 起動して」とフル文字打つコスト
- C（部分連結）: テーマ選定だけohayoで走る案は、結局原稿生成段階で同じ判定をやり直すため節約効果薄い
- D（曜日限定自動）: 街宣前提日(火・木)限定の自動展開案は、街宣やらない日が増えた場合の制度疲労リスクあり

将来D案に切替えたくなった場合は本v2.5-dの「発火条件」を曜日条件に置き換えるだけで対応可（拡張容易）。

関連: [[feedback_ohayo_token_efficiency_v3]] / [[feedback_ohayo_v25_streamline]] / project_short_video_create_system
