---
name: drive-structure-v2-2026-05-21
description: Drive運用構造v2（投函口2系統＋月別取込済アーカイブ＋日常資料4カテゴリ）の設計と草川手動移行手順
metadata: 
  node_type: memory
  type: project
  originSessionId: 8d7d8ad2-37b3-49a7-aa1b-b2823bc87805
---

# Drive運用構造 v2（2026-05-21〜）

## 設計の骨子
- 投函口を **2つだけ** に絞る: `_INBOX_council/`（議会資料）／`_INBOX_daily/`（日常資料）
- 取込後の元ファイルは **`_processed_<YYYY-MM>/`** に月別退避 → INBOXは常にクリーン
- 議会資料の最終置き場は `議会資料アーカイブ/`（旧「議事録（年度別）」改名）
- 日常資料の最終置き場は `日常資料アーカイブ/` 配下4カテゴリ＋その他

**Why:** Drive `_INBOX_新規投函/` 直下に取込後も元ファイルが滞留、議会資料以外（自治会・後援会・印刷物素材）の振分先が未定義で散らかっていた問題への対応。投函口2系統に絞ることで草川が迷わない、月別退避で履歴も追える。
**How to apply:** 新規Drive投函は2投函口のどちらかへ。取込済の整理は drive-sync-review／council-materials-intake で自動振分（ローカル）＋草川手動move（Drive側、MCP制約のため）。

## Drive 新構造

```
ROOT (1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg)
│
├── 📥 _INBOX_council/                    投函口（議会資料用） NEW
│   │   ID: 1fJjS-auqrG9wKa97BPmksBJCHwFVvd_4
│   └── _processed_2026-05/                ID: 1sEFF8xsjWhoWuh52WZ9_8a49-3tw7v8F
│
├── 📥 _INBOX_daily/                      投函口（日常資料用）
│   │   ※草川リネーム後発効（現「_INBOX_新規投函」)
│   │   旧ID: 1Cxn0oFSK7QnpWZN0QsQtd2D2OD_F9MMF
│   └── _processed_<YYYY-MM>/             ※草川手動作成
│
├── 📂 議会資料アーカイブ/                 ※草川リネーム後発効
│      旧名「議事録（年度別）」
│      旧ID: 19j_dfqIjXST9qNxRcFpYSHBD5Z9eBI9E
│
├── 📂 日常資料アーカイブ/                 NEW
│   │   ID: 1-rm_sM2296Q0wpUiDxuxJjRDbP4heVjx
│   ├── 01_政策素材/      要望書/陳情/提案書/事業計画/プレゼン  ID: 1ZOrg2z08A5M4OSHzKrxO4BTjR2LVJn5V
│   ├── 02_自治会・地区/   組分け図/地区組織図/まちづくり協      ID: 16vYWkszTpBH_DxUL5iLrha_IRxsVPims
│   ├── 03_後援会・組織/   業界団体/組合/JC/ライオンズ          ID: 1xnxcxOTypWwLgWdluuNgLQMIjVkuFP4-
│   ├── 04_印刷物素材/     チラシ/応援カード/市政報告草案       ID: 1VBkslIwzMz3dGac1l3UgdvRPPhXhWfCG
│   └── 99_その他/        上記非該当                          ID: 1m6CKWXCvmqa7gUICwt_vGyDYeboKoKle
│
├── ZZ_市政報告レポート/     既存
└── ZZ_選挙関連/            既存
```

## ローカル振分先（kusagawa_archive/）

| Drive配置 | ローカル配置 |
|---|---|
| `議会資料アーカイブ/RXX/MM_定例会/種別/` | `01_council/RXX-MM_定例会/種別/` |
| `日常資料アーカイブ/01_政策素材/` | `05_resources/01_政策素材/` |
| `日常資料アーカイブ/02_自治会・地区/` | `05_resources/02_自治会・地区/` |
| `日常資料アーカイブ/03_後援会・組織/` | `05_resources/03_後援会・組織/` |
| `日常資料アーカイブ/04_印刷物素材/` | `99_raw/_drive_originals/print_materials/` |
| `日常資料アーカイブ/99_その他/` | （草川判断・自動cpスキップ） |

## 草川手動Drive UI操作（残作業）

### A. フォルダリネーム 2件
1. `_INBOX_新規投函` → `_INBOX_daily` にリネーム
   - URL: https://drive.google.com/drive/folders/1Cxn0oFSK7QnpWZN0QsQtd2D2OD_F9MMF
   - 操作: 右クリック → 名前を変更
2. `議事録（年度別）` → `議会資料アーカイブ` にリネーム
   - URL: https://drive.google.com/drive/folders/19j_dfqIjXST9qNxRcFpYSHBD5Z9eBI9E
   - 操作: 右クリック → 名前を変更

### B. `_council_pending/` の中身を `_INBOX_council/` に移動
- 元: `_INBOX_新規投函/_council_pending/` (1Uk2yabgrJCz56KQP1i2AThGTAMGKKh-l) 内のPDF全件
- 移動先: `_INBOX_council/` (1fJjS-auqrG9wKa97BPmksBJCHwFVvd_4)
- 操作: 該当ファイル全選択 → 右クリック → 移動 → `_INBOX_council/` 選択
- 完了後、空になった `_council_pending/` フォルダは削除 or 残置（次回投函時の互換のため一旦残置でOK）

### C. 既存 `_INBOX_新規投函/` 直下11件の振分

