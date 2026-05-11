---
name: Notion会議ページ→Googleカレンダー登録時は元ページ削除まで自走
description: 草川がNotionのミーティングページURLを貼って「スケジュールに入れて」と言ったとき、Googleカレンダーに登録した上で、不要なNotionページの削除（または削除依頼の明示）まで一手で完了させる
type: feedback
originSessionId: efd3ba2e-af96-4113-a72a-520218417b20
---
草川がNotionの`<meeting-notes>`タグ付きページURLを貼って「スケジュール／予定に入れて」と言ったときは、以下を**指示なしで**自走する：

1. **登録先はGoogle Calendar**（kusakawa.taku@gmail.com）。Notionの会議ページに留め置かない。
2. **元のNotionページは不要**として扱う：
   - Notion MCPは`archive=true`相当の削除APIを公開していない（`notion-update-page`にarchiveフラグなし、`notion-move-pages`は他親への移動のみ）
   - 自動削除できないので、登録報告と同時に「Notionページは手動でゴミ箱へ送ってください」と明示する
   - もし将来MCPに削除APIが追加されたら自走する
3. **使用カレンダーアカウントを必ず明示**して報告する（kusakawa.taku@gmail.com）。

**Why:** 2026-05-06、Notionの「松尾英子さんへお礼訪問」会議ページURLで「スケジュール入れて」と言われた際、Googleカレンダーへの登録は完了したが、Notionの元ページを残したまま報告 → 草川から「ミーティングではない、カレンダーに追加という意味。Notionページは不要なので削除、指示しなくてもこれくらいは判断して」と修正指示。会議ページ＝Notion会議録目的ではなく単なるリマインダー用途のことがある。

**How to apply:** Notion会議ページURL＋「スケジュール／予定／カレンダー」系トリガー時、(1) Google Calendar登録 (2) アカウント明示 (3) Notion元ページの削除（不可なら手動依頼）まで1パスで完了。「とりあえず登録だけ」で止めない。
