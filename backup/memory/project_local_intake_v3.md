---
name: ローカル資料921件取込v3構造
description: 2026-05-05実施。~/Documents/政治活動・市議会・政策・2026senkyo・選挙・サロン活動・kameyama-research・Creative Cloud市政報告・Desktop直近・直下PDF 計921件(5.1GB)をテキスト化してkusagawa_archive/に統合。新カテゴリ05_resources/06_election追加で学習層を301→1088件に拡大
type: project
originSessionId: c51d25d3-bac9-4389-a011-c69108f135b0
---
# ローカル資料 大量取込（2026-05-05）

## 背景
草川議員の選挙準備（2026-10-25投票）に向けて、ローカルPC内の過去政策資料・議会資料を漏れなくClaude Code学習層に統合。Drive取込ルーティン（毎週日曜21時）と並行して、既にローカルに散在していた8年分の議員業務蓄積を1パスで取り込んだ。

## 取込対象と除外（草川判断）

### 取込（921件 / 5.1GB → 794件変換成功）
- ~/Documents/政治活動/{2023年以前資料,2024年,2025年,★VIP} 260件
- ~/Documents/市議会・政策/{2023〜2025年,通告書様式,定期監査資料} 510件
- ~/Documents/2026senkyo/ 1件
- ~/Documents/選挙/ 6件
- ~/Documents/サロン活動/ 5件
- ~/Documents/kameyama-research/ 1件
- ~/Documents/直下PDF（総合計画案・要望書系）9件
- ~/Desktop/議員業務PDF/docx 22件
- ~/Documents/Creative Cloud Files/.../市政報告レポート/ 113件
- ~/Documents/Creative Cloud Files/.../選挙チラシ/ 1件

### 除外（選挙無関係 or プライベート）
- 三重大応援団（大学時代）
- 草川家（プライベート）
- 亀山青年会議所/三重パラ陸協/亀山社中/飲食業組合/消防団/昼生小PTA（関連団体）
- eスポーツ/League of Legends/superwhisper（趣味）
- ObsidianVault（別管理）
- OneDrive/亀山市議会（議会事務局公式・既Drive取込分で十分）

## 変換結果
- **OK: 794件**（pdftotext/python-docx/直接コピー）
- 画像PDF（OCR要）: 116件
- その他失敗: 11件

## v3配置結果

| 配置先 | 件数 | サイズ |
|---|---|---|
| 01_council/ | +93→168 | 13MB |
| 02_publications/reports/ | +101→143 | 1.3MB |
| 02_publications/leaflets/ | +3→110 | 1.1MB |
| 05_resources/ ★NEW | 577 | 114MB |
| 06_election/ ★NEW | 19 | 428KB |
| 99_raw/_pending_review | 1 | - |

**学習層合計: 1088件・130MB（grep対象）**

## 分類ロジック
1. ファイル名パターン（議事録/市政報告/印刷物/選挙/政策資料）
2. 親パスヒント（市議会・政策→05_resources、政治活動→05_resources、2026senkyo→06_election等）
3. パターン外455件は親パスベース救済振り分け（→05_resources/）
4. 残1件のみ pending（手動確認待ち）

## How to apply
- ブログ・SNS・スピーチ作成時に `01_council/ 02_publications/ 05_resources/ 06_election/` をgrepで横断検索
- 過去発言の連続性確保（voice-dna整合性）
- 選挙公約作成時に06_election/で過去資料参照
- 印刷物制作時に02_publications/leafletsの過去パターン継承
- 補正予算質疑時に05_resources/で過去予算書・原稿参照

## フェーズ2 完了（2026-05-05実施）

### ~/Documents/ 5階層大整理
| 階層 | 件数 | サイズ | 内容 |
|---|---|---|---|
| _archived_to_claude/ | 1316件 | 14G | 取込済原本（政治活動・市議会・政策・2026senkyo・選挙・サロン活動・kameyama-research・直下PDF・Desktop議員業務）|
| _personal/ | 3062件 | 1.5G | 選挙無関係（草川家・三重大・JC・PTA・消防団・eスポーツ・LoL・superwhisper・ObsidianVault・マスターズ陸上ほか）|
| _ext/ | 0 | 0B | シンボリックリンク（OneDrive・CreativeCloud）|
| _scratch/ | 9件 | 97M | 録音3件＋Word/Excel一時ファイル6件（隔離・削除しない）|
| _claude_active/ | 0 | 0B | 現在進行中作業の置き場（空）|

Creative Cloud Files は Adobe アプリ依存のため元の場所（Documents直下）に残置。`_ext/CreativeCloud` からシンボリックリンクで参照。

### Desktop / Downloads クリーン
- Desktop: 11件 → 4件（進行中フォルダ4のみ。議員業務PDF/docx 2件→_archived_to_claude/desktop_20260505/、Word一時5件→_scratch/_word_temp/隔離）
- Downloads: 9件 → 1件（_old_30d のみ。30日以上前5件隔離、Excel一時1件→_scratch/_word_temp/）

### 移動ログ
全51操作（mv 44件、ln -s 2件、mkdir 5件）を `~/Documents/_relocation_log_20260505.csv` に記録。逆順処理で復元可能。

### Spotlight再インデックス
`mdimport ~/Documents/` 実行済。検索インデックス更新で新パスに即追従。

## スクリプト
- 変換: `/tmp/kusagawa_intake/_convert.py`（並列pdftotext/docx）
- 分類: `/tmp/kusagawa_intake/_classify_v2.py`（6カテゴリ振り分け）
- 結果ログ: `/tmp/kusagawa_intake/_index.json` `_classified.json`
- フェーズ2計画: `/tmp/kusagawa_intake/_phase2_plan.md`
