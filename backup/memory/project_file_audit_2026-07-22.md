---
name: project-file-audit-2026-07-22
description: 2026-07-22ファイル管理・引き継ぎ体制の全面監査結果と実施済み改善・残タスク
metadata: 
  node_type: memory
  type: project
  originSessionId: 00d1106b-200d-4ede-baa7-e258a7dadeab
  modified: 2026-07-22T05:03:09.637Z
---

# ファイル管理監査 2026-07-22（実施済み＋残タスク）

## 実施済み（同日）
- **Drive直下を4フォルダ正規形に整理**: `草川たくや 議会質問アーカイブ`／`📷写真ストック`／`📱動画素材`／`💾Macローカルミラー`（新設）のみ。野良のgform/gsheet/gscript 8件を`06_フォーム・アンケート運用/`配下へ移動（移動ログ=`~/Archive/_relocation_log_20260722.csv`）。
- **マイドライブ直下の重複「日常資料アーカイブ」を統合**: 7/14後援会フォーム構築時に誤作成されたもの。後援会名簿マスタCSV→アーカイブ内`00_名簿・個人情報/`、後援会入会フォーム正本一式・リニア杯フォーム→アーカイブ内`06_フォーム運用/`へ。フォルダ/ファイルIDは移動で不変＝GAS動作に影響なし。
- **_INBOX_daily滞留3件を振り分け**（18日間滞留していた。daily判定不能分の後処理launchdジョブは存在しない＝CLAUDE.mdの「朝7時/夜22時無人実行」記述は誤りで修正済）: サマーキャンプ参加報告書(**7/24必着**)→03_後援会・組織/青少年育成市民会議、10周年式典時程表→03、城東報告会解説台本→02_自治会・地区/城東。
- **入れ子.claude隔離（4箇所・偽エージェント汚染の再発）**: kusagawa_archive/・design_system/・design_system/templates/・01_council/ 配下→`~/Archive/_trash_pending_2026-07-22/nested_claude/`。セッション再起動まで偽エージェント表示は残る。
- **💾Macローカルミラー初回実行**: drafts143M/outputs696M/publications122M/~scripts → Drive。※openrsyncは`--iconv`非対応（usageエラーになる）。
- **restore.sh修理**: scripts-claude(td.py)・CLAUDE.md・launchd plist+ランナーの復元を追加＋手動セットアップ手順（Todoistトークン/Drive Desktop/FDA/symlink）を明記。README.mdも更新。

## 引き継ぎ体制の結論
- claude-config自動同期は健全（Stop hookで毎セッションpush・当日確認済）。カバー=agents/skills/memory/settings/td.py/CLAUDE.md/launchd。
- 一次資料はDriveが正本で安全。生成物はミラー新設でカバー。
- **残る唯一の大穴=Time Machine未設定**: `~/Archive` 17GB（録音・Takeout・資料倉庫）・Movies 1.9GB・Photosライブラリはこのマシン単独保有。

## 残タスク（要対応）
- [x] 夜間パイプラインv4化 — 2026-07-22草川承認済・本体適用済（構文チェックPASS・今夜2:30から稼働）
- [ ] バックアップ最後の穴: **~/Archive 17GB・Movies 1.9GBはiCloudにもDriveにも入っていない**（Desktop/DocumentsはiCloud同期ON確認済16GB・drafts/outputs/publicationsはDriveミラー済）。写真AppのiCloud写真ON/OFFは未確認。草川は「iCloudに入ってるのでは」と認識→事実を伝えたが対応方針は未決（TM or ArchiveのDriveミラー追加はDrive容量次第）
- [ ] `~/Archive/_trash_pending_*` 4フォルダ: 2026-07-22に中身一覧を提示済み・削除判断待ちのまま保留。`_要確認_20260702`（38MB・19件）も未レビュー
- [ ] SNSニュース収集WebFetch 403が5日連続（クラウド側・7/17修理タスク未解決）／日曜Discord監査(sunday_audit)が7/19失敗／update_status.pyのtmpファイルバグ
- サマーキャンプ報告書7/24は提出済み（タスク不要・2026-07-22草川回答）

## 既知の無害物
- `~/docs`=superpowersスキル作業場、`~/nichijo-mobile-project-instructions.md`=ホーム直下野良（軽微）、Desktop=スクショ10枚+写真候補3フォルダ（30日で自動スイープ対象）、`~/Archive/claude-config-full-history-20260705.bundle` 730MB=git履歴の保険。
