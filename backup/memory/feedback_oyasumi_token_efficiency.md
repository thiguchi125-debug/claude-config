---
name: oyasumi トークン効率化方針
description: oyasumiスキルもohayoと同様100K+消費。Drive pageSize 25→10 / read_file_content 3000→1500字 / Notion DB pageSize 30上限で対処。SKILL.md冒頭に「⚡トークン効率化原則」追加済み
type: feedback
originSessionId: 7e6bdb45-44e5-4890-b3d1-7774a1bce51d
---
oyasumi は1回100K+消費しがち。2026-05-07 草川「燃費改善してから」指示で以下を SKILL.md に反映済み。ohayo と対称運用で日次合計200K+を抑える。

**ルール:**
- Drive `list_recent_files` は `pageSize: 10`（旧25）
- Drive `read_file_content` は先頭1500字打切り（旧3000字）
- Notion DB 取得は常に `pageSize: 30` 上限。view_url 経由で時系列降順
- Step 6 デイリーサマリ 2,500字以内厳守、0件セクションは見出しごと省略
- Step 8 朝ダッシュボード `update_content` の `old_str` は見出し1行＋直下数行に絞る
- Gmail 取得は ohayo との共有前提（同一セッション内 24h 以内なら再利用可）

**Why:** 2026-05-06 ohayo 燃費改善方針 (feedback_ohayo_token_efficiency.md) と対称運用。夜100K+×朝100K+で日次200K+は持続不可能。

**How to apply:**
- oyasumi 起動時、SKILL.md冒頭の「⚡ トークン効率化原則」を遵守
- 次回 ohayo/oyasumi 前に「軽量view 4個（タスク=未完了∧期限≤明日／ニュース=今日／SNS投稿=今日完了系／市民意見=今日 OR 未対応）」を `notion-create-view` で作成し view_url を SKILL.md に恒久反映するのが next step
