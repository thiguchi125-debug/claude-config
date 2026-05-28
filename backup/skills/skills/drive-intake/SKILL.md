---
name: drive-intake
description: 草川たくや（亀山市議会議員）のDrive→ローカル統合取込スキル。**メイントリガーは「ドライブ資料取り込んで」「Drive取り込んで」「取り込んで」「資料取り込んで」の一言**。**v3 2026-05-28: Google Drive Desktopミラー方式に移行。Drive→Local同期はOS daemonが自動・リアルタイムなので、本スキルの仕事は「_INBOX_council/と_INBOX_daily/の新着→pdftotext→カテゴリ判定→正規配置にmv→Notion登録」に変化**。後方互換: 「議会資料取り込んで」「daily取込」「取込確認」「Drive差分スキャン」「議会資料インテーク」「council-materials-intake」「drive-sync-review」も全て同じ統合フローを起動。
---

# ⚠️ v3 移行中（2026-05-28〜）：このSKILL.md本体はv2前提のまま未書換

以下の前提読み替えが必要：

| v2 SKILL.md記述 | v3 実機 |
|---|---|
| `launchd が _drive_sync.sh を裏で実行` | **不在**（plistは `~/Library/LaunchAgents/_deprecated_2026-05-28/` に退避） |
| `rclone copy で Drive→Local DL` | **不要**（Drive Desktopが自動ミラー、~30秒遅延） |
| `rclone moveto で Drive側を _processed_ に整理` | 不可。代わりに `mv ~/.claude/agents/knowledge/kusagawa_archive/_drive/_INBOX_xxx/file ~/.claude/agents/knowledge/kusagawa_archive/_drive/<カテゴリ>/` で行う（symlink経由でDrive側に反映） |
| Drive側パス`1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg`を直接操作 | **ローカル経由**：`~/.claude/agents/knowledge/kusagawa_archive/_drive/...`（symlink） |
| Drive構造 `_INBOX_新規投函/` | `_INBOX_daily/` にリネーム済 |
| Drive構造 `_INBOX_新規投函/_council_pending/` | `_INBOX_council/` に統合済（subfolder廃止） |
| Drive構造 `議事録（年度別）` | `議会資料アーカイブ` にリネーム済 |
| 日常資料カテゴリ 4個＋99 | **5個＋99**（05_視察・外部交流 新設） |

詳細仕様は `~/.claude/projects/-Users-kusakawatakuya/memory/project_drive_structure_v3.md` を参照。

**SKILL.md本体の書き換えは未実施・別セッションで対応予定**。当面はこのv3移行ノートを優先、以下v2記述は前提読み替えで利用。

---

# Drive 統合取込（drive-intake）

## メイントリガー
**「ドライブ資料取り込んで」** ／ 「Drive取り込んで」 ／ 「取り込んで」 ／ 「資料取り込んで」

→ 4モード全部を自動順次チェックして必要分だけ取込。草川は一言で済む。

## 全体フロー（メイントリガー実行時）

```
[Step 1] _INBOX_council/ をスキャン
  ├─ 投函あり → 議会資料取込（モードA）
  └─ なし → スキップ

[Step 2] _INBOX_daily/ をスキャン
  ├─ 投函あり → 日常資料取込（モードB）
  └─ なし → スキップ

[Step 3] Notion📥Drive取込キューDB をスキャン
  ├─ 保留あり → 草川に承認問いかけ（モードC）
  └─ なし → スキップ

[Step 4] Drive側 取込済ファイル整理（rclone）
  └─ [DONE_<日付>]_<元名> にリネーム＋ _processed_<YYYY-MM>/ にmove

[Step 5] サマリ報告
  ✅ 議会資料: X件 / 日常資料: Y件 / DB保留: Z件処理
```

## 後方互換トリガー（旧スキル統合済）

| 旧トリガー | 統合元 |
|---|---|
| 「議会資料取り込んで」「議案書取り込んで」「議会資料インテーク」「council-materials-intake」 | 旧council-materials-intake（モードA相当） |
| 「日常資料取り込んで」「daily取込」「INBOX_daily取込」 | 新規（モードB相当） |
| 「取込確認」「Drive取込確認」「pendingレビュー」「ドライブ確認待ち」「/drive-sync-review」 | 旧drive-sync-review モードA（モードC相当） |
| 「Drive差分スキャン」「routine止まってる」「週次Drive同期手動実行」 | 旧drive-sync-review モードB（モードD相当） |

これら旧トリガーで起動した場合も**メイントリガーと同じ統合フロー**を実行（特定モードだけに絞らない）。

---

## 完全自動運用（launchd）

このスキル手動起動は**緊急時のみ**。通常は macOS launchd が裏で自動実行している:

| モード | 実行頻度 |
|---|---|
| 通常期 | 毎朝7:00・毎晩22:00（1日2回） |
| 議会期 | 毎日 3時間ごと（council-mode-toggleで切替） |

実行内容（無人）:
```bash
~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_sync.sh
```
スクリプト内部で:
1. rclone copy で `_INBOX_council/` `_INBOX_daily/` をローカルへDL
2. pdftotext + メタデータ抽出 + カテゴリ振分
3. rclone moveto で Drive側を `_processed_<YYYY-MM>/` に整理＋ [DONE_<日付>]_ prefix付与
4. ログを `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_sync_state.json` に記録

