---
name: weekly-drive-sync
description: 草川たくや（亀山市議会議員）の議会質問アーカイブをDriveからローカルへ取り込むワークフローのドキュメント＆手動実行スキル。本来は毎週日曜21時(JST)にリモートRoutine `weekly-drive-sync-kusagawa` (trig_016r7yNKRqVubUvCJMTzVZ98)が自動実行する → Notion `📥Drive取込キュー` DBに登録 → 翌月曜にローカル `/drive-sync-review` で取込。トリガー: 「週次Drive同期手動実行」「Drive差分手動スキャン」「routineが動いてない」「weekly-drive-sync」など。
---

# 週次 Google Drive 同期（手動実行版）

## 通常運用
このスキルは**通常は手動実行不要**です。リモートRoutineが自動で同じ処理を実行しています：

- **Routine ID**: `trig_016r7yNKRqVubUvCJMTzVZ98`
- **実行スケジュール**: 毎週日曜 21:00 JST (= 12:00 UTC)
- **管理URL**: https://claude.ai/code/routines/trig_016r7yNKRqVubUvCJMTzVZ98
- **動作**: Drive差分検出→ファイル名分類→Notion `📥Drive取込キュー` DB登録→Gmail通知

このローカルスキルは**手動実行用のフォールバック**です：
- Routineが何らかの理由で実行されなかった
- 緊急で議会後すぐ取込みたい
- 手動でDrive差分を確認したい

## 設計思想（参考）
- **Drive = 受信箱**: 草川がブラウザ・モバイルから原本を投げ込む
- **Notion DB = 取込キュー**: クラウドRoutineが差分検出して登録、草川判定待ち
- **ローカル = 学習層**: ローカル `/drive-sync-review` で実取込→`kusagawa_archive/` に保管
- **役割分離**: クラウド=メタ管理／ローカル=実体取込

---

## 手動実行ステップ

### Step 1: Notion DB の最終登録日時を確認

`mcp__claude_ai_Notion__notion-fetch` で `collection://5187247b-f6ea-420a-a80c-154947911f64` を開き、検出日時の最大値を確認。

例: 最終登録 2026-04-27T12:00:00Z → これ以降の Drive 差分をスキャン。

### Step 2: Drive 差分スキャン

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

### Step 3: ファイル名パターン分類

`~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_classify.py` で分類：

```bash
echo "$DRIVE_FILES_JSON" | python3 ~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_classify.py
```

カテゴリ：
- `auto_council`: 議事録（kaigiroku/議事録/委員会/通告書 等）
- `auto_reports`: 市政報告（市政報告/号外/地区版/ニュース 等）
- `pending`: パターン外（未分類・草川判定待ち）
- `skipped`: テンプレ・草案・私的・mime非対応

### Step 4: Notion DB 登録

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

### Step 5: 草川に通知

通常Routine実行時はGmail下書き作成だが、手動実行時は実行画面で結果を直接表示してOK。

```
✅ 手動Drive同期 完了
スキャン対象: 15フォルダ
新規ファイル: {N}件
  議事録自動登録: {n_council}件
  市政報告自動登録: {n_reports}件
  未分類(要判定): {n_pending}件
  自動スキップ: {n_skipped}件

次のアクション: 「/drive-sync-review」を実行して取込判定
Notion DB: https://www.notion.so/ed2d5e6a96f9401fa204c3431602de41
```

---

## 関連リソース

### Notion
- 📥Drive取込キューDB: https://www.notion.so/ed2d5e6a96f9401fa204c3431602de41
- 📚 草川議会質問アーカイブ Driveミラーハブ: https://www.notion.so/356cf503a68f814c9997ef56a3cca376

### Remote Routine
- weekly-drive-sync-kusagawa: https://claude.ai/code/routines/trig_016r7yNKRqVubUvCJMTzVZ98

### ローカルスクリプト
- 分類ロジック: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_classify.py`
- 同期スクリプト: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_sync.sh`
- 抽出スクリプト: `_extract_kusagawa.py` / `_extract_committee.py`
- INDEX: `~/.claude/agents/knowledge/kusagawa_archive/INDEX.md`

### 関連スキル
- `drive-sync-review`: 草川手動承認＆ローカル取込（このスキルの後段）
- `ohayo`: 月曜朝に取込結果サマリ表示
