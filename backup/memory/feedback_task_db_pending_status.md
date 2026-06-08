---
name: feedback-task-db-pending-status
description: ✅タスクDBのステータス「Remind」を廃止し「Pending」に変更。Pendingは要検討・保留の置き場
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 80d9eae1-b8d0-49ea-a609-4979efdeb9a3
---

2026-06-08 草川が✅タスクDB（`292cf503-a68f-81c6-b9dd-000b3ffdd2ce`）のステータス選択肢「Remind」を「Pending」に変更（UIで手動・Remindはもう使わない）。

**現行ステータス**: inbox / Wish List / Project / Waiting / **Pending**（旧Remind）/ Done / Archive

**保留系3ステータスの定義（2026-06-08 草川確定・厳密に区別）**:
- **Pending**：やる方向だけど、実行には検討が必要（自分の判断・段取り待ち。「要検討」もここ）
- **Wish List**：やりたいけど、今こちらで追加対応できることがない（手詰まり・寝かせ）
- **Waiting**：相手の対応待ち（外部の返事・対応待ち）

**Why:** 当初「要検討」カテゴリ新設を検討したが、Notion APIはstatus型の選択肢追加不可（DDL弾かれる・UI専用）。新規プロパティを作らず、使っていなかったRemindをPendingに転用して解決した。

**How to apply:**
- ohayo/oyasumi/task-audit 等でステータスを扱うとき「Remind」は存在しない前提。「Pending」を要検討・保留バケットとして扱う。
- 保留系の使い分け（上の定義に厳密に従う）: **Pending**＝やる方向だが実行に検討要／**Wish List**＝やりたいがこちらで追加対応できることなし／**Waiting**＝相手の対応待ち。task-audit等の仕分けで混同しない。
- ステータスの選択肢追加が必要になっても API では不可。草川にUI手動追加を依頼する。
- **グループ未所属のstatus選択肢はAPI書込不可（重要）**: Pending/Waiting/Project はenumに存在してもどのグループ（to_do/in_progress/complete）にも属していないと、update_propertiesで「Value must be one of inbox/Wish List/Done/Archive」エラーになる。fetchのgroupsで該当オプションがどの配列にも無ければこれ。直し方は草川がUIで「プロパティを編集→該当オプションを"進行中(In progress)"等のグループ内へドラッグ」。グループに入れば以降API書込可。これもAPIからは直せない（UI専用）。
- 旧ビュー「🔁 Remind残存確認」は名称がRemindのまま残っている可能性あり（option renameならフィルタは生きてPendingを表示）。気になればビュー名変更を草川に促す。
- 関連: [[feedback-notion-dsl-status-filter-limitation]] [[feedback-blog-sns-db-status-options]]
