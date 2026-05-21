---
name: drive-intake
description: 草川たくや（亀山市議会議員）のDrive→ローカル統合取込スキル（旧drive-sync-review + council-materials-intake 統合、2026-05-21）。4モード運用 — A. 即時取込・議会資料／B. 即時取込・日常資料／C. レビュー承認型／D. 手動Drive差分スキャン。トリガー: 「議会資料取り込んで」「議案書取り込んで」「日常資料取り込んで」「daily取込」「取込確認」「Drive取込確認」「ドライブ確認待ち」「pendingレビュー」「Drive差分スキャン」「routine止まってる」「議会資料インテーク」「council-materials-intake」「drive-intake」「drive-sync-review」「週次Drive同期手動実行」等。リモートRoutine `weekly-drive-sync-kusagawa` が日曜21時JSTにDrive差分をNotion DBに登録 → このスキルでローカル取込実行。取込後はrcloneでDrive側を _processed_<YYYY-MM>/ に自動move＋[DONE_<日付>]prefix自動付与。
---

# Drive 統合取込（drive-intake）

## 役割
Driveに投函された資料（議会資料／日常資料）を、ローカル `kusagawa_archive/` に統合的に取り込み、Drive側も自動整理する単一エントリポイント。

旧 `drive-sync-review` ＋ `council-materials-intake` ＋ 廃止された `weekly-drive-sync` を2026-05-21に統合。

## 4モード一覧

| モード | 主な起動キーワード | 起点 | 流れ |
|---|---|---|---|
| **A. 即時取込・議会資料** | 「議会資料取り込んで」「議案書取り込んで」「議会資料インテーク」 | Drive `_INBOX_council/` 直接スキャン | DB経由せず即時 |
| **B. 即時取込・日常資料** | 「日常資料取り込んで」「daily取込」「INBOX_daily取込」 | Drive `_INBOX_daily/` 直接スキャン | DB経由せず即時 |
| **C. レビュー承認型**（通常運用） | 「取込確認」「Drive取込確認」「pendingレビュー」 | Notion📥Drive取込キューDB | Routineが積んだファイルを草川承認→取込 |
| **D. 手動Drive差分スキャン** | 「Drive差分スキャン」「routine止まってる」「週次Drive同期手動実行」 | Drive 15フォルダ直接 | クラウドRoutine代替→DB登録→C移行 |

## Drive構造（2026-05-21〜）

