---
name: weekly-drive-sync
description: 草川たくや（亀山市議会議員）の議会質問アーカイブを週1回（毎週日曜21時 cron実行）Google Driveから差分取得し、ファイル名パターンで自動分類して `~/.claude/agents/knowledge/kusagawa_archive/` 配下に取り込むルーティン。議事録・市政報告レポートは自動取込、それ以外（草案・テンプレ・私的資料）は確認待ちキューに積みDiscordで草川に通知する。トリガー: 「週次Drive同期」「Drive取込」「weekly-drive-sync」「drive-sync」または cron 自動起動。手動承認は別スキル `drive-sync-review` を使う。
---

# 週次 Google Drive 同期スキル

## 役割
草川たくやの議会発言・市政報告レポート・印刷物原稿を保管している Google Drive の **`1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg`** ルートフォルダを毎週1回スキャンし、新規ファイルを自動分類してローカル学習層 `~/.claude/agents/knowledge/kusagawa_archive/` に取り込む。

## 設計思想
- **Drive = 受信箱（草川がブラウザ・モバイルから原本を投げ込む場所）**
- **ローカル = Claude の学習層（grep最適化された高速検索DB）**
- **このスキル = Drive→ローカルの差分自動同期パイプライン**

---

## 実行ステップ

### Step 1: 状態DB読み込み
`~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_sync_state.json` を読み、`last_sync_at` と既存 `auto_imported`（重複防止用）を取得。

```bash
STATE=~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_sync_state.json
LAST_SYNC=$(python3 -c "import json; print(json.load(open('$STATE'))['last_sync_at'])")
echo "前回同期: $LAST_SYNC"
```

### Step 2: Drive 差分スキャン

Drive MCP `mcp__claude_ai_Google_Drive__search_files` で以下のクエリを並列実行：

各年度フォルダ＋ZZ系フォルダ＋ルートで `modifiedTime > '<LAST_SYNC>'` を検索。
folder_id 一覧は `99_raw/_drive_originals/_INTAKE_REPORT.md` 参照。

```python
# 主要folder_id（並列スキャン対象）
FOLDERS = {
    "1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg": "ROOT",
    "1oQxIunn3nB4vMJQdEzYcFZZgk5N1d2rP": "H30",
    "1i1Ds5RkCJbt0Y7X2onRuFq6QfXvjq1kp": "R01",
    "1pvIuV4a6id8_G_uNsOS0B2DOjYcD6kB7": "R02",
    "12ihONYcNTlDRxDqw8SEYsNs_zoLNGs9A": "R03",
    "1_vNgDKDkLiF2qL-ClYFArbzhk-vYLFQI": "R04",
    "1Jn5Y_zwqlNkH8Mo5QwblMBkPBx2i1ojd": "R05",
    "1KpNNJi5hJPeVm6ICb3iMqYL9yDH22pxH": "R06",
    "1GyCICnLFokDzl6ZK53ztCl3zcgfEV-mW": "R07",
    "1VttHwAVtaTgHT6gj1AEmYk_ZoZ9XTmLx": "R08",
    "1bhtxwXuGeMi-Y5NNlF6SPE_UQ_65Eqqz": "ZZ_市政報告レポート",
    "1iIAsrd0LCS9IZ2p2hSEC6VogcPfutrX5": "ZZ_委員会・地域議事録",
    "1RkDuAFY64-VgVDO43IHNo8_eurLtBi5T": "ZZ_政策別深掘り",
    "1VX_WYfMELB26UOwcvQ9nzQGfgjxweiLZ": "ZZ_議会事務局公式OneDrive",
    "1mNHzaHx9CxrDAHyMnq3K5EBqMRrTM4au": "ZZ_ブログSNS全アーカイブ",
}
```

各フォルダで:
- query: `parentId = '<folder_id>' and modifiedTime > '<LAST_SYNC>'`
- pageSize: 100
- excludeContentSnippets: true

並列15フォルダ取得 → 結果集約。

### Step 3: 重複除外＋分類

取得した全ファイルを以下で処理：
1. 既存 `auto_imported` のtitleと突合 → 重複を除外
2. `_classify.py` で分類

```bash
echo "$DRIVE_FILES_JSON" | python3 ~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_classify.py > /tmp/classified.json
```

