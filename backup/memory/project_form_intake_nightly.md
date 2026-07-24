---
name: project_form_intake_nightly
description: ご意見箱Googleフォーム3シートの夜間自動取込システム（form-intakeスキル＋launchd 3:30）。旧ohayo§9朝ポーリングの夜間前倒し。2026-07-25構築。
metadata: 
  node_type: memory
  type: project
  originSessionId: 127e63c0-a431-4d43-83f1-008de904dd92
  modified: 2026-07-24T15:35:36.236Z
---

2026-07-25構築。ご意見箱フォーム回答シート3枚の新着を毎晩3:30に自動取込（launchd `com.kusagawa.form-intake` → `~/.claude/scripts/form-intake/form_intake.sh` → claude -p → **form-intakeスキル**が正本手順）。手動フォールバック=「フォーム取り込んで」。

- フロー: 新着検出→ikenスキル準拠解析→📝市民意見リスト(c2c34bd8-)登録→`_citizen_voice/`ドメイン別ファイルにマスク追記→`_form_status.json`→翌朝ohayo§9が表示。返信案・タスク化は夜間やらない（朝「◯番の返信案作って」でikenへ）。
- **重要経緯**: ohayo§9が2026-05-11から既に毎朝同シートをポーリングしていた（[[project_form_intake_db]]のGAS断念→手動コピペ運用の後に追加されていた）。本システムはその夜間前倒しで、state=`iken_poller_state.json`を共用（`last_processed_timestamp`=Notion登録済み／`etl_last_row`=ETL追記済み行数の2トラック）。ohayo§9はシート直接ポーリング廃止・結果表示＋死活監視のみに書換済み。
- **落とし穴**: Drive `read_file_content`は古いキャッシュを返す→`download_file_content`＋base64デコード必須。headlessはToolSearch必須（[[feedback_headless_mcp_deferred_false_absent]]）。
- 設計書: `~/claude-config/specs/2026-07-25-form-intake-design.md`
- **残タスク**: 初回キャッチアップ実行（etl_last_row初期値=ETL 2026-05-06時点のため、2026-05以降の未追記分＋7月新着があれば初回にまとめて処理。「フォーム取り込んで」で対話実行し草川目視確認が推奨）。

**Why:** 手動コピペの投函負担をゼロにし、報告会の声と同様「届いた声が行方不明になる」事故を構造的に防ぐ（[[feedback_system_closing_loops_rot]]=締め工程は定時トリガーに載せる）。

**How to apply:** フォーム意見の取込状況を聞かれたら「毎晩3:30自動・朝ohayoで表示・手動は『フォーム取り込んで』」。二重登録の心配はstate共用＋重複ガードで対処済み。
