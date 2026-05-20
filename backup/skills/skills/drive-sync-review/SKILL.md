---
name: drive-sync-review
description: 草川たくや（亀山市議会議員）が Notion `📥Drive取込キュー`DB に積まれた確認待ちファイルを承認・取込・スキップするスキル。トリガー: 「/drive-sync-review」「Drive取込確認」「取込確認」「ドライブ確認待ち」「pendingレビュー」「週次Drive同期手動実行」「Drive差分手動スキャン」「routineが動いてない」など。通常はリモートRoutine `weekly-drive-sync-kusagawa` が毎週日曜21時(JST)にDrive差分をNotion DBに登録 → このスキルでローカル取込実行。クラウドRoutine不調時はモードB（手動Drive差分スキャン）にフォールバック可能。
---

# Drive 同期 確認待ちレビュー

## 役割
リモートRoutine `weekly-drive-sync-kusagawa`（毎週日曜21時 JST、Anthropicクラウドで実行）が Notion `📥Drive取込キュー` DB に積んだファイルを草川がレビュー・承認し、ローカルClaude Codeで実際にダウンロード→テキスト化→草川パート抽出→`kusagawa_archive/` に取り込む。

## 設計
- **クラウド側（Routine）**: Drive差分検出→Notion DB登録→Gmail通知。ローカルアクセス不可。
- **ローカル側（このスキル）**: Notion DB読み取り→草川承認→Drive MCPでダウンロード→pdftotext→草川パート抽出→`kusagawa_archive/01_council/` or `02_publications/reports/` に配置→Notion状態更新。

## トリガー語

### モードA: 通常レビュー（クラウドRoutineが正常動作している前提）
- 「/drive-sync-review」
- 「Drive取込確認」「取込確認」
- 「ドライブ確認待ち」「pendingレビュー」
- ohayo月曜朝のレポートから草川が応答した時

### モードB: 手動Drive差分スキャン（クラウドRoutine不調時のフォールバック）
- 「週次Drive同期手動実行」「Drive差分手動スキャン」
- 「routineが動いてない」「routine止まってる」
- 「緊急で議会後すぐ取込みたい」
- 旧 `weekly-drive-sync` skill 統合済み（2026-05-21）

---

## 実行ステップ（モードA: 通常レビュー）

### Step 1: Notion DB から確認待ち取得

`mcp__claude_ai_Notion__notion-fetch` で `collection://5187247b-f6ea-420a-a80c-154947911f64` を開く。

状態が「未着手」or「進行中」かつ草川判定が空のレコードを抽出。

```
Notion DB ID: ed2d5e6a-96f9-401f-a204-c3431602de41
data_source_id: 5187247b-f6ea-420a-a80c-154947911f64
URL: https://www.notion.so/ed2d5e6a96f9401fa204c3431602de41
```

確認待ち0件なら「✅ 確認待ちはありません」と返して終了。

### Step 2: 草川に判定リクエスト

カテゴリ別にグルーピングして表示：

```
📋 Drive取込 確認待ち {N}件

【自動分類: 議事録 → 01_council/】 {n_council}件
1. {title} ({mimeType}, {sizeKB}KB) [{親フォルダ}]
   分類理由: {分類理由}
   Drive: {DriveURL}

【自動分類: 市政報告 → 02_publications/reports/】 {n_reports}件
2. {title} ({mimeType}, {sizeKB}KB)
...

【未分類（要判定）】 {n_pending}件
3. {title} ({mimeType}, {sizeKB}KB)
   配置先候補: 議事録/市政報告/印刷物/ブログ/コンパス/原本のみ
...

判定方法:
- 「全部承認」: 自動分類分は推奨先に取込／未分類は別途確認
- 「1,3,5」: 番号指定で承認
- 「3 → leaflets」: 番号指定 + 配置先上書き（未分類用）
- 「なし」「全スキップ」: 全件スキップ
- 「保留」: 何もしない（来週再表示）
```