| ファイル | 移動先 |
|---|---|
| 小下自治会組分け住宅地図.pdf | 日常資料アーカイブ/02_自治会・地区/ |
| 昼生地区まちづくり協議会組織図2026 | 日常資料アーカイブ/02_自治会・地区/ |
| 楠の木会.pdf | 日常資料アーカイブ/03_後援会・組織/ |
| CO−niwa　プレゼン原案_20260410_214940_0000.pdf | 日常資料アーカイブ/01_政策素材/ |
| 防災キャンプ企画（出店企業様向け）最新 4.pdf | 日常資料アーカイブ/01_政策素材/ |
| 祭食材の価格目安.pdf | 日常資料アーカイブ/01_政策素材/ |
| mixi2.pdf | 日常資料アーカイブ/99_その他/ |
| 亀山市への要望.pdf | 日常資料アーカイブ/01_政策素材/ |
| 応援カード表面修正版0504.pdf | 日常資料アーカイブ/04_印刷物素材/ |
| index.html | 日常資料アーカイブ/99_その他/ |

操作: Drive UIで各ファイル右クリック → 移動 → 上表の宛先選択

## スキル＆スクリプト改修済（2026-05-21完了）

### スキル統合
- **drive-sync-review → drive-intake にリネーム＋4モード化**
- **council-materials-intake は deprecated**（drive-intake へリダイレクト）
- 4モード: A.即時取込・議会 / B.即時取込・日常 / C.レビュー承認 / D.手動Drive差分

### スクリプト
- `_drive_sync.sh`: 日常資料処理ブロック＋Drive後処理呼び出し追加
- `_drive_postprocess.sh`: 新規作成（rclone自動move＋[DONE_<日付>]prefix）

### rclone導入＋完全自動化（2026-05-21追加）
- brew install rclone 完了（v1.74.1）
- `_drive_sync.sh` 冒頭にrclone DLステップ追加 → MCP不要で自走可能
- launchd plist `~/Library/LaunchAgents/com.kusagawa.drive-sync.plist` 作成済
  - 通常期: 朝7:00・夜22:00の2回/日
  - 議会期: 7,13,19,22時の4回/日（council-mode-toggleで切替）
- council-mode-toggle 拡張: クラウドRoutine cron＋ローカルlaunchd plistを同時切替

### トリガー1本化（2026-05-21）
- メイントリガー: **「ドライブ資料取り込んで」**（一言で4モード自動順次実行）
- 旧トリガー（「議会資料取り込んで」「取込確認」「Drive差分スキャン」等）は後方互換で全て同じ統合フローを起動

### 完全自動化フロー
```
[launchd 毎朝7時・毎晩22時]  ※議会期は4回/日
  ↓
_drive_sync.sh
  ↓
①rclone copy: _INBOX_council/, _INBOX_daily/ → local
②pdftotext + メタデータ抽出 + カテゴリ振分
③ローカル archive 配置（01_council/, 05_resources/01-04, etc.）
④_drive_postprocess.sh: rclone moveto で Drive側を
  [DONE_<日付>]_<元名> にリネーム＋_processed_<YYYY-MM>/ にmove
  ↓
ログ: _launchd_stdout.log / _launchd_stderr.log
例外（OCR要・未分類）は朝のohayoブリーフィングで通知
```

### ⚠️ 草川作業（初回のみ・約15分）
**① rclone config OAuth設定**（5分）
```
rclone config
→ n (New remote)
→ name: kusagawa_drive
→ Storage: drive
→ scope: 1 (Full access)
→ ブラウザで t.higuchi125@gmail.com でログイン→許可
→ Configure as Shared Drive: n
→ Keep: y
→ Quit: q
```
動作確認: `rclone lsd kusagawa_drive:草川議会質問アーカイブ/`

**② launchd 起動**（1分）
```
launchctl load ~/Library/LaunchAgents/com.kusagawa.drive-sync.plist
launchctl list | grep kusagawa  # 確認: com.kusagawa.drive-sync 表示されればOK
```

**③ Drive UI 既存整理**（10分）
- `_INBOX_新規投函` → `_INBOX_daily` リネーム
- `議事録（年度別）` → `議会資料アーカイブ` リネーム
- 既存INBOX 11件を `日常資料アーカイブ/<カテゴリ>/` へ振分

3作業完了後は **完全無人運用**（草川は投函してDriveに資料置くだけ）。

## rclone config 設定手順（草川作業・初回のみ・5分）

ターミナルで以下を実行:

```
rclone config
```

対話プロンプトに以下で回答:

| 質問 | 回答 |
|---|---|
| Current remotes | `n` (New remote) |
| name> | `kusagawa_drive` |
| Storage > | `drive` (Google Drive) ※番号入力 |
| client_id> | （空Enter） |
| client_secret> | （空Enter） |
| scope> | `1` (Full access all files) |
| service_account_file> | （空Enter） |
| Edit advanced config? > | `n` |
| Use auto config? > | `y` |
| → ブラウザが開く | Googleアカウント `t.higuchi125@gmail.com` でログイン→Drive権限許可 |
| Configure as Shared Drive? > | `n` |
| Keep this "kusagawa_drive" remote? > | `y` |
| Quit config > | `q` |

設定後、動作確認:
```
rclone lsd kusagawa_drive:草川議会質問アーカイブ/
```
フォルダ一覧が出ればOK。

## 関連
- 議論セッション: 2026-05-21
- 関連skill: drive-sync-review, council-materials-intake, council-mode-toggle
- 関連MEMORY: [[project_drive_sync_v2]]（旧Drive→ローカル同期v2拡張）
- 既知の制約: Drive MCP に move/rename/delete tool 無し → Drive側ファイル操作は草川手動 or 将来 rclone/OAuth 自動化
