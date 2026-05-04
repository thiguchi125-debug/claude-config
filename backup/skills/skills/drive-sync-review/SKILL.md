---
name: drive-sync-review
description: 草川たくや（亀山市議会議員）が `weekly-drive-sync` で確認待ちキューに積まれたファイルを承認・取込・スキップするスキル。トリガー: 「/drive-sync-review」「Drive取込確認」「取込確認」「ドライブ確認待ち」「pendingレビュー」など。pending_review一覧を表示し、草川の応答（全部/番号/なし）を受けて該当ファイルだけ取込実行・state更新する。
---

# Drive 同期 確認待ちレビュー

## 役割
`weekly-drive-sync` が自動分類できなかった「確認待ち」ファイル群を草川にレビューしてもらい、承認分のみ取込実行する。

## トリガー語
- 「/drive-sync-review」
- 「Drive取込確認」「取込確認」
- 「ドライブ確認待ち」「pendingレビュー」
- ohayo月曜朝のレポートから草川が応答した時

---

## 実行ステップ

### Step 1: pending_review 読み込み

```bash
STATE=~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_sync_state.json
python3 -c "
import json
state = json.load(open('$STATE'))
pending = state.get('pending_review', [])
print(f'確認待ち件数: {len(pending)}')
for i, p in enumerate(pending, 1):
    print(f'  {i}. {p[\"title\"]} ({p.get(\"mimeType\", \"?\")}, {p.get(\"size\", \"?\")} bytes)')
    print(f'     drive_id: {p[\"drive_id\"]}')
    print(f'     added_at: {p.get(\"added_at\", \"?\")}')
"
```

確認待ちが0件なら「✅ 確認待ちはありません」と返して終了。

### Step 2: 草川に判定リクエスト

以下のフォーマットで一覧表示し、応答を求める：

```
📋 Drive取込 確認待ち {N}件

{i}. {title} ({mimeType}, {size}KB)
   理由: {classification_reason}
   Drive: {viewUrl}

…

判定方法:
- 「全部」: 全件取込
- 「1,3,5」: 番号指定で取込
- 「議事録」「市政報告」「leaflets」: 対象カテゴリと配置先を指定（例: 「3 → leaflets」）
- 「なし」「スキップ」: 全件スキップ（state から削除）
- 「保留」: 何もしない（次週も再表示）
```

### Step 3: 応答パース

草川の応答を解釈：
- 「全部」「all」→ 全 pending を取込候補に
- カンマ区切り数字 → 該当インデックスのみ
- 「N → category」形式 → 配置先を上書き指定
- 「なし」「skip」→ 全 pending を `skipped_files` へ移動
- 「保留」「pending」→ そのまま

### Step 4: 取込実行（承認分のみ）

承認された各ファイルについて：
1. Drive MCP `download_file_content` でローカル取得
2. 配置先に応じて：
   - 議事録: `99_raw/_drive_originals/transcripts/` → `_extract_kusagawa.py` → `01_council/`
   - 市政報告: `99_raw/_drive_originals/reports/` → `pdftotext` → `02_publications/reports/`
   - leaflets: `99_raw/_drive_originals/leaflets/` → `pdftotext` → `02_publications/leaflets/`
3. ファイル名を `YYYY-MM_*` 形式にリネーム（年月推定可能なら）

```bash
# 議事録系なら既存スクリプト再利用
bash ~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_sync.sh
```

### Step 5: state 更新

```python
# pending から取込分を削除→auto_imported へ移動
# スキップ分は skipped_files へ移動
# 保留分はそのまま pending_review に残す
state['history'].append({
    'ts': now,
    'action': 'manual_review',
    'approved': len(approved),
    'skipped': len(skipped),
    'kept_pending': len(kept),
})
```

### Step 6: 結果報告

草川に報告：

```
✅ 取込完了: {N}件
  議事録 → 01_council/: {n_council}件
  市政報告 → 02_publications/reports/: {n_reports}件
  leaflets → 02_publications/leaflets/: {n_leaflets}件

⏭ スキップ: {M}件
⏸ 保留（来週再表示）: {K}件

学習層に反映済み。次のブログ・SNS生成時から grep 対象になります。
```

### Step 7: Discord 通知（任意）

完了内容を Discord にも投稿（モバイル確認用）。

---

## 関連ファイル
- 状態DB: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_sync_state.json`
- 同期スクリプト: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_sync.sh`

## 関連スキル
- `weekly-drive-sync`: 週次自動取込（このスキルの上流）
- `ohayo`: 月曜朝に確認待ち件数を表示
