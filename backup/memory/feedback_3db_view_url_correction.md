---
name: 3DB view_url再設定（2026-05-08）
description: oyasumi/ohayoが2026-04-30〜05-07に連発した「3DB 0件返却事故」の根本原因。SNS投稿管理DB／一般質問ネタDBはpage URLのみで?v=不在、市民意見受付BOXは廃止DBを指していた
type: feedback
originSessionId: 7e6bdb45-44e5-4890-b3d1-7774a1bce51d
---
oyasumi/ohayo SKILL.md記載の3DB view_urlに重大な誤りがあり、2026-04-30〜05-07の連続0件返却の原因と判明。2026-05-08確定：

**修正内容（oyasumi SKILL.md反映済み）:**
- SNS投稿管理DB: `78f40f33ae714f329cc3b00c0a36707c` → `78f40f33ae714f329cc3b00c0a36707c?v=6ac6eddd-53b7-4e54-8ebe-ec2e02227718`（page URLのみで?v=なしは validation_error）
- 一般質問ネタDB: `cb47d25e30b14b61b39f56254bf9432a` → `cb47d25e30b14b61b39f56254bf9432a?v=2d912401-3794-484a-8252-04ade354fbd2`（同上）
- 📋市民意見受付BOX `70eeaeabe7e246599e0e7d5f8fef88c6` は実は **「📦 旧受付BOX（2026-04-30〜05-02統合済・data_source 354432ec-）」の廃止DB**を指していた → 現役は `collection://c2c34bd8-1e16-492e-aab0-d3f497d18d4d`（database top page `8a36d28a0e1d4fb595a09107f663aa1e`）に変更
- 旧ブログ記事管理DB（dcdf44af-）は2026-05-03廃止統合済み（SNS投稿管理DB プラットフォーム=ブログに統合）

**Why:** 5/7 oyasumi で3DB連続失敗 → 5/8 ohayo で原因究明依頼。SKILL.md記載が page URLのみ（`?v=` なし）+ 廃止DBへの参照という二重ミス。

**How to apply:**
- 次回 oyasumi/ohayo 起動時、修正済 view_url で正常クエリされる想定
- 市民意見リストDB c2c34bd8系の defaultview URL は次回機会に notion-fetch で確定し、SKILL.md を二段階で確定させる
- view_url追加・削除時は必ず一度 notion-query-database-view で動作確認してから SKILL.md コミット
