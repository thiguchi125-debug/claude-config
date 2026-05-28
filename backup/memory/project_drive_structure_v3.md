---
name: drive-structure-v3-2026-05-28
description: Drive運用構造v3（Google Drive Desktop ミラー方式＋taxonomy 5カテゴリ）。v2のrclone/launchd路線を全廃しDrive Desktopに一本化。
metadata: 
  node_type: memory
  type: project
  originSessionId: a885a2e2-dc7c-4d32-ad9a-a1d8f6f9e89a
---

# Drive運用構造 v3（2026-05-28〜）

## 設計の骨子（v2→v3 変更点）

| 観点 | v2（2026-05-21設計、設定で停滞） | v3（2026-05-28実装、稼働中） |
|---|---|---|
| 同期機構 | rclone CLI + launchd plist 2-4回/日 | **Google Drive Desktop**（ミラーモード、リアルタイム） |
| 初回設定 | rclone config OAuth + launchctl load + Drive UI整理（15分・草川が止まった） | アプリインストール + サインイン + ミラー選択（10分・完了済） |
| Drive→Local | cron バッチコピー | OS daemon が ~30秒で自動ミラー |
| Local→Drive | 手動 or scriptトリガー | Local mv が自動でDriveに反映（iPhone側にも届く） |
| iPhone→Mac | 最大12時間遅延 | 1分以内 |

**Why v3：** v2の停止原因はtaxonomyではなく **rclone OAuth設定** という初回手作業の高い摩擦。Drive Desktopに切り替えると、草川作業は「アプリ入れてサインイン」だけ、それ以降の同期は全自動。

**How to apply：** 新規投函はDriveの`_INBOX_council/`または`_INBOX_daily/`へ。iPhoneでもMacでも同じUX。Claude Code側は `~/.claude/agents/knowledge/kusagawa_archive/_drive/` symlinkで直接grep可。

## 3層アーキテクチャ

```
┌─────────────────────────────────────────────────────┐
│ Layer 1: Drive クラウド（一次保管）                    │
│ https://drive.google.com/drive/folders/             │
│   1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg                 │
│ フォルダ名: 草川たくや 議会質問アーカイブ              │
└─────────────────────────────────────────────────────┘
         ↑↓ Google Drive Desktop（ミラーモード）
┌─────────────────────────────────────────────────────┐
│ Layer 2: CloudStorage ローカル実体（macOS）           │
│ ~/Library/CloudStorage/                             │
│   GoogleDrive-t.higuchi125@gmail.com/               │
│   マイドライブ/草川たくや 議会質問アーカイブ/         │
└─────────────────────────────────────────────────────┘
         ↓ symbolic link
┌─────────────────────────────────────────────────────┐
│ Layer 3: Claude Code 作業領域                         │
│ ~/.claude/agents/knowledge/kusagawa_archive/_drive/  │
│   → Layer 2 へのsymlink                              │
└─────────────────────────────────────────────────────┘
```

## Drive構造（v3確定形）

```
草川たくや 議会質問アーカイブ/
│
├── 📥 _INBOX_council/                投函口（議会資料）
│   └── _processed_<YYYY-MM>/         （取込済の月別退避）
│
├── 📥 _INBOX_daily/                  投函口（日常資料）
│   └── _processed_<YYYY-MM>/
│
├── 📂 議会資料アーカイブ/             （旧名「議事録（年度別）」をv3でリネーム）
│   ├── H30 (2018-12〜2019-2)/
│   ├── R01 (2019)/ 〜 R07 (2025)/
│   └── R08 (2026)/
│       ├── 03_定例会/
│       ├── 06_定例会/                ← 2026年6月議会の議案・委員会資料はここ
│       ├── 09_定例会/
│       ├── 12_定例会/
│       └── 委員会・全協（会期外）/
│
├── 📂 日常資料アーカイブ/             5カテゴリ＋その他
│   ├── 01_政策素材/                  他自治体事例・要望書・統計・記事
│   ├── 02_自治会・地区/               組分け図・地区組織図・まちづくり協
│   ├── 03_後援会・組織/               業界団体・組合・JC・ライオンズ
│   ├── 04_印刷物素材/                 チラシ・応援カード・市政報告草案
│   ├── 05_視察・外部交流/             ← v3新設（4カテゴリの「視察・外部交流」担当）
│   │   ├── 視察レポート/
│   │   ├── 講演・研修/
│   │   └── 名刺・連絡先/
│   └── 99_その他/                     上記非該当
│
├── 📂 00_INDEX/                       （既存）
├── 📂 ZZ_市政報告レポート/             （既存）
└── 📂 ZZ_選挙関連/                    （既存）
```