### Step 3: 応答パース

草川の応答を解釈：
- 「全部承認」「all」→ 自動分類分は全部、未分類分は個別確認
- カンマ区切り数字 → 該当インデックスのみ
- 「N → category」形式 → 配置先上書き指定
- 「なし」「skip」→ 全 pending を スキップ
- 「保留」「pending」→ そのまま

### Step 4: 取込実行（承認分のみ）

各承認ファイルについて：

1. Drive MCP `mcp__claude_ai_Google_Drive__download_file_content` でローカル取得
   - PDFなら base64 → ローカル保存
   - Google Docsなら `read_file_content` で text 取得
2. 配置先に応じて `99_raw/_drive_originals/<sub>/` に原本保存：
   - 議事録 → `transcripts/`
   - 市政報告 → `reports/`
   - 印刷物 → `leaflets/`
   - 政策資料 → `resources/`
   - 選挙関連 → `election/`
3. PDFなら `pdftotext -layout` でテキスト化
4. **議事録のみ** `_extract_kusagawa.py` または `_extract_committee.py` で草川パート抽出
5. 命名規則 `YYYY-MM_<キーワード>.txt` でリネーム（推測可能な場合）
6. 最終配置（取込先4階層に対応）：
   - 議事録抽出済 → `01_council/`
   - 市政報告 → `02_publications/reports/`
   - 印刷物 → `02_publications/leaflets/`
   - 政策資料 → `05_resources/`
   - 選挙関連 → `06_election/`
   - 草川判定で配置先上書きされた場合 → 該当先

```bash
# 一括処理は既存スクリプト再利用（拡張版）
bash ~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_sync.sh
```

### Step 5: Notion DB 状態更新

各処理済みファイルに `mcp__claude_ai_Notion__notion-update-page` で更新：

```
- 状態: 「完了」
- 草川判定: 「承認(取込)」 or 「スキップ」 or 「差戻し(配置先変更)」
- 差戻し配置先: 上書き指定があれば該当値
- ローカル取込先: 実際の保存パス（例: 01_council/2026-04_R0804_本会議議事録_kusagawa.txt）
- date:取込/判定日時:start: 今のISO datetime
- date:取込/判定日時:is_datetime: 1
```

「保留」は触らずにそのまま（次週も表示される）。

### Step 6: 結果報告

草川に報告：

```
✅ 取込完了: {N}件
  議事録 → 01_council/: {n_council}件
  市政報告 → 02_publications/reports/: {n_reports}件
  印刷物 → 02_publications/leaflets/: {n_leaflets}件

⏭ スキップ: {M}件
⏸ 保留（来週再表示）: {K}件

学習層に反映済み。次のブログ・SNS生成時から grep 対象になります。
INDEXファイル件数: {更新後の件数}
```

---

## 実行ステップ（モードB: 手動Drive差分スキャン）

> このモードは**通常は手動実行不要**。リモートRoutine `weekly-drive-sync-kusagawa` (trig_016r7yNKRqVubUvCJMTzVZ98) が毎週日曜21:00 JSTに自動実行している。
>
> モードBが必要なケース：
> - Routineが何らかの理由で実行されなかった
> - 緊急で議会後すぐ取込みたい
> - 手動でDrive差分を確認したい
>
> 旧 `weekly-drive-sync` skill (2026-05-05〜2026-05-21) のフローを統合。

### Step B-1: Notion DB の最終登録日時を確認

`mcp__claude_ai_Notion__notion-fetch` で `collection://5187247b-f6ea-420a-a80c-154947911f64` を開き、検出日時の最大値を確認。

例: 最終登録 2026-04-27T12:00:00Z → これ以降の Drive 差分をスキャン。

### Step B-2: Drive 差分スキャン

Drive MCP `mcp__claude_ai_Google_Drive__search_files` を以下15フォルダに対して並列実行：