カテゴリ：
- `auto_council`: 議事録パターン（kaigiroku/議事録/委員会/通告書 等）→ **自動取込**
- `auto_reports`: 市政報告パターン（市政報告/号外/地区版/ニュース 等）→ **自動取込**
- `pending`: パターン外 → **確認待ち（草川にDiscordで問いかけ）**
- `skipped`: テンプレ・草案・私的・mime非対応 → **自動スキップ（履歴のみ残す）**

### Step 4: 自動取込実行

`auto_council` と `auto_reports` の各ファイルを：
1. Drive MCP `download_file_content` で取得（Google Docsは `read_file_content` でtxtエクスポート）
2. ローカル `99_raw/_drive_originals/<sub>/` に保存
3. PDFなら `pdftotext -layout` でテキスト化
4. 議事録なら `_extract_kusagawa.py` または `_extract_committee.py` で草川パート抽出
5. 命名規則 `YYYY-MM_セッション_種別.txt` でリネームしつつ最終配置：
   - 議事録 → `01_council/`
   - 市政報告 → `02_publications/reports/`

```bash
# 既存 _drive_sync.sh を呼び出すのが最も確実
bash ~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_sync.sh
```

### Step 5: pending を state に追加

`pending` バケットの各ファイルを `_sync_state.json` の `pending_review` に追加（drive_id, title, mimeType, size, suggested_category=null, added_at）。

### Step 6: state 更新

```python
state['last_sync_at'] = datetime.now(timezone.utc).isoformat()
state['auto_imported'].extend([{...} for f in auto_council + auto_reports])
state['pending_review'].extend([{...} for f in pending])
state['skipped_files'].extend([{...} for f in skipped])
state['history'].append({
    'ts': now,
    'action': 'weekly_sync',
    'auto_count': len(auto_council) + len(auto_reports),
    'pending_count': len(pending),
    'skipped_count': len(skipped),
})
```

### Step 7: Discord 通知

Discord MCP `mcp__plugin_discord_discord__reply` で草川に結果通知。

通知フォーマット：

```
📚 週次Drive同期 完了 ({YYYY-MM-DD HH:MM})

✅ 自動取込: {N}件
  議事録 ({n_council}): {file1.title}, {file2.title}, ...
  市政報告 ({n_reports}): {file3.title}, ...

❓ 確認待ち: {M}件
  1. {pending1.title} ({mimeType})
  2. {pending2.title} ({mimeType})
  ...

⏭ 自動スキップ: {K}件（テンプレ/草案/mime非対応）

🔍 確認待ち分の判定は次のClaude Codeセッションで `/drive-sync-review` を実行してください。
全部取り込みたい場合は「全部」、選別する場合は「1,3,5」、保留は「なし」と返してください。
```

長文になる場合は Discord embed 機能 or 2-3メッセージに分割。

確認待ちが0件の場合は「✅ 全件自動取込済」のみ通知。
何も新規がなかった場合は「📭 新規ファイルなし」のみ通知（短く）。

### Step 8: state.json をディスクに保存

```bash
python3 -c "
import json
state = {...}  # Step 6で構築
json.dump(state, open('$STATE', 'w'), ensure_ascii=False, indent=2)
"
```

---

## 失敗時の挙動
- Drive MCP が失敗 → state 更新せず、Discord に「Drive スキャン失敗。手動で `_drive_sync.sh` を実行してください」と通知
- pdftotext 失敗（OCR要） → `99_raw/_needs_ocr/<sub>/` に隔離、Discord通知に「OCR要N件」を明記
- 草川パート抽出が0セッション → `99_raw/_drive_originals/<sub>/_text/` に残し、ローカル統合スキップ。確認待ちに追加。

## 関連ファイル
- 状態DB: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_sync_state.json`
- 分類ロジック: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_classify.py`
- 同期スクリプト: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_sync.sh`
- 抽出スクリプト: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_extract_kusagawa.py`, `_extract_committee.py`
- INDEX: `~/.claude/agents/knowledge/kusagawa_archive/INDEX.md`

## 関連スキル
- `drive-sync-review`: 草川手動承認用（pending_review消化）
- `ohayo`: 月曜朝に取込結果サマリ表示
