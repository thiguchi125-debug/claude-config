---
name: feedback-no-dedicated-blog-db-in-notion
description: Notionに「📝ブログDB」は存在しない。ブログは📣投稿管理DB（SNS＋ブログ統合）にプラットフォーム＝ブログで入れる
metadata:
  type: feedback
---

**Notionにブログ専用DBは無い。**旧ブログ記事管理DB（`dcdf44af-`）は2026-05-03に廃止・統合済みで、ブログ記事は **📣投稿管理DB（SNS＋ブログ統合）** に「プラットフォーム＝ブログ」で入れるのが正しい。

- database page: `78f40f33-ae71-4f32-9cc3-b00c0a36707c`
- data_source: `1bd98deb-624f-402c-aeb3-bdaa4782b389`
- path: 朝のダッシュボード / 📣 コンテンツ管理 / 📣 投稿管理DB（SNS＋ブログ統合）
- プロパティ＝投稿タイトル（title）／ステータス（未着手・進行中・完了）／プラットフォーム／公開URL／公開予定日／メモ

**Why:** 2026-09-11、handoffメモの「ブログ（📝ブログDB）」という表記を鵜呑みにして notion-saver に「📝ブログDBへ」と指示し、草川に「📝ブログDBなんて今まで使っていたか？」と指摘された。DB名は handoff や会話の言い回しでなく `feedback_3db_view_url_correction` 系を正本にする。

**How to apply:** ブログ保存の指示を書くときは「📣投稿管理DB（ds `1bd98deb-624f-402c-aeb3-bdaa4782b389`）にプラットフォーム＝ブログで」と明示する。

関連: [[feedback_3db_view_url_correction]] [[feedback_3db_view_url_correction_v2]] [[feedback_notion_saver_reports_unverified_success]]
