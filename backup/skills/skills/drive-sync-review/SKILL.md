---
name: drive-sync-review
description: 草川たくや（亀山市議会議員）が Notion `📥Drive取込キュー`DB に積まれた確認待ちファイルを承認・取込・スキップするスキル。トリガー: 「/drive-sync-review」「Drive取込確認」「取込確認」「ドライブ確認待ち」「pendingレビュー」など。リモートRoutine `weekly-drive-sync-kusagawa` が毎週日曜21時(JST)にDrive差分をNotion DBに登録 → このスキルでローカル取込実行。
---

# Drive 同期 確認待ちレビュー

## 役割
リモートRoutine `weekly-drive-sync-kusagawa`（毎週日曜21時 JST、Anthropicクラウドで実行）が Notion `📥Drive取込キュー` DB に積んだファイルを草川がレビュー・承認し、ローカルClaude Codeで実際にダウンロード→テキスト化→草川パート抽出→`kusagawa_archive/` に取り込む。

## 設計
- **クラウド側（Routine）**: Drive差分検出→Notion DB登録→Gmail通知。ローカルアクセス不可。
- **ローカル側（このスキル）**: Notion DB読み取り→草川承認→Drive MCPでダウンロード→pdftotext→草川パート抽出→`kusagawa_archive/01_council/` or `02_publications/reports/` に配置→Notion状態更新。

## トリガー語
- 「/drive-sync-review」
- 「Drive取込確認」「取込確認」
- 「ドライブ確認待ち」「pendingレビュー」
- ohayo月曜朝のレポートから草川が応答した時

---

## 実行ステップ

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
2. 配置先に応じてローカル保存：
   - 議事録: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_drive_originals/transcripts/<title>` に保存
   - 市政報告: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_drive_originals/reports/<title>` に保存
3. PDFなら `pdftotext -layout` でテキスト化
4. 議事録なら `_extract_kusagawa.py` または `_extract_committee.py` で草川パート抽出
5. 命名規則 `YYYY-MM_セッション_種別.txt` でリネーム
6. 最終配置：
   - 議事録抽出済 → `01_council/`
   - 市政報告 → `02_publications/reports/`
   - 印刷物 → `02_publications/leaflets/`
   - その他 → 指定先

```bash
# 一括処理は既存スクリプト再利用
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
