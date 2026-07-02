---
name: reference_storage_map
description: ファイル管理システムv4の保存先マップ正本。用途→正規置き場の対応表・パイプライン監視・トラブル時の確認手順
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2237a7c2-1e97-4b26-8ecc-ad5b1b3e3b53
---

# ファイル管理システム v4 保存先マップ（2026-07-02確立）

CLAUDE.mdの「📂保存先マップ」の詳細版。散乱の3根本原因（①夜間パイプラインのTCCサイレント故障 ②ローカル→Drive導線未整備 ③iCloud圧迫）をv4で解消した後の正規運用。

## 保存先の全体構造

**Drive（一次資料・成果物の正本）** — `マイドライブ/草川たくや 議会質問アーカイブ/`
- `_INBOX_council/`・`_INBOX_daily/` — 投函口。iPhone/Macから放り込むだけ
- `議会資料アーカイブ/R0X (20XX)/{03,06,09,12}_定例会/種別/`＋`委員会・全協（会期外）/`
- `日常資料アーカイブ/00_名簿・個人情報/` — **PII保護区画（2026-07-02新設・_build_indexのgrepキャッシュ対象外）**
- `日常資料アーカイブ/01_政策素材/〜05_視察・外部交流/`＋`06_フォーム・アンケート運用/<案件名>/`（2026-07-02新設・gform/gsheet/gscript置き場）＋`99_その他/`
- `ZZ_一般質問制作/`・`ZZ_議案質疑制作/`（R0X/YYYY-MM_◯月議会/01_通告書〜04_完成品）・`ZZ_市政報告レポート/`・`ZZ_選挙関連/`
- `📱動画素材/`（Driveルート直下・編集済み動画とスマホ編集用PNG）
- **Drive直下への野良ファイル禁止**（2026-07-02に27件一掃済み）

**ローカル**
- `~/.claude/projects/-Users-kusakawatakuya/drafts/` — AI下書き（ブログD1保管等）
- `~/outputs/` — スキル生成物の唯一の出力先（daily-content/short-video/図解。**絶対パスで指定・cwd依存禁止**。旧 projects/outputs は2026-07-02統合済み）
- `~/publications/<YYYY-MM_案件名>/` — 署名活動等のプロジェクト
- `~/Archive/` — **iCloud外の長期保管庫（2026-07-02新設）**: 資料倉庫_2026以前(14GB・旧Documents/_archived_to_claude)／団体活動アーカイブ(JC・三重大応援団)／録音／GoogleTakeout／Downloads_old_30d／`_sweep/`(週次自動退避先)／`_trash_pending_<日付>/`(削除承認待ち)／`_要確認_<日付>/`(判定不能ファイル)／`_relocation_log_*.csv`(全移動記録・ロールバック用)
- `~/Documents` — ほぼ空運用（ObsidianVault・kameyama-researchのみ。iCloud同期対象のため大容量禁止）
- `~/Desktop`・`~/Downloads` — 一時作業場。恒久保管禁止。30日超は日曜夜スイープで`~/Archive/_sweep/YYYY-MM/`へ自動退避

## 自動化（夜間パイプライン v4）

- launchd `com.kusagawa.daily-drive-pipeline` 毎晩2:30 — ランナーは `~/.local/bin/kusagawa-pipeline-bash`（bashコピー＋ad-hoc署名 `codesign -s - --identifier com.kusagawa.pipeline-bash`。/bin/bash直起動だとCloudStorageが空に見える＝2026-05〜06のサイレント故障の原因。2026-07-02のE2Eテストで振分け動作確認済み。**将来visibility_errorが出たら**システム設定→フルディスクアクセスにこのバイナリを追加）
- Phase1 `_auto_intake.sh`(v4): INBOX振分＋可視性チェック（空に見えたらVISIBILITY_ERROR）＋council判定不能はmtimeから`📥要確認_YYYY-MM/`へ＋ファイル名に「個人情報/名簿/連絡先」→00_名簿・個人情報へ自動隔離＋結果を`_pipeline_status.json`へ
- Phase2 `_build_index.sh`: pdftotext→`_index/`（00_名簿・個人情報は除外）
- Phase3 `_local_sweep.sh`: 日曜のみDesktop/Downloadsの30日超を退避
- **監視**: ohayo v2.7が毎朝 `_pipeline_status.json` を読んで1行表示。🚨visibility_error→FDA確認、🚨48h以上未実行→launchctl確認

## トラブル時

- パイプラインが動かない: `launchctl print gui/501/com.kusagawa.daily-drive-pipeline`、手動実行は `launchctl kickstart gui/501/com.kusagawa.daily-drive-pipeline`
- visibility_error: システム設定→プライバシーとセキュリティ→フルディスクアクセス→`kusagawa-pipeline-bash` がONか確認
- 移動したファイルが見つからない: `~/Archive/_relocation_log_*.csv` をgrep（元パス→新パスの全記録）

関連: [[feedback_system_closing_loops_rot]] / [[feedback_publications_binary_storage]] / [[reference_ippan_shitsumon_seisaku_drive]]
