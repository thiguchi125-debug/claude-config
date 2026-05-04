# 草川たくや 知識アーカイブ ルートINDEX

**更新日**: 2026-05-04（v2構造リファクタ完了：番号prefix 5階層に統合）
**目的**: 草川の発言・原稿・印刷物をエージェント（blog-writer / council-material-creator / sns-content-creator / speech-writer / policy-archive-miner / agenda-analyzer / counter-argument-simulator 等）が参照する横断検索基盤

---

## 1. 設計思想（重要）

### Drive vs ローカルの役割分担
- **Drive（クラウド）** = 受信箱／バックアップ（草川がブラウザ・モバイルから原本を投げ込む）
- **ローカル（このフォルダ）** = Claude の学習層（テキスト化・抽出済の高速検索DB）
- **同期** = 議会後 or 月次に `99_raw/_scripts/` を実行して Drive 原本→ローカル化

### 参照優先順位
1. **第一手**: ローカル grep（ゼロトークン・即時・全文走査）
2. **第二手**: Drive MCP `read_file_content`（ローカルに無い時のみ）

---

## 2. ディレクトリ構造（v2）

```
~/.claude/agents/knowledge/kusagawa_archive/
├── INDEX.md                  ← このファイル（単一窓口）
│
├── 01_council/               議会発言テキスト（75件、約4.4MB）
│   ├── _council_search_index.md   全期間索引47エントリ（H30〜R7）
│   ├── INDEX.md                    旧サブINDEX
│   ├── YYYY-MM_セッション_種別.txt（命名統一）
│   ├── 2018-12_H3012_本会議議事録_kusagawa.txt
│   ├── 2019-03_H3103_*.txt 〜 2026-03_R0803_*.txt
│   └── （旧 transcripts/ + transcripts/google_drive_kaigiroku/ 統合）
│
├── 02_publications/          公開発信物（202件、約1.8MB）
│   ├── blog/                 ブログ全文53件（2021-10〜2026-05）
│   ├── reports/              市政報告レポート42件（38〜62号＋地区版）
│   └── leaflets/             印刷物107件（応援カード・チラシ・市政報告レポート1〜39号）
│
├── 03_themes/                テーマ別蒸留12件
│   ├── 子育て・教育.md
│   ├── まちづくり・経済.md
│   ├── 防災・安全.md / 暮らし・福祉.md / 行政DX・透明性.md
│   ├── 環境・エネルギー.md / 議会改革.md / 文化・観光.md
│   ├── construction_union_report_2026_04.md
│   ├── construction_union_report_v3_2026_04.md
│   ├── noyaki_seikatu_kankyo.md
│   └── _v1_review_提案.md
│
├── 04_compass/               政策コンパス・voice-dna・3本柱（12件）
│   ├── voice-dna.md          声の指紋（最重要）
│   ├── policy_compass.md     3軸＋origin story
│   ├── MISSION_REPORT.md     アーカイブ整備の経緯
│   ├── manuscripts_inventory.md  原稿在庫の生記録
│   ├── 朝のブリーフィング_20260427.md
│   └── 3pillars/             3本柱草案（v0_handoff.md・step_a/）
│
└── 99_raw/                   ★grep対象外（容量隔離・原本保管）
    ├── _drive_originals/     Drive取込原本（254MB・PDF/docx/txt）
    │   ├── transcripts/      議事録原本＋_text/＋_kusagawa_only/
    │   ├── reports/          市政報告レポート原本＋_text/
    │   └── _INTAKE_REPORT.md  取込完全レポート
    ├── _legacy/              旧 raw/ 配下（HTML excerpts 等23件）
    ├── _needs_ocr/           OCR要PDF
    │   ├── council/          議事録（8件・画像PDF）
    │   └── canva/            印刷物（0件・将来用）
    └── _scripts/             同期＆抽出スクリプト
        ├── _extract_kusagawa.py     本会議用 草川パート抽出
        └── _extract_committee.py    委員会用 草川パート抽出
```

---

## 3. エージェント参照規約

### 標準フロー
原稿生成前に以下を必ず実行：

```bash
# 1. テーマで横断grep（学習層のみ・99_raw除外）
grep -l "<キーワード>" \
  ~/.claude/agents/knowledge/kusagawa_archive/01_council/*.txt \
  ~/.claude/agents/knowledge/kusagawa_archive/02_publications/blog/*.txt \
  ~/.claude/agents/knowledge/kusagawa_archive/02_publications/reports/*.txt \
  ~/.claude/agents/knowledge/kusagawa_archive/02_publications/leaflets/*.txt

# 2. テーマ別蒸留ノート参照
ls ~/.claude/agents/knowledge/kusagawa_archive/03_themes/

# 3. 声・コンパス整合確認
cat ~/.claude/agents/knowledge/kusagawa_archive/04_compass/voice-dna.md
cat ~/.claude/agents/knowledge/kusagawa_archive/04_compass/policy_compass.md
```

