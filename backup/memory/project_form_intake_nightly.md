---
name: project_form_intake_nightly
description: ご意見箱Googleフォーム3シートの夜間自動取込システム（form-intakeスキル＋launchd 3:30）。旧ohayo§9朝ポーリングの夜間前倒し。2026-07-25構築。
metadata: 
  node_type: memory
  type: project
  originSessionId: 127e63c0-a431-4d43-83f1-008de904dd92
  modified: 2026-08-15T23:13:10.811Z
---

2026-07-25構築。ご意見箱フォーム回答シート3枚の新着を毎晩3:30に自動取込（launchd `com.kusagawa.form-intake` → `~/.claude/scripts/form-intake/form_intake.sh` → claude -p → **form-intakeスキル**が正本手順）。手動フォールバック=「フォーム取り込んで」。

- フロー: 新着検出→ikenスキル準拠解析→📝市民意見リスト(c2c34bd8-)登録→`_citizen_voice/`ドメイン別ファイルにマスク追記→`_form_status.json`→翌朝ohayo§9が表示。返信案・タスク化は夜間やらない（朝「◯番の返信案作って」でikenへ）。
- **重要経緯**: ohayo§9が2026-05-11から既に毎朝同シートをポーリングしていた（[[project_form_intake_db]]のGAS断念→手動コピペ運用の後に追加されていた）。本システムはその夜間前倒しで、state=`iken_poller_state.json`を共用（`last_processed_timestamp`=Notion登録済み／`etl_last_row`=ETL追記済み行数の2トラック）。ohayo§9はシート直接ポーリング廃止・結果表示＋死活監視のみに書換済み。
- **落とし穴**: Drive `read_file_content`は古いキャッシュを返す→`download_file_content`＋base64デコード必須。headlessはToolSearch必須（[[feedback_headless_mcp_deferred_false_absent]]）。
- **2026-08-15/16 連夜停止＝claude.aiコネクタのOAuth期限切れ**。8/15はCLI自体が `Failed to authenticate: OAuth session expired and could not be refreshed`（2回試行とも）、8/16はCLIは起動したが `mcp__claude_ai_*` がToolSearchで0件（deferredはplugin:discordのみ／`~/.claude/daemon-auth-status.json` = `auth_required`）。**草川手番＝`claude` 起動して `/mcp` から再認証 → 「フォーム取り込んで」で手動再走**。stateは両夜とも未更新なので取りこぼしゼロ（再開点 S1=49行/S2=213行/S3=148行）。「MCPが無い」判定はToolSearchを複数クエリ試してから（[[feedback_headless_mcp_deferred_false_absent]]）。
- 設計書: `~/claude-config/specs/2026-07-25-form-intake-design.md`
- **初回キャッチアップ**: ETL側は2026-07-25完了（バックログ44件追記・359→403件。S3はETL漏れ22件=2025/03〜2026/04も回収）。**残=Notion登録6件のみ**（Notion MCP認証切れで停止中→草川が/mcpで再認証→「フォーム取り込んで」。Todoist登録済み・E2Eテストで検出/フィルタ/state保守処理は動作確認済）。新着6件の対応タスクはTodoist登録済（図書館聞き取り事案=緊急ほか計6本）。
- ohayo§9はタスク化候補同時提示（承認制）も実装済（表示だけでは声が落ちる穴の締め・2026-07-25）。

**Why:** 手動コピペの投函負担をゼロにし、報告会の声と同様「届いた声が行方不明になる」事故を構造的に防ぐ（[[feedback_system_closing_loops_rot]]=締め工程は定時トリガーに載せる）。

**How to apply:** フォーム意見の取込状況を聞かれたら「毎晩3:30自動・朝ohayoで表示・手動は『フォーム取り込んで』」。二重登録の心配はstate共用＋重複ガードで対処済み。
