---
name: feedback-task-db-pending-status
description: ✅タスクDBのステータス「Remind」を廃止し「Pending」に変更。Pendingは要検討・保留の置き場
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 80d9eae1-b8d0-49ea-a609-4979efdeb9a3
---

2026-06-08 草川が✅タスクDB（`292cf503-a68f-81c6-b9dd-000b3ffdd2ce`）のステータス選択肢「Remind」を「Pending」に変更（UIで手動・Remindはもう使わない）。

**Pending の用途**: 「要検討・保留」のタスクをここに入れていく。やる/やらないをまず決める必要があるもの、自分都合で一旦止めるもの。

**現行ステータス**: inbox / Wish List / Project / Waiting / **Pending**（旧Remind）/ Done / Archive

**Why:** 当初「要検討」カテゴリ新設を検討したが、Notion APIはstatus型の選択肢追加不可（DDL弾かれる・UI専用）。新規プロパティを作らず、使っていなかったRemindをPendingに転用して解決した。

**How to apply:**
- ohayo/oyasumi/task-audit 等でステータスを扱うとき「Remind」は存在しない前提。「Pending」を要検討・保留バケットとして扱う。
- 保留系の使い分け: **Pending**＝自分が判断保留（要検討）／**Wish List・Waiting**＝相手の連絡待ち・外部要因待ち。
- ステータスの選択肢追加が必要になっても API では不可。草川にUI手動追加を依頼する。
- 旧ビュー「🔁 Remind残存確認」は名称がRemindのまま残っている可能性あり（option renameならフィルタは生きてPendingを表示）。気になればビュー名変更を草川に促す。
- 関連: [[feedback-notion-dsl-status-filter-limitation]] [[feedback-blog-sns-db-status-options]]