| folder_id | 表示名 |
|---|---|
| 1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg | ROOT |
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
| 1RkDuAFY64-VgVDO43IHNo8_eurLtBi5T | ZZ_政策別深掘り |
| 1VX_WYfMELB26UOwcvQ9nzQGfgjxweiLZ | ZZ_議会事務局公式OneDrive |
| 1mNHzaHx9CxrDAHyMnq3K5EBqMRrTM4au | ZZ_ブログSNS全アーカイブ |

各フォルダのクエリ:
```
parentId = '<folder_id>' and modifiedTime > '<最終登録日時>'
```

pageSize: 100, excludeContentSnippets: true。

### Step B-3: ファイル名パターン分類

`~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_classify.py` で分類：

```bash
echo "$DRIVE_FILES_JSON" | python3 ~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_classify.py
```

カテゴリ：
- `auto_council`: 議事録（kaigiroku/議事録/委員会/通告書 等）
- `auto_reports`: 市政報告（市政報告/号外/地区版/ニュース 等）
- `pending`: パターン外（未分類・草川判定待ち）
- `skipped`: テンプレ・草案・私的・mime非対応

### Step B-4: Notion DB 登録

`mcp__claude_ai_Notion__notion-create-pages` で `collection://5187247b-f6ea-420a-a80c-154947911f64` に登録：

**注意**: skipped はDB登録しない（ログのみ）。auto_council / auto_reports / pending を登録。

properties:
- ファイル名: <Drive title>
- DriveID: <Drive file id>
- DriveURL: <viewUrl>
- 親フォルダ: <フォルダ表示名>
- MIMEタイプ: PDF/docx/gdoc/txt/png/zip/その他
- サイズKB: <fileSize/1024>
- 推奨カテゴリ: 議事録(01_council) / 市政報告(02_publications/reports) / 未分類
- 分類理由: 一致したパターン名 or 'no pattern match'
- 状態: 未着手
- date:検出日時:start: 今のISO datetime
- date:検出日時:is_datetime: 1

### Step B-5: 完了サマリ提示

```
✅ 手動Drive同期 完了
スキャン対象: 15フォルダ
新規ファイル: {N}件
  議事録自動登録: {n_council}件
  市政報告自動登録: {n_reports}件
  未分類(要判定): {n_pending}件
  自動スキップ: {n_skipped}件

次のアクション: 「/drive-sync-review」モードA を実行して取込判定
Notion DB: https://www.notion.so/ed2d5e6a96f9401fa204c3431602de41
```

その後、自動的にモードA Step 1 に移行（草川承認フロー）。

---

## エラー処理

- Drive MCP取得失敗 → 該当ファイルの状態を「進行中」のまま残し、エラー内容を草川に報告
- pdftotext失敗（OCR要） → `99_raw/_needs_ocr/<sub>/` に隔離、Notion状態を「進行中」のままにしてOCR要フラグ
- 草川パート抽出が0セッション → `99_raw/_drive_originals/<sub>/_text/` に残し、Notion DB に「抽出失敗・要手動確認」のコメント

## 関連ファイル
- Notion DB: https://www.notion.so/ed2d5e6a96f9401fa204c3431602de41 (`📥Drive取込キュー`)
- 同期スクリプト: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_sync.sh`
- 抽出スクリプト: `_extract_kusagawa.py` / `_extract_committee.py`
- INDEX: `~/.claude/agents/knowledge/kusagawa_archive/INDEX.md`

## 関連リソース
- Remote Routine: `weekly-drive-sync-kusagawa` (trig_016r7yNKRqVubUvCJMTzVZ98) — 毎週日曜21:00 JST
  - URL: https://claude.ai/code/routines/trig_016r7yNKRqVubUvCJMTzVZ98
- ohayo: 月曜朝に取込結果サマリ表示（このスキルへのリンク付き）
