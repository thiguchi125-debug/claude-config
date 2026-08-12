---
name: reference-todoist-gcal-sync-allday
description: Googleカレンダーの終日枠を埋め尽くしているのはTodoist同期カレンダー。期限付きタスクが全部終日イベント化する
metadata: 
  node_type: memory
  type: reference
  originSessionId: 9eee0977-c8ac-42d8-928d-0f6d110c74f3
  modified: 2026-08-12T01:01:57.666Z
---

草川のGoogleカレンダーには `92341b5ccf5d41a33ec7c5975be99843d2c6c2e490857bccdb6f7a6c70a20009@group.calendar.google.com`（表示名「Todoist」）が登録されており、**Todoistの時刻なし期限（日付だけ）のタスクを全部「終日イベント」として書き出す**。CLAUDE.mdのルールでタスクは全部Todoistに一本化＋期限は日付のみなので、期限付きタスクの件数がそのまま終日枠の件数になる（2026-08-12時点でアクティブ183件・期限付き163件）。完了済みタスクも `✓` 付きで残る。

「終日枠が埋まっている」と言われたときの第一手は、この同期カレンダーの存在を疑うこと。`list_calendars` で確認できる。表示を消すだけならGoogleカレンダー左サイドバーの「Todoist」のチェックを外す（同期も履歴も壊れず、ワンクリックで戻せる）。恒久停止はTodoist側の設定→連携→Googleカレンダーで、草川本人のログイン操作が必要。

**「時間の正本」は `【作業】` ブロックの側**であって終日枠ではない。終日枠はTodoistの生の期限一覧が二重に見えているだけなので、[[project_task_window_labels]] の束ね枠へタスクを割り付けたうえで、この層は非表示にするのが正しい状態。枠と期限のズレは毎朝ohayoの「🗓 枠×期限の突合」が検出する。