## ローカル振分対応（kusagawa_archive配下）

| Drive配置 | ローカル参照 |
|---|---|
| `議会資料アーカイブ/RXX/MM_定例会/` | `~/.claude/agents/knowledge/kusagawa_archive/_drive/議会資料アーカイブ/RXX/MM_定例会/` |
| `日常資料アーカイブ/01_政策素材/` | 同上 `_drive/日常資料アーカイブ/01_政策素材/` |
| `日常資料アーカイブ/05_視察・外部交流/` | 同上 |
| `_INBOX_council/` | 同上 `_drive/_INBOX_council/` |

既存の `01_council/`〜`99_raw/` は引き続きローカル専用（agentの中間処理、voice-dna、policy_compass、選挙データ等）として保持。

## v3移行で実行したこと（2026-05-28）

1. ✅ Google Drive Desktop インストール＋サインイン＋ミラーモード選択
2. ✅ `~/.claude/agents/knowledge/kusagawa_archive/_drive/` symlink作成（→ CloudStorage実体）
3. ✅ Drive側フォルダリネーム: `議事録（年度別）`→`議会資料アーカイブ`、`_INBOX_新規投函`→`_INBOX_daily`
4. ✅ `日常資料アーカイブ/05_視察・外部交流/` 新規作成（サブ3フォルダ含む）
5. ✅ `_INBOX_daily/_council_pending/` の6件を `_INBOX_council/` 統合（5件保持、1件は99_その他、TEST marker削除）
6. ✅ `_INBOX_daily/` 直下の12件を各カテゴリへ振分（01_政策素材6件・02_自治会2件・03_後援会1件・04_印刷物1件・99_その他2件）
   - うち1件は `file_20265181152626_1.pdf` を `R8-06_中学校給食献立予定表.pdf` にリネーム
7. ✅ 旧launchd plist `com.kusagawa.drive-sync` を unload→`~/Library/LaunchAgents/_deprecated_2026-05-28/` に退避
8. ✅ `_drive_sync.sh` `_drive_postprocess.sh` を `kusagawa_archive/99_raw/_scripts/_deprecated_v2_drive_sync_2026-05-28/` に退避
9. ✅ CLAUDE.md主要リソース欄 更新（v3アクセス手段3つ明記）

## v3.1 追加実装（2026-05-29）

10. ✅ drive-intake skill v3クリーン書き換え（rclone/launchd記述完全削除、カテゴリ判定辞書追加）
11. ✅ council-mode-toggle skill v3簡素化（launchd plist操作撤回、flag管理＋任意Routine cron切替に）
12. ✅ `_index/` 処理パイプライン構築（`_build_index.sh`＋launchd nightly 2:30）。初回フルスキャン101 PDF抽出済
13. ✅ `_INBOX_council/` 残5件配置（議案書2件＋委員会資料1件をR8.3/各サブへ、README＋_processed_は構造として残置）
14. ✅ **マイドライブ大整理**: 325件＋既存10フォルダ →「草川たくや 議会質問アーカイブ」1個のみに集約
    - Batch A (議会資料): 45件
    - Batch B-D (後援会・組織): 78件（亀山JC46/くすのき会5/亀山社中1/飲食業組合2/三重パラ陸協4/消防団1/亀山eスポーツ協会17/JC文化資料2）
    - Batch E-F (自治会・政策素材): 65件
    - Batch G-H (市政報告・個人): 35件
    - 追加分類: 25件
    - 要判定残: 169件（`日常資料アーカイブ/99_その他/要判定_2026-05-29/`）
15. ✅ **日次自動パイプライン**: `_auto_intake.sh`（INBOX→キーワード判定→正規配置）＋`_build_index.sh`（pdftotext→_index）を統合した `_daily_drive_pipeline.sh` を launchd `com.kusagawa.daily-drive-pipeline` で毎晩2:30実行

## TODO（次回以降）

- [ ] `要判定_2026-05-29/`169件の分類（草川と1個ずつ確認しながら順次）
- [ ] `_auto_intake.sh` のキーワード辞書追加学習（新たなテーマ追加時に随時）
- [ ] ohayo に「昨夜のパイプライン処理結果」セクション追加（_pipeline.log末尾を要約）

## 関連

- 旧版: [[project_drive_structure_v2]]（2026-05-21設計、rclone路線、停止）
- 関連skill: drive-intake（要更新）、council-mode-toggle（要更新）
- 過去シリーズ: [[project_drive_sync_v2]]、[[project_mydrive_full_intake]]
