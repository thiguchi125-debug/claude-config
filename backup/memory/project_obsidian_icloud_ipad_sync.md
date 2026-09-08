---
name: project-obsidian-icloud-ipad-sync
description: ObsidianVaultのiPad同期は2026-09-09に完了・iPadで実機確認済。旧実体の削除承認だけ未了
metadata:
  type: project
---

2026-09-09時点。ObsidianVault（`~/Documents/ObsidianVault`・175ファイル/82MB）をiPadと同期する作業。

**確定した事実（調べ直し不要）**
- `~/Documents` は「デスクトップと書類」iCloud同期がONで、vaultは既にiCloud Drive上にある。だが **iOS/iPadOS版Obsidianは自分専用コンテナ `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/` のvaultしか開けない**。iCloud Driveの任意フォルダは選べないので、移動しない限りiPadから見えない。
- **公式Obsidian Sync Standard（$4/月）は1ファイル5MB上限で使えない**。`議場カード_全7枚_v3.pdf` が6.7MBあり、超過分は静かにスキップされる。課金するならPlus（$8/月・200MB上限）一択。商用ライセンスは現在「任意」なので議員活動でも追加費用なし。
- macOS 26.4.1 Tahoe の「Macストレージを最適化」は システム設定 → アカウント名 → iCloud → **Drive** → の中。iCloudのトップ画面には無い。`一般 → ストレージ` の「ストレージを最適化」は別物（映画・メール添付が対象）。

**済み（2026-09-09に移動まで完了）**
- vaultを `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVault` へ移動（175ファイル/82MB・件数照合一致）。旧パス `~/Documents/ObsidianVault` は互換symlink。旧実体は `~/Archive/_trash_pending_20260909_ObsidianVault_old`
- `obs_open.sh` の `VAULT_DIR` を新パスへ更新（旧パス指定も受ける）／`OPERATIONS.md` L114 更新
- 「Macストレージを最適化」OFF（2026-09-09・`defaults read com.apple.bird optimize-storage` = 0）
- `~/.claude/scripts/vault_guard.sh` … 退避検知→`brctl download`で引き戻し→`~/Archive/_vault_backup/`へ控え。手動実行
- `~/.claude/scripts/vault_to_icloud_obsidian.sh` … 移動用。**未実行**。Obsidian起動中なら自分で止まる

**2026-09-09 完了**
- Obsidianの登録パスを実パスへ書き換え（`obsidian.json`・bakあり）。再起動後も定着
- iPadにObsidian導入→「Store in iCloud」でvault読込成功。`議場カード_全7枚_v3.pdf`（6.7MB）を実機で開けることを草川が確認

**次の一手**
1. 旧実体 `~/Archive/_trash_pending_20260909_ObsidianVault_old`（180ファイル）の削除承認待ち
2. `vault_guard.sh` のlaunchd毎日実行は「@日曜改修」枠で（[[feedback-maintenance-weekly-window]]）

**macOS 26で判明した罠**
- **`brctl` コマンドは機能しない**。`brctl status` は標準のCloudDocsコンテナでも `Client zone not found` を返す。同期の可否とは無関係なので、このエラーを故障と誤読しないこと。退避ファイルの引き戻しは実ファイルを `cat` して FileProvider に materialize させる方式に変更済（`vault_guard.sh`）
- PyObjCが入っていないため、アップロード完了のCLI確認もできない。最終確認はiPad実機

**注意**
- vaultには `40_市民対応/` の相談者氏名が入る。iPadに乗せる以上パスコード／Face IDと「探す」は必須
- 移動時に更新が要るパス参照は2か所だけ＝`~/.claude/scripts/obs_open.sh` の `VAULT_DIR` と `OPERATIONS.md` L114（[[feedback-open-md-in-obsidian-not-notion]]）