```
ROOT (1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg)
├── _INBOX_council/          1fJjS-auqrG9wKa97BPmksBJCHwFVvd_4
│   └── _processed_2026-05/  1sEFF8xsjWhoWuh52WZ9_8a49-3tw7v8F
├── _INBOX_daily/            ※草川リネーム後発効（旧_INBOX_新規投函）
│   └── _processed_<YYYY-MM>/
├── 議会資料アーカイブ/        ※草川リネーム後発効（旧議事録（年度別））
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

## モードA/B: 即時取込フロー

### Step 1: 投函フォルダ中身リスト
- モードA: `parentId = '1fJjS-auqrG9wKa97BPmksBJCHwFVvd_4'` (_INBOX_council)
- モードB: `parentId = '<_INBOX_daily ID>'` (リネーム後)

ファイル名 README* 始まりと `[DONE_*` で始まるファイルは除外（取込済）。0件なら「投函済資料なし」で終了。

### Step 2: ローカルDL
```
mcp__claude_ai_Google_Drive__download_file_content (fileId: <ID>)
```
base64取得 → 配置:
- モードA: `99_raw/_drive_originals/council_materials/<元名>`
- モードB: `99_raw/_drive_originals/daily/<元名>`

### Step 3: ローカルスクリプト実行
```bash
bash ~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_sync.sh
```
PDF→txt変換 → メタデータ抽出 → カテゴリ別ローカル振分。

### Step 4: Drive側自動整理（rclone必須）
```bash
bash ~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_postprocess.sh <mode>
# mode: council | daily
```
取込済ファイルを:
- 元名 → `[DONE_<YYYY-MM-DD>]_元名` にrclone moveto でリネーム＋move
- 移動先: `_INBOX_council/_processed_<YYYY-MM>/` or `_INBOX_daily/_processed_<YYYY-MM>/`

rclone未設定なら：Drive側はそのまま、草川にmove依頼メッセージを表示。

### Step 5: サマリ提示
```
✅ Drive取込完了
- 取込: X件
  - 議会資料 RXX-MM_定例会/議案書: Y件
  - 日常資料 01_政策素材: Z件
- 要分類: W件 → _needs_classify/ 退避
- OCR要: V件 → _needs_ocr/ 退避
- Drive整理: rclone自動move済 / 草川手動move依頼
```

---

## モードC: レビュー承認型フロー（通常運用）

### Step 1: Notion DB から確認待ち取得
```
mcp__claude_ai_Notion__notion-fetch
  collection://5187247b-f6ea-420a-a80c-154947911f64
```
状態が「未着手」or「進行中」かつ草川判定が空のレコードを抽出。0件なら「確認待ちなし」で終了。

```
Notion DB ID: ed2d5e6a-96f9-401f-a204-c3431602de41
data_source_id: 5187247b-f6ea-420a-a80c-154947911f64
URL: https://www.notion.so/ed2d5e6a96f9401fa204c3431602de41
```

### Step 2: 草川に判定リクエスト
カテゴリ別にグルーピングして表示（議事録/市政報告/日常資料候補/未分類）。

判定方法:
- 「全部承認」: 自動分類分は推奨先に取込／未分類は別途確認
- 「1,3,5」: 番号指定で承認
- 「3 → leaflets」: 番号指定 + 配置先上書き
- 「なし」「全スキップ」: 全件スキップ
- 「保留」: 何もしない（来週再表示）

### Step 3〜4: 取込実行＋Drive整理（モードA/B Step 2〜4 と同じ）

### Step 5: Notion DB 状態更新
```
- 状態: 「完了」
- 草川判定: 「承認(取込)」/「スキップ」/「差戻し(配置先変更)」
- 差戻し配置先: 上書き指定値
- ローカル取込先: 実際の保存パス
- date:取込/判定日時:start: 今のISO datetime
- date:取込/判定日時:is_datetime: 1
```

「保留」は触らずそのまま（次週も表示）。

---

## モードD: 手動Drive差分スキャン

クラウドRoutine `weekly-drive-sync-kusagawa` (trig_016r7yNKRqVubUvCJMTzVZ98) が日曜21時JSTに自動実行している。これが動かない時のフォールバック。

### Step D-1: Notion DB の最終登録日時を確認
`mcp__claude_ai_Notion__notion-fetch` で `collection://5187247b-f6ea-420a-a80c-154947911f64` を開き、検出日時の最大値を確認。

### Step D-2: 監視15フォルダを並列スキャン

| folder_id | 表示名 |
|---|---|
| 1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg | ROOT |
| 1fJjS-auqrG9wKa97BPmksBJCHwFVvd_4 | _INBOX_council |
| 1-rm_sM2296Q0wpUiDxuxJjRDbP4heVjx | 日常資料アーカイブ |
| 1oQxIunn3nB4vMJQdEzYcFZZgk5N1d2rP | H30 |
| 1i1Ds5RkCJbt0Y7X2onRuFq6QfXvjq1kp | R01 |
| 1pvIuV4a6id8_G_uNsOS0B2DOjYcD6kB7 | R02 |
| 12ihONYcNTlDRxDqw8SEYsNs_zoLNGs9A | R03 |
| 1_vNgDKDkLiF2qL-ClYFArbzhk-vYLFQI | R04 |
| 1Jn5Y_zwqlNkH8Mo5QwblMBkPBx2i1ojd | R05 |
| 1KpNNJi5hJPeVm6ICb3iMqYL9yDH22pxH | R06 |
| 1GyCICnLFokDzl6ZK53ztCl3zcgfEV-mW | R07 |
| 1VttHwAVtaTgHT6gj1AEmYk_ZoZ9XTmLx | R08 |
| 1bhtxwXuGeMi-Y5NNlF6SPE_UQ_65Eqqz | ZZ_市政報告レポート |
| 1iIAsrd0LCS9IZ2p2hSEC6VogcPfutrX5 | ZZ_委員会・地域議事録 |
| 1VX_WYfMELB26UOwcvQ9nzQGfgjxweiLZ | ZZ_議会事務局公式OneDrive |

各クエリ: `parentId = '<folder_id>' and modifiedTime > '<最終登録日時>'`、pageSize=100、`[DONE_*` で始まるファイルは除外。

### Step D-3: 分類スクリプト
```bash
echo "$DRIVE_FILES_JSON" | python3 ~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_classify.py
```
カテゴリ: `auto_council` / `auto_reports` / `auto_daily_<sub>` / `pending` / `skipped`

### Step D-4: Notion DB登録 → モードC自動移行
`notion-create-pages` で `collection://5187247b-f6ea-420a-a80c-154947911f64` に登録後、自動的にモードC Step 1 へ遷移（草川承認フロー）。

---

## エラー処理

- Drive MCP取得失敗 → 状態「進行中」のままエラー報告
- pdftotext失敗（OCR要） → `99_raw/_needs_ocr/<sub>/` 隔離、状態「進行中」+OCR要フラグ
- 草川パート抽出が0セッション → `_drive_originals/<sub>/_text/` 残し、DB に「抽出失敗・要手動確認」コメント
- rclone未設定 or remote名不一致 → Drive整理スキップ、草川手動move依頼メッセージ表示
- 議会回次判定失敗 → `_needs_classify/` 退避＋AskUserQuestionで草川に回次入力依頼

## 関連
- 同期スクリプト本体: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_sync.sh`
- Drive後処理: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_postprocess.sh`（rclone）
- 抽出スクリプト: `_extract_kusagawa.py` / `_extract_committee.py` / `_extract_gian_metadata.py` / `_classify.py`
- Notion DB: https://www.notion.so/ed2d5e6a96f9401fa204c3431602de41
- Remote Routine: `weekly-drive-sync-kusagawa` (trig_016r7yNKRqVubUvCJMTzVZ98)
- INDEX: `~/.claude/agents/knowledge/kusagawa_archive/INDEX.md`
- 関連skill: council-mode-toggle（cron頻度切替）

## 旧スキルからの移行（2026-05-21）
- 旧 `drive-sync-review` のトリガーは全て本スキルが継承
- 旧 `council-materials-intake` のトリガーも全て本スキルが継承（フォルダはdeprecated noticeのみ残置）
- 旧 `weekly-drive-sync` は2026-05-21に drive-sync-review へ統合済 → 本スキルへ
