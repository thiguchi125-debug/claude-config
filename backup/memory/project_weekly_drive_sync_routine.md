---
name: 週次Drive同期ルーティン構築
description: 草川議会質問アーカイブのDrive→ローカル取込を半自動化したハイブリッド構造（クラウドRoutine＋Notion DB＋ローカルスキル2本）
type: project
originSessionId: c51d25d3-bac9-4389-a011-c69108f135b0
---
# 週次 Drive 同期ルーティン（2026-05-04 構築完了）

## 構造（ハイブリッド方式）

```
[毎週日曜21:00 JST]
        ↓
[クラウドRoutine: weekly-drive-sync-kusagawa]
  ├─ Drive 15フォルダ並列スキャン (modifiedTime差分)
  ├─ ファイル名パターンで自動分類（議事録/市政報告/未分類/スキップ）
  ├─ Notion `📥Drive取込キュー`DB に登録
  └─ Gmail下書きで草川に通知（N件検出・確認待ちM件）
        ↓
[月曜朝 ohayo]
  └─ 月曜セクションX-2「📚 先週のDriveアーカイブ同期」
     - 自動分類済N件・未分類M件を表示
     - /drive-sync-review への導線
        ↓
[草川がClaude Code開く]
  └─ 「/drive-sync-review」を実行
     ├─ Notion DB から確認待ち取得
     ├─ カテゴリ別に表示・草川判定（全部/番号/差戻し/スキップ）
     ├─ 承認分を Drive MCP でダウンロード
     ├─ pdftotext → 草川パート抽出 (_extract_kusagawa.py / _extract_committee.py)
     ├─ 命名規則統一して 01_council/ or 02_publications/reports/ に配置
     └─ Notion DB の状態を「完了」に更新
```

## なぜハイブリッド？
- リモートRoutineはAnthropicクラウドで動くため**ユーザーのMacにアクセスできない**
- ローカルファイル取込・Discord通知はローカルClaude Codeでないと不可能
- → クラウド側はメタ管理（差分検出・DB登録・通知）／ローカル側は実体取込（DL・抽出・配置）に役割分離

## リソース

### Notion DB
- **DB名**: `📥Drive取込キュー`
- **DB URL**: https://www.notion.so/ed2d5e6a96f9401fa204c3431602de41
- **data_source_id**: `5187247b-f6ea-420a-a80c-154947911f64`
- **親ハブ**: `📚 草川議会質問アーカイブ Driveミラー` (356cf503-a68f-814c-9997-ef56a3cca376)
- **17フィールド**: ファイル名/受付ID(DRV-)/DriveID/DriveURL/親フォルダ/MIMEタイプ/サイズKB/推奨カテゴリ/分類理由/状態/草川判定/差戻し配置先/ローカル取込先/検出日時/取込・判定日時/更新日時

### Remote Routine
- **trigger_id**: `trig_016r7yNKRqVubUvCJMTzVZ98`
- **管理URL**: https://claude.ai/code/routines/trig_016r7yNKRqVubUvCJMTzVZ98
- **cron**: `0 12 * * 0` (UTC) = 毎週日曜21:00 JST
- **MCP接続**: Google Drive + Notion
- **モデル**: claude-sonnet-4-6
- **次回実行**: 2026-05-10T12:00:00Z (= 2026-05-10 21:00 JST)

### ローカルスキル
- `weekly-drive-sync` (手動実行用フォールバック)
- `drive-sync-review` (草川承認＆ローカル取込)
- `ohayo` 月曜セクションX-2 (取込結果サマリ表示)

### ローカルスクリプト
- `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_classify.py` (ファイル名分類)
- `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_drive_sync.sh` (取込パイプライン)
- `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_extract_kusagawa.py` (本会議草川パート抽出)
- `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_extract_committee.py` (委員会草川パート抽出)

## 分類ルール（_classify.py 準拠）

### 自動取込: 議事録(01_council)
タイトルに含む: kaigiroku/議事録/会議録/委員会/本会議/定例会/通告書/一般質問/代表質問/代表質疑/議案質疑/総括質疑/予算決算/決算委員会/総合計画
正規表現: `^[Rr]\d+\.\d+` `^[Rr]\d{4}` `^\d{3,4}\.pdf$` `^令和[\d０-９]+年`

### 自動取込: 市政報告(02_publications/reports)
タイトルに含む: 市政報告/市政レポート/号外/地区版/ニュース/チラシ/昼生/二本松/みずきが丘/けんろう/菅内/御幸/東部/南部/下庄/田村/出屋/川崎/井田川/神辺/城東/北東

### 自動スキップ
タイトルに含む: テンプレ/テンプレート/草案/下書き/private/個人/非公開/指示書/アシスタント/.DS_Store/`~$`
MIME: audio/* video/* image/*

### それ以外
→ 未分類（草川判定待ち）

## How to apply
- Routineは自動実行。草川は月曜朝のohayoブリーフィングで「先週のDrive同期」を確認するだけ
- 確認待ちが0件なら何もしない、ある場合のみ `/drive-sync-review` を起動
- Routine失敗時はohayoが警告、`/weekly-drive-sync` 手動実行で代替
- 新しいファイル名パターンが頻出したら `_classify.py` のCOUNCIL_PATTERNS / REPORT_PATTERNS / SKIP_PATTERNSに追加

## トラブルシューティング
- Routineが動かない → https://claude.ai/code/routines/trig_016r7yNKRqVubUvCJMTzVZ98 で実行履歴確認
- Gmail通知届かない → Routine内でGmail MCP接続失敗の可能性。Notion DBには記録されているはずなので /drive-sync-review で確認
- 同じファイルが何度もキューに登録される → Notion DB既登録チェックロジックに問題、Routineプロンプト調整要
