---
name: project-obsidian-icloud-ipad-sync
description: ObsidianVaultをiPadへiCloud同期する計画。退避対策は完了、vault移動は9月議会本番後に保留中
metadata:
  type: project
---

2026-09-09時点。ObsidianVault（`~/Documents/ObsidianVault`・175ファイル/82MB）をiPadと同期する作業。

**確定した事実（調べ直し不要）**
- `~/Documents` は「デスクトップと書類」iCloud同期がONで、vaultは既にiCloud Drive上にある。だが **iOS/iPadOS版Obsidianは自分専用コンテナ `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/` のvaultしか開けない**。iCloud Driveの任意フォルダは選べないので、移動しない限りiPadから見えない。
- **公式Obsidian Sync Standard（$4/月）は1ファイル5MB上限で使えない**。`議場カード_全7枚_v3.pdf` が6.7MBあり、超過分は静かにスキップされる。課金するならPlus（$8/月・200MB上限）一択。商用ライセンスは現在「任意」なので議員活動でも追加費用なし。
- macOS 26.4.1 Tahoe の「Macストレージを最適化」は システム設定 → アカウント名 → iCloud → **Drive** → の中。iCloudのトップ画面には無い。`一般 → ストレージ` の「ストレージを最適化」は別物（映画・メール添付が対象）。

**済み**
- 「Macストレージを最適化」OFF（2026-09-09・`defaults read com.apple.bird optimize-storage` = 0）
- `~/.claude/scripts/vault_guard.sh` … 退避検知→`brctl download`で引き戻し→`~/Archive/_vault_backup/`へ控え。手動実行
- `~/.claude/scripts/vault_to_icloud_obsidian.sh` … 移動用。**未実行**。Obsidian起動中なら自分で止まる

**次の一手**
1. 9/10・11の一般質問本番後に `vault_to_icloud_obsidian.sh` を実行（Obsidian終了が前提）。移動後に「フォルダをVaultとして開く」で新パスを指定し旧エントリを削除。旧パスには互換symlinkが張られる
2. `vault_guard.sh` のlaunchd毎日実行は「@日曜改修」枠で（[[feedback-maintenance-weekly-window]]）
3. iPad側：Obsidianインストール → 「Store in iCloud」で ObsidianVault を選択

**注意**
- vaultには `40_市民対応/` の相談者氏名が入る。iPadに乗せる以上パスコード／Face IDと「探す」は必須
- 移動時に更新が要るパス参照は2か所だけ＝`~/.claude/scripts/obs_open.sh` の `VAULT_DIR` と `OPERATIONS.md` L114（[[feedback-open-md-in-obsidian-not-notion]]）