### 議事録参照規約（必須）
- **草川議員の発言＋亀山市側答弁**（市長／副市長／教育長／各部長等）の**ペアだけ**を抽出して使う
- 他議員（豊田／伊藤／前田／福沢ほか）の質疑ブロックは読み飛ばす
- 比較材料として他議員質問への市答弁を引く場合は「他議員〇〇氏が引き出した」と明示必須
- 詳細: `~/.claude/projects/-Users-kusakawatakuya/memory/feedback_giji_kusagawa_response_only.md`
- `01_council/` 配下の `*_kusagawa.txt` は既に抽出済（grep結果がそのまま安全）

---

## 4. 各リソースの使い分け

| ニーズ | 参照先 | 特徴 |
|---|---|---|
| 過去の議場発言を引用 | `01_council/*.txt` | 一次資料（議事録・原稿・通告書）、`*_kusagawa.txt` は草川パート抽出済 |
| 同テーマの過去ブログを引用 | `02_publications/blog/*.txt` | 公開済全文（2021-10〜2026-05全期間53件） |
| 市政報告レポートの文言継承 | `02_publications/reports/*.txt` | 38〜62号＋地区版42件 |
| 印刷物の文言継承 | `02_publications/leaflets/*.txt` | 応援カード・チラシ・市政報告レポート1〜39号107件 |
| テーマ別観点まとめ | `03_themes/*.md` | policy-archive-miner蒸留結果12件 |
| 声・3本柱・コンパス | `04_compass/` | voice-dna・policy_compass・3pillars |
| H30〜R7の発言索引 | `01_council/_council_search_index.md` | 47セッション索引 |
| Drive原本確認・再抽出 | `99_raw/_drive_originals/` | grep対象外。テキスト化済の原本 |

---

## 5. 更新方法（Drive→ローカル同期）

### 標準運用（自動・週次）
**毎週日曜21:00 JST にリモートRoutine `weekly-drive-sync-kusagawa` (trig_016r7yNKRqVubUvCJMTzVZ98) が自動実行**：
1. Drive 15フォルダを並列スキャン（modifiedTime差分）
2. ファイル名パターンで自動分類
3. Notion `📥Drive取込キュー` DB (ed2d5e6a-96f9-) に登録
4. Gmail下書きで草川に通知

**月曜朝 ohayo** で「📚 先週のDriveアーカイブ同期」セクションが表示され、確認待ち件数を案内。

**草川は `/drive-sync-review` を起動** → Notion DB から確認待ち取得 → 判定（全部/番号/差戻し/スキップ）→ 承認分のみローカルClaudeがDrive MCPでダウンロード→pdftotext→草川パート抽出→ `01_council/` or `02_publications/reports/` に配置 → Notion状態更新。

### 議会直後など緊急時の手動取り込み手順
1. 草川がブラウザでDriveに資料を置く
2. ローカルClaude Codeで `/weekly-drive-sync` 実行（手動実行版）
3. または Routine手動トリガー: https://claude.ai/code/routines/trig_016r7yNKRqVubUvCJMTzVZ98
4. その後 `/drive-sync-review` で取込

### 市政報告レポート追加時
1. Canva「ダウンロード→PDF」を `99_raw/_drive_originals/reports/` に置く
2. `pdftotext -layout <pdf> 99_raw/_drive_originals/reports/_text/<basename>.txt`
3. `cp 99_raw/_drive_originals/reports/_text/<basename>.txt 02_publications/reports/`

### ブログ・SNSの定期同期
- 月次cron: `~/.claude/scripts/published-archive/scrape_full_blog.py`
- 出力先: `02_publications/blog/`

---

## 6. 既知の穴（残課題）

| 領域 | 穴 | 対応策 |
|---|---|---|
| 議事録H30-R6 | 通告書のみ・本会議全文なし | 議会事務局B案請求 |
| 議事録 R030604/0827/1126 | 議題HTMLのみ | B案請求 |
| 議事録 R040225〜R050825 | 部分のみ | B案請求 |
| 議事録 R061129 | 議題HTMLのみ | B案請求 |
| R8.3.18決算委員会 | 音声起こし誤認識でセッション本体取り損ね | スクリプト改修 or 手動補正 |
| OCR要PDF | 8件（議事録）+ 1件（市政レポート51） | `brew install tesseract tesseract-lang` 後OCR |
| 一般質問資料zip | PNG4枚（議場配布資料）OCR要 | 同上 |
| Threadsスクレイプ | パーサー破損 | Threads UI再調査 |
| X/Instagram/Facebook全件 | API有償 | CSVエクスポート手動 |

---

## 7. ファイル件数サマリ

| 階層 | 件数 | サイズ | 用途 |
|---|---|---|---|
| `01_council/` | 75 | 4.4MB | 議会発言（grep対象） |
| `02_publications/blog/` | 53 | 420KB | ブログ全文 |
| `02_publications/reports/` | 42 | 360KB | 市政報告レポート |
| `02_publications/leaflets/` | 107 | 1.1MB | 印刷物 |
| `03_themes/` | 12 | 328KB | テーマ別蒸留 |
| `04_compass/` | 12 | 224KB | コンパス・voice-dna |
| `99_raw/` | 221 | 254MB | 原本（grep対象外） |
| **合計** | **522** | **261MB** | |

**学習層（grep対象 = 99_raw除く）**: 301件・6.8MB

---

**最終更新**: 2026-05-04（v2構造リファクタ：番号prefix 5階層・Drive同期スクリプト整備）
