---
name: council-materials-intake
description: 草川たくや（亀山市議会議員）がSideBooks/議会クラウドからDLしてGoogle Drive `_INBOX_新規投函/_council_pending/` に投函した議会資料（議案書・委員会資料・行政報告・通告書等）を、ローカル `kusagawa_archive/` に取り込んでメタデータ付与＋振分するスキル。トリガー: 「議会資料取り込んで」「議会資料インテーク」「council-materials-intake」「議会資料の取込」「議案書取り込んで」「議会資料同期」等。リモートRoutineが日次/週次で自動同期する裏で、緊急時の即時取込を担う。
---

# 議会資料インテーク

## 役割
Drive `_INBOX_新規投函/_council_pending/`（ID: 1Uk2yabgrJCz56KQP1i2AThGTAMGKKh-l）に投函された議会資料PDFを、緊急時に即時で：
1. Drive MCP でDL → ローカル `99_raw/_drive_originals/council_materials/` 配置
2. `_drive_sync.sh` で pdftotext + メタデータ抽出 + 振分
3. Drive側も `_council_pending/` から `議事録（年度別）/RXX/MM_定例会/種別/` へ自動振分（copy）
4. 結果サマリを草川に提示

## トリガー語
- 「議会資料取り込んで」「議案書取り込んで」
- 「議会資料インテーク」「council-materials-intake」
- 「議会資料の取込」「議会資料同期」
- 議会前夜・委員会前夜の草川判断起動

## 実行ステップ

### Step 1: Drive `_council_pending` の中身をリスト
```
mcp__claude_ai_Google_Drive__search_files
  query: parentId = '1Uk2yabgrJCz56KQP1i2AThGTAMGKKh-l' and mimeType != 'application/vnd.google-apps.folder'
  pageSize: 50
```
README_ここに議会資料を投函.md は除外。0件なら「投函済議会資料なし」と返して終了。

### Step 2: 各PDFをローカルDL
```
mcp__claude_ai_Google_Drive__download_file_content
  fileId: <PDF_ID>
```
取得した base64 を `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_drive_originals/council_materials/<元ファイル名>` に書き出す。

### Step 3: ローカルスクリプト実行
```bash
bash ~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_sync.sh
```
pdftotext で `_text/` に txt 変換 → `_extract_gian_metadata.py` でYAMLメタ抽出 → `01_council/RXX-MM_定例会/<種別>/` に配置。`unknown` 判定は `01_council/_needs_classify/` 退避。

### Step 4: Drive 側の振分
各PDFについて、抽出された議会回次（RXX-MM）と種別から **振分先 Drive フォルダID** を選択：

| 種別 | R08-03 振分先（フォルダID） |
|---|---|
| 議案書 | 1-_1Ew1OmCYPOM7lS7ddWty-tG0QI8blV |
| 委員会資料 | 1TRW2gfX3jWCqguu_LBP_-buf9jHVAaFS |
| 行政報告 | 139u0DzNQYI6ZQTfulvGOjeWwDXuGoxHe |
| 議事録 | 1VBAQkbsLMIjesYGzk6Y6v6PnHEY5_Akt |
| 草川質問 | 1uruyEpOcrjrssiEELllMOtC1P-K0ywTM |

R08-06以降は親フォルダ配下に同名サブを自動 `create_file (mimeType: folder)` で作成。

Drive MCPに `move_file` 機能無いため：
```
mcp__claude_ai_Google_Drive__copy_file
  fileId: <PDF_ID>
  parentId: <振分先フォルダID>
  title: <元ファイル名>
```
copy成功後、`_council_pending/` 内の原本は草川に手動削除を依頼（または `_council_pending/_processed/` サブを作って移動扱いにする運用）。

### Step 5: サマリ提示
```
✅ 議会資料インテーク完了
- 取込: X件
  - R08-03_定例会/議案書: Y件
  - R08-03_定例会/委員会資料: Z件
- 要分類（_needs_classify）: W件 → 草川判定待ち
- OCR要: V件 → _needs_ocr/ に退避
- Drive振分: U件copy済 → 草川は _council_pending/ 内の原本を削除可能
```

## 失敗時のフォールバック
- pdftotext失敗（画像PDF）: `_needs_ocr/` 退避＋OCR要件数を表示
- 議会回次判定失敗: `_needs_classify/` 退避＋AskUserQuestionで草川に回次入力依頼
- Drive書込権限エラー: ローカルだけ取込完了、Drive側はsupplemental task登録

## 関連
- 設計書: `~/.claude/projects/-Users-kusakawatakuya/specs/2026-05-11-council-materials-management-design.md`
- 進行PJ: `~/.claude/projects/-Users-kusakawatakuya/memory/project_council_materials_management.md`
- 既存pipeline: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_sync.sh`
- 抽出スクリプト: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_extract_gian_metadata.py`
