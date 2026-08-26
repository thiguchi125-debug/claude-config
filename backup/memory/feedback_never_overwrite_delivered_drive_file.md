---
name: feedback-never-overwrite-delivered-drive-file
description: 一度草川に渡したDrive同期フォルダ上の成果物を cp で上書きしない。草川がクラウド側で加えた編集が黙って消える
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a4c6b6-7f0f-49d2-ac05-764d02aae063
  modified: 2026-08-26T14:24:59.658Z
---

**一度リンクを渡した成果物を、Drive同期フォルダ上で `cp` 上書きしてはいけない。**

2026-08-26の後援会管理表で、同じファイルを18:35→22:22→23:15と3回 `cp` で差し替えた。
その間に草川がGoogleスプレッドシート側で加えた編集は、最後の上書きで消えた。
草川からの申告は「直接更新しても保存されないのなんで」で、原因の特定まで草川の時間を使わせた。

**Why:** Google Drive Desktop の同期フォルダはローカル→クラウドの一方向上書きになる。
ローカルで丸ごと差し替えると、クラウド側の編集履歴ごと新しいファイル内容に置き換わる。
「保存されない」という症状で表面化するので、草川からは原因が見えない。

**How to apply:**
- リンクを渡す**前**なら上書きしてよい。渡した**後**は原則さわらない。
- どうしても直すなら、①先に「上書きするので編集を止めてほしい」と断る か
  ②`_v2` など別名で新規作成して新リンクを渡す。黙って差し替えない。
- 作業前に `modifiedTime`（Drive）とローカル mtime を突き合わせ、
  自分の最後のコピーより新しければ草川の編集が入っている＝上書き禁止。
- 直す予定があるうちは、そもそもリンクを渡さない。完成してから1回で渡す。

関連: [[feedback_spreadsheet_deliverable_must_be_native_and_functional]]
[[feedback_open_folder_after_generating_files]] [[project_koenkai_roster_two_systems]]
