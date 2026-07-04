---
name: routine-cleanup-2026-07
description: 2026-07-04/05のクラウドRoutine棚卸し結果（停止2本・修理1本・現役6本の一覧）
metadata: 
  node_type: memory
  type: project
  originSessionId: ed827cf3-b41b-4305-a638-19d97fd693a5
---

2026-07-04〜05、クラウドRoutine全10本を棚卸しし、廃止Notion✅タスクDB(292cf503)への書込が残っていた腐敗Routineを処置した（[[feedback-system-closing-loops-rot]]の実例）。

**停止した2本（無効化のみ・削除は https://claude.ai/code/routines から草川手動）:**
1. `weekly-drive-sync-kusagawa`（trig_016r7yNKRqVubUvCJMTzVZ98）— Drive Desktop＋夜間パイプラインに吸収され二重処理。詳細は[[project_drive_sync_v2]]
2. `草川選挙進捗ウィークリーレビュー`（trig_01KfnWW7sA6xGTH3ZX251p5b）— 廃止Notion✅タスクDBの★選挙プロジェクト前提で、毎週金曜に廃止DBへタスクを書き込み続けていた。選挙カウントダウンはohayo§7が毎朝表示するため役割消滅。Todoist🗳選挙2026ベースの週次レビューが欲しくなったら新規Routineとして作り直す

**修理した1本:**
3. `oyasumi-nightly-kusagawa`（trig_01TbZU1pJDecnG4QmZKosz72・毎晩22:00 JST）— フォールバック手順が廃止✅タスクDBへの繰越・タスクcreateを毎晩実行していた。プロンプトを全面書き換え：タスクは**Todoist MCP読み取り専用**（find-tasks系・書込全面禁止）・繰越は翌朝morning承認方式・Todoistコネクタ接続済。td.pyはローカル専用でクラウド不可の旨も明記

**追加停止2本（2026-07-05）:**
4. `policy-update-weekly`（trig_01TfKn6JL5o6JjTLdLaT8Zin）・5. `policy-update-monthly`（trig_01KazqqjgMaw1H7w1rsjgfTq）— policy-radar（2026-05-21にpolicy-update統合済）の後継Routine（weekly/monthly-policy-radar）と並走し、毎週日曜・毎月1日に🎯政策候補DBへ候補を二重生成していた。旧世代側を停止。

**現役で健全な4本:** news-briefing v3.1（毎朝6時）／oyasumi-nightly（修理済・毎晩22時）／weekly-policy-radar（日曜）／monthly-policy-radar（月1）
