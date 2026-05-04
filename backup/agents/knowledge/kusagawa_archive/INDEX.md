# 草川たくや 知識アーカイブ ルートINDEX

**更新日**: 2026-05-04（Drive一次資料28議事録＋42市政報告レポート 取込完了）
**目的**: 草川の発言・原稿・印刷物をエージェント（blog-writer/council-material-creator/sns-content-creator/speech-writer/policy-archive-miner等）が参照する横断検索基盤

## 上流：Drive 一次資料サイロ
- URL: https://drive.google.com/drive/folders/1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg
- folder_id: `1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg`
- 構成: H30(2018-12〜)〜R08(2026)年度別議事録／ZZ_市政報告レポート38〜62号＋地区版／ZZ_委員会・地域議事録／ZZ_政策別深掘り／ZZ_議会事務局公式OneDrive／ZZ_ブログSNS全アーカイブ／99_音声記録 全17フォルダ
- このローカル `kusagawa_archive/` は Drive 一次資料を**テキスト化・索引化した高速参照層**
- 参照優先順位: **ローカルgrep → 不足時のみ Drive MCP `read_file_content`**

## 議事録参照規約（必須）
- **草川議員の発言＋亀山市側答弁（市長／副市長／教育長／各部長等）のペアだけ**を抽出して使う
- 他議員（豊田／伊藤／前田／福沢ほか）の質疑ブロックは読み飛ばす
- 比較材料として他議員質問への市答弁を引く場合は「他議員〇〇氏が引き出した」と明示必須
- 詳細: `~/.claude/projects/-Users-kusakawatakuya/memory/feedback_giji_kusagawa_response_only.md`

---

## ディレクトリ構造

```
~/.claude/agents/knowledge/kusagawa_archive/
├── INDEX.md                  ← このファイル
├── transcripts/              議会発言テキスト（45件・約2MB）
│   ├── INDEX.md
│   ├── _council_search_index.md  ★全期間索引47エントリ（H30〜R7）
│   ├── _needs_ocr/           画像PDFでOCR要（8件）
│   ├── 2019-06_R010531_*.txt 〜 2026-03_R080304_*.txt
│   └── google_drive_kaigiroku/  ★2026-05-04取込・草川パート＋執行部答弁のみ抽出（28件・2.2MB、H30〜R08全期間）
├── blog_full/                ブログ全文（53件・約420KB）
│   └── 2021-10_311522_リニア〜.txt 〜 2026-05_1370223_防災気象情報.txt
├── canva/                    印刷物テキスト（107件・1.1MB）★NEW
│   ├── 2026-05-04_canva_*.txt（応援カード/産後ケア/市政報告会・10件）
│   ├── 2026-05-04_shisei_*.txt（市政報告レポート1〜39号系・97件）
│   ├── _needs_ocr/  画像PDF・OCR要（16件・市政報告レポート4・5・37他）
│   └── google_drive_reports/  ★2026-05-04取込・市政報告レポート38〜62号＋地区版（42件・360KB）
├── themes/                   テーマ別蒸留ノート（11件）
│   ├── 子育て・教育.md
│   ├── まちづくり・経済.md
│   └── （他・防災/福祉/DX等）
├── 3pillars/                 3本柱草案
│   ├── v0_handoff.md
│   └── step_a/
├── googledrive/              ★2026-05-04取込・原本＋中間テキスト＋抽出スクリプト（_INTAKE_REPORT.md参照）
│   ├── transcripts/   原本29PDF+1docx+2txt → _text/ → _kusagawa_only/
│   └── reports/       原本43PDF+1zip → _text/ → canva/google_drive_reports/へ統合済
└── raw/
    └── council_minutes_excerpts/  議題HTML20セッション
```

---

## 各リソースの使い分け

| ニーズ | 参照先 | 特徴 |
|---|---|---|
| 過去の議場発言を引用 | `transcripts/*.txt` | 一次資料（議事録ドラフト・原稿・通告書） |
| 同テーマの過去ブログを引用 | `blog_full/*.txt` | 公開済全文（2021-10〜2026-05全期間） |
| 印刷物の文言継承 | `canva/*.txt` | 応援カード・チラシ・**市政報告レポート1〜39号** |
| 過去の有権者向けメッセージング履歴 | `canva/2026-05-04_shisei_*.txt` | 2018年初当選〜2026年現在の継続的市政報告（97号分） |
| テーマ別観点まとめ | `themes/*.md` | policy-archive-miner蒸留結果 |
| 3本柱・コンパス | `3pillars/`, `policy_compass.md` | 政策の軸 |
| H30〜R7の発言索引 | `transcripts/_council_search_index.md` | 47セッション索引（全文は事務局B案要請） |

---

## エージェント参照規約

エージェントは原稿生成前に以下を必ず実行：

```bash
# 同テーマの過去発言を確認
grep -l "<キーワード>" ~/.claude/agents/knowledge/kusagawa_archive/transcripts/*.txt
grep -l "<キーワード>" ~/.claude/agents/knowledge/kusagawa_archive/blog_full/*.txt

# テーマ別蒸留ノートを参照
ls ~/.claude/agents/knowledge/kusagawa_archive/themes/
```

---

## 更新方法

### 議事録（transcripts/）
- 新セッション後、PDF/DOCXを `~/Documents/市議会・政策/<年>/` に保存
- バッチ実行: `bash /tmp/convert_transcripts.sh`（カスタマイズ要）

### ブログ全文（blog_full/）
- 月次オートで `~/.claude/scripts/published-archive/scrape_full_blog.py` 実行
- 新規記事ID追加→再実行

### Canva印刷物（canva/）
- Canvaで「ダウンロード→PDF（標準）」エクスポート
- `~/.claude/scripts/canva-import/canva_to_text.sh <pdf_path>` 実行
- 一括: `~/.claude/scripts/canva-import/canva_to_text.sh --batch ~/Downloads/`

### 公開済アーカイブDB（Notion）
- ohayo月曜分岐 cron で自動増分
- 全件再取得は `python3 ~/.claude/scripts/published-archive/scrape_full_blog.py`

---

## 既知の穴（連休明け対応）

| 領域 | 穴 | 対応策 |
|---|---|---|
| 議事録H30-R6 | 通告書のみ・全文なし | 議会事務局B案請求 |
| 議事録 R030604/0827/1126 | 議題HTMLのみ | B案請求 |
| 議事録 R040225〜R050825 | 部分のみ | B案請求 |
| 議事録 R061129 | 議題HTMLのみ | B案請求 |
| OCR要PDF（8件） | 画像PDF | brew install tesseract or shortcuts |
| Threadsスクレイプ | パーサー破損 | Threads UI再調査 |
| X/Instagram/Facebook | API有償 | CSVエクスポート手動 |

---

**最終更新**: 2026-05-04（Step 1議事録テキスト化／Step 2ブログ全件取得／会議録索引／Canva対応 完了）
