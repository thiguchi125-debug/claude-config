# 草川たくや 知識アーカイブ ルートINDEX

**更新日**: 2026-05-05（v3：ローカル資料921件取込／05_resources・06_election新設・学習層1094件/130MBへ拡大）
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

## 2. ディレクトリ構造（v3）

```
~/.claude/agents/knowledge/kusagawa_archive/
├── INDEX.md                  ← このファイル（単一窓口）
│
├── 01_council/               議会発言テキスト（168件、13MB）
│   ├── _council_search_index.md   全期間索引47エントリ（H30〜R7）
│   ├── INDEX.md
│   ├── *_kusagawa.txt              草川パート抽出済（Drive取込分）
│   └── 通告書・原稿・議事録（市議会・政策/政治活動から取込分）
│
├── 02_publications/          公開発信物（306件、2.8MB）
│   ├── blog/                 ブログ全文53件（2021-10〜2026-05）
│   ├── reports/              市政報告レポート143件（38〜62号＋地区版＋Creative Cloud取込分）
│   └── leaflets/             印刷物110件（応援カード・チラシ・市政報告レポート1〜39号）
│
├── 03_themes/                テーマ別蒸留12件・328KB
│   └── 子育て教育/まちづくり経済/防災安全/暮らし福祉/DX/環境/議会改革/文化観光ほか
│
├── 04_compass/               政策コンパス・voice-dna・3本柱（6件・308KB）
│   ├── voice-dna.md          声の指紋（最重要）
│   ├── policy_compass.md     3軸＋origin story
│   ├── MISSION_REPORT.md
│   ├── manuscripts_inventory.md
│   └── 3pillars/             3本柱草案
│
├── 05_resources/             ★v3新設 政策資料・調査・要望書・計画書（582件、114MB）
│   ├── 補正予算原稿・予算書・決算書類
│   ├── 総合計画・基本計画・各種計画書
│   ├── 要望書・別紙・経緯資料
│   ├── 調査・アンケート・実施結果
│   ├── 政策メモ・政策案・各種参考資料
│   ├── 定期監査資料（各課別）
│   ├── 過去質問関連資料（DX/リニア/獣害/濁り水ほか）
│   ├── サロン活動・kameyama-research
│   └── notion_archive_2026-05-05/ ★Notion埋没ページ調査v1（4ファイル）
│       ├── 00_overview.md / 01_政策105件.md / 02_選挙地域150件.md
│       └── 03_議会市民相談160件.md / 04_action_plan.md
│
├── 06_election/              ★v3新設 選挙準備・公約・後援会（19件、428KB）
│   ├── 2026senkyo準備資料
│   ├── 過去選挙資料
│   ├── 公約・マニフェスト
│   ├── 戸別訪問記録・visit-scripts
│   └── 後援会員管理関連
│
└── 99_raw/                   ★grep対象外（容量隔離・原本保管）
    ├── _drive_originals/     Drive取込原本（238MB・82件）
    ├── _legacy/              旧 raw/ 配下（23件・448KB）
    ├── _needs_ocr/           OCR要PDF（8件）
    ├── _pending_review/      自動分類未マッチ（1件・要手動確認）
    └── _scripts/             同期＆抽出スクリプト（_drive_sync.sh / _extract_*.py / _classify.py / _sync_state.json）
```

---

## 3. エージェント参照規約

### 標準フロー
原稿生成前に以下を必ず実行：

```bash
# 1. テーマで横断grep（学習層全6階層）
grep -rl "<キーワード>" \
  ~/.claude/agents/knowledge/kusagawa_archive/01_council/ \
  ~/.claude/agents/knowledge/kusagawa_archive/02_publications/ \
  ~/.claude/agents/knowledge/kusagawa_archive/05_resources/ \
  ~/.claude/agents/knowledge/kusagawa_archive/06_election/

# 2. テーマ別蒸留ノート参照
ls ~/.claude/agents/knowledge/kusagawa_archive/03_themes/

# 3. 声・コンパス整合確認
cat ~/.claude/agents/knowledge/kusagawa_archive/04_compass/voice-dna.md
cat ~/.claude/agents/knowledge/kusagawa_archive/04_compass/policy_compass.md
```

### 用途別の優先参照先
- **議会発言の引用** → `01_council/`
- **市民向け発信文言の継承** → `02_publications/blog/` `02_publications/reports/`
- **印刷物（チラシ・カード）デザイン文言** → `02_publications/leaflets/`
- **政策の中身・補正予算・要望書・調査** → `05_resources/`
- **選挙公約・後援会・戸別訪問** → `06_election/`
- **テーマ俯瞰** → `03_themes/`
- **声・3軸の整合チェック** → `04_compass/`

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

### 標準運用（自動・週2回）
**毎週水・日曜21:00 JST にリモートRoutine `weekly-drive-sync-kusagawa` (trig_016r7yNKRqVubUvCJMTzVZ98) が自動実行**：
1. Drive **18フォルダ**を並列スキャン（modifiedTime差分）
2. ファイル名パターンで**6カテゴリ自動分類**（議事録/市政報告/印刷物/政策資料/選挙関連/未分類）
3. Notion `📥Drive取込キュー` DB (ed2d5e6a-96f9-) に登録
4. Gmail下書きで草川に通知

### 議会モード（議会期の頻度UP）
3/6/9/12月の議会開催月は草川が「議会モードon」と言うとcron `0 12 * * *`（毎日21時）に切替。議会終了後「議会モードoff」で `0 12 * * 0,3`（水・日）に復帰。詳細はスキル `council-mode-toggle` 参照。

### Drive投函ガイド（草川向け）
| 何を | どこに投函 | カテゴリヒント |
|---|---|---|
| 議会で配布された資料・議事録 | `R0X (年)` 等の年度フォルダ | 自動で01_council |
| 自分が作った市政報告レポート | `ZZ_市政報告レポート` | 自動で02_publications/reports |
| 行政・他団体からもらった政策資料 | `ZZ_政策資料` ★NEW | 自動で05_resources |
| 選挙公約・後援会・戸別訪問関連 | `ZZ_選挙関連` ★NEW | 自動で06_election |
| **迷ったら全部** | **`_INBOX_新規投函`** ★NEW | パターンマッチで自動振り分け、外れたら未分類 |

モバイル運用: iPhoneのDriveアプリで `_INBOX_新規投函` をホーム画面ショートカット登録 → 1タップで投函

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

## 7. ファイル件数サマリ（v3）

| 階層 | 件数 | サイズ | 用途 |
|---|---|---|---|
| `01_council/` | 168 | 13MB | 議会発言（grep対象） |
| `02_publications/blog/` | 53 | 420KB | ブログ全文 |
| `02_publications/reports/` | 143 | 1.3MB | 市政報告レポート（38〜62号＋地区版＋Creative Cloud） |
| `02_publications/leaflets/` | 110 | 1.1MB | 印刷物・応援カード |
| `03_themes/` | 12 | 328KB | テーマ別蒸留 |
| `04_compass/` | 6 | 308KB | コンパス・voice-dna・3pillars |
| `05_resources/` | 582 | 114MB | 政策資料・要望書・補正予算原稿・定期監査・参考資料＋Notion埋没ページ調査(2026-05-05) |
| `06_election/` | 19 | 428KB | 選挙準備・公約・後援会 |
| `99_raw/` | 114 | 240MB | 原本（grep対象外） |
| **合計** | **1202** | **370MB** | |

**学習層（grep対象 = 99_raw除く）**: **1088件・130MB**

---

**最終更新**: 2026-05-05（v3：ローカル資料921件取込／05_resources・06_election新設・学習層 301→1088件に拡大）
