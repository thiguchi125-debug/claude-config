---
name: routine-cleanup-2026-07
description: 2026-07-04/05のクラウドRoutine棚卸し結果（停止2本・修理1本・現役6本の一覧）
metadata: 
  node_type: memory
  type: project
  originSessionId: ed827cf3-b41b-4305-a638-19d97fd693a5
---

2026-07-04〜05、クラウドRoutine全10本を棚卸しし、廃止Notion✅タスクDB(292cf503)への書込が残っていた腐敗Routineを処置した（[[feedback-system-closing-loops-rot]]の実例）。

## 2026-07-05 全体一掃の実行結果（草川「全部代行して」承認）
- **ローカル削除**: _trash_pending_20260702(192MB)／旧v2同期残骸(_council_mode.json・_sync_state.json・_classify.py・旧ログ・_deprecated_v2フォルダ)／memory旧2本(ohayo_token_efficiency・v25_streamline)。_extract_*.pyは保持
- **生成物移動**: slide-deck-prep/output(263MB) → `~/outputs/slide-deck-prep/`（SKILL.mdの出力先9箇所も書き換え済み）
- **バックアップ肥大対策**: sync-to-git.shに5exclude追加(99_raw/02_publications/05_resources/_index/_drive＋skills側output/)＋--delete-excluded → backup/ 1.0GB→41MB。**⚠️.git履歴802MBの縮小(filter-repo＋force push)は不可逆のため未実行・草川の明示承認待ち**。書き換え前の完全履歴は `~/Archive/claude-config-full-history-20260705.bundle`(697MB)に保全済み
- **Notion**: 📚Driveミラー＋📥取込キューDB・3年放置ページ(8ba6e67b)を🗄️旧アーカイブへMCP移動。ゴミ箱投入はNotionの「アプリで開く」設定でWeb UI操作不可→**🗄️ページ冒頭に「🗑️ゴミ箱に入れてOKリスト」チェックリスト設置済み**＝草川が次にNotionを開いたとき1分で処理可
- **drive-intake SKILL.md**: 旧取込キューDB参照2行を廃止注記化

**✅ 2026-07-05 削除完了**: 下記の停止4本＋実行済み単発2本（議運リマインド5/22・プロジェクト化判定レビュー5/8）の計6本を、Claude in Chrome経由でclaude.ai/code/routinesから完全削除（草川承認のもと代行・各削除前にtrigger IDを照合）。現在のRoutineは現役4本のみ：news-briefing v3.1／oyasumi-nightly（7/4修理済）／weekly-policy-radar／monthly-policy-radar。

**停止した2本（当初は無効化・後に上記の通り削除済）:**
1. `weekly-drive-sync-kusagawa`（trig_016r7yNKRqVubUvCJMTzVZ98）— Drive Desktop＋夜間パイプラインに吸収され二重処理。詳細は[[project_drive_sync_v2]]
2. `草川選挙進捗ウィークリーレビュー`（trig_01KfnWW7sA6xGTH3ZX251p5b）— 廃止Notion✅タスクDBの★選挙プロジェクト前提で、毎週金曜に廃止DBへタスクを書き込み続けていた。選挙カウントダウンはohayo§7が毎朝表示するため役割消滅。Todoist🗳選挙2026ベースの週次レビューが欲しくなったら新規Routineとして作り直す

**修理した1本:**
3. `oyasumi-nightly-kusagawa`（trig_01TbZU1pJDecnG4QmZKosz72・毎晩22:00 JST）— フォールバック手順が廃止✅タスクDBへの繰越・タスクcreateを毎晩実行していた。プロンプトを全面書き換え：タスクは**Todoist MCP読み取り専用**（find-tasks系・書込全面禁止）・繰越は翌朝morning承認方式・Todoistコネクタ接続済。td.pyはローカル専用でクラウド不可の旨も明記

**追加停止2本（2026-07-05）:**
4. `policy-update-weekly`（trig_01TfKn6JL5o6JjTLdLaT8Zin）・5. `policy-update-monthly`（trig_01KazqqjgMaw1H7w1rsjgfTq）— policy-radar（2026-05-21にpolicy-update統合済）の後継Routine（weekly/monthly-policy-radar）と並走し、毎週日曜・毎月1日に🎯政策候補DBへ候補を二重生成していた。旧世代側を停止。

**現役で健全な4本:** news-briefing v3.1（毎朝6時）／oyasumi-nightly（修理済・毎晩22時）／weekly-policy-radar（日曜）／monthly-policy-radar（月1）