例外（OCR要・未分類）は ohayo の朝ブリーフィングに表示される。

---

## Drive構造（2026-05-21〜）

```
ROOT (1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg)
├── _INBOX_council/          1fJjS-auqrG9wKa97BPmksBJCHwFVvd_4
│   └── _processed_<YYYY-MM>/  ※launchdが月初に自動作成
├── _INBOX_daily/            ※草川リネーム後発効
│   └── _processed_<YYYY-MM>/
├── 議会資料アーカイブ/        ※草川リネーム後発効
└── 日常資料アーカイブ/        1-rm_sM2296Q0wpUiDxuxJjRDbP4heVjx
    ├── 01_政策素材/      1ZOrg2z08A5M4OSHzKrxO4BTjR2LVJn5V
    ├── 02_自治会・地区/   16vYWkszTpBH_DxUL5iLrha_IRxsVPims
    ├── 03_後援会・組織/   1xnxcxOTypWwLgWdluuNgLQMIjVkuFP4-
    ├── 04_印刷物素材/    1VBkslIwzMz3dGac1l3UgdvRPPhXhWfCG
    └── 99_その他/        1m6CKWXCvmqa7gUICwt_vGyDYeboKoKle
```

## 自動振分ロジック（ファイル名キーワード）

| カテゴリ | キーワード | Drive配置先 | ローカル配置先 |
|---|---|---|---|
| 01_政策素材 | 要望/陳情/提案書/意見書/プレゼン/企画/事業計画/資料 | 日常資料アーカイブ/01_政策素材/ | 05_resources/01_政策素材/ |
| 02_自治会・地区 | 自治会/組分け/まちづくり/地区/組織図/回覧 | 日常資料アーカイブ/02_自治会・地区/ | 05_resources/02_自治会・地区/ |
| 03_後援会・組織 | 後援/業界/組合/商工/農協/JC/ライオンズ/ロータリー/会員 | 日常資料アーカイブ/03_後援会・組織/ | 05_resources/03_後援会・組織/ |
| 04_印刷物素材 | チラシ/リーフレット/市政報告/応援カード/ポスター/名刺/印刷 | 日常資料アーカイブ/04_印刷物素材/ | 99_raw/_drive_originals/print_materials/ |
| 99_その他 | 上記非該当 | 日常資料アーカイブ/99_その他/ | （草川判断・自動cpスキップ） |

議会資料は別ロジック（`_extract_gian_metadata.py`）でRXX-MM_定例会/種別 を抽出。

---

## モードC（Notion DB承認）が必要なケース

通常は launchd が完全自動化するため不要。ただし以下では草川承認問いかけが入る:

1. **未分類ファイル**（キーワード非該当・議会回次抽出失敗）
2. **OCR要**（pdftotext結果が極端に小さい＝画像PDF）
3. **クラウドRoutine `weekly-drive-sync-kusagawa` がNotion DBに積んだファイル**で、ローカルrclone copyとは別経路のもの

これらは ohayo の朝ブリーフィングで「📋 Drive取込 確認待ち N件」として表示される。草川が「ドライブ資料取り込んで」or「取込確認」と言えば該当フローが起動。

Notion DB:
```
DB ID: ed2d5e6a-96f9-401f-a204-c3431602de41
data_source_id: 5187247b-f6ea-420a-a80c-154947911f64
URL: https://www.notion.so/ed2d5e6a96f9401fa204c3431602de41
```

---

## エラー処理

- rclone未設定 or remote名不一致 → Drive側整理スキップ、草川手動move依頼メッセージ表示
- pdftotext失敗（OCR要） → `99_raw/_needs_ocr/<sub>/` 隔離、朝ブリーフィングでフラグ
- 草川パート抽出が0セッション → `_drive_originals/<sub>/_text/` 残し、DB に「抽出失敗・要手動確認」コメント
- 議会回次判定失敗 → `_needs_classify/` 退避＋朝ブリーフィングで草川入力依頼

## 関連
- 同期スクリプト本体: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_sync.sh`
- Drive後処理: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_postprocess.sh`（rclone）
- launchd plist: `~/Library/LaunchAgents/com.kusagawa.drive-sync.plist`
- 抽出スクリプト: `_extract_kusagawa.py` / `_extract_committee.py` / `_extract_gian_metadata.py` / `_classify.py`
- Notion DB: https://www.notion.so/ed2d5e6a96f9401fa204c3431602de41
- 関連skill: council-mode-toggle（launchd頻度切替）

## 旧スキルからの移行（2026-05-21）
- 旧 `drive-sync-review` → 本スキルに改名統合
- 旧 `council-materials-intake` → deprecated（フォルダ残置のみ）
- 旧 `weekly-drive-sync` → 2026-05-21に旧drive-sync-review経由で本スキルへ統合済
- 旧クラウドRoutine `weekly-drive-sync-kusagawa` → ローカルlaunchdに役割移管予定（クラウドRoutineは継続稼働させて補完）
