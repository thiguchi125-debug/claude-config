# shisei-houkokukai スキル実装計画

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 市政報告会を5ステージ（企画相談→案内文兼レポート→スライド→連動解説→前夜チェック）でプロデュースするスキル一式（SKILL.md＋references 2本＋新設エージェント3本＋周辺更新）を実装する。

**Architecture:** 正本スペック＝同ディレクトリの `2026-07-04-shisei-houkokukai-design.md`（草川承認済み・以下「設計書」）。スキルは薄いオーケストレーターで、演出ドクトリンと解説PDF生成手順は references に分離、内容品質は新設エージェント3本が担う。進捗正本はローカル `_status.json`、Notionはミラー。

**Tech Stack:** Claude Code スキル/エージェント定義（Markdown＋YAML frontmatter）／HTML/CSS→Chrome headless PDF／Notion MCP／td.py（Todoist）

## Global Constraints

- 実装ファイルは**全て設計書の該当§に忠実に**書く。判断に迷ったら設計書が正
- 自作スキル・エージェントは `~/.claude/skills/`・`~/.claude/agents/` 直下のみ（plugins cache 禁止・agents/knowledge 配下に入れ子 `.claude` を作らない）
- 発信物系の記述に絵文字を使わないルール・他議員氏名禁止ルールを本文に必ず含める（設計書§5-4）
- 日本語は直接書く（JSON unicode escape で「亀」を書かない = 亀山typoガード）
- パスは全て絶対パスで記述（cwd依存禁止）
- ホームはgitリポジトリではない。バックアップは Task 8 の `~/claude-config/scripts/sync-to-git.sh` で行う
- 新スキル・新エージェントは**セッション再起動後に登録される**。同一セッションでの起動テストは不可（Task 8 の検証は静的チェックのみ）

## File Structure

```
~/.claude/skills/shisei-houkokukai/
  SKILL.md                       Task 3: 5ステージのオーケストレーション本体
  references/engagement.md       Task 1: 演出ドクトリン（設計書§5成文化）
  references/kaisetsu_format.md  Task 2: 解説カードPDFのテンプレ＋生成手順
  design/                        既存（設計書・本計画）
~/.claude/agents/
  audience-experience-reviewer.md  Task 4
  district-issue-scout.md          Task 5
  district-hazard-analyst.md       Task 6
~/CLAUDE.md                        Task 7: トリガー表1行追加
~/.claude/projects/-Users-kusakawatakuya/memory/
  feedback_shisei_houkokukai_slides_claude_code.md  Task 7: 移管を追記
  project_shisei_houkokukai_skill.md                Task 7: 新設
  MEMORY.md                                         Task 7: 1行追加
```

---

### Task 1: references/engagement.md（演出ドクトリン）

**Files:**
- Create: `/Users/kusakawatakuya/.claude/skills/shisei-houkokukai/references/engagement.md`

**Interfaces:**
- Produces: SKILL.md（Task 3）が Stage1 演出配置案・Stage3 スライド制作・Stage4 台本生成の前に Read するドクトリン文書。見出し構成（下記5節）を後続タスクが参照する

- [ ] **Step 1: 設計書§5「演出ドクトリン」「制作規格」を読む**

Read: `/Users/kusakawatakuya/.claude/skills/shisei-houkokukai/design/2026-07-04-shisei-houkokukai-design.md` の §5・§5.5

- [ ] **Step 2: engagement.md を書く**

以下の5節構成。各節の中身は設計書§5の該当項目を**そのまま展開**し、加えて明記事項を含める:

```markdown
# 市政報告会 演出ドクトリン（engagement.md）

## 1. 参加型（クイズ・問いかけ）
（設計書§5-1を展開。クイズ2枚ペア構造のHTMLパターン例・挙手アンケートのノート側キュー記法・
密度基準「30分2回以上/60分3〜4回を出発点、顔ぶれで増減・機械適用禁止」を明記）

## 2. 自分ごと化（地元密着）
（設計書§5-2を展開。柱ごと地区固有スライド1枚以上・「皆さんの」主語・
一般論スライドへの「では<地区>では？」接続規則）

## 3. 未来提示（選択肢を渡す）
（設計書§5-3を展開。分岐スライドの2列対比・行動CTAメニュー4種
（声を寄せる/AIインタビュー https://depth-interview-kusagawa.vercel.app/ /アンケート/次回参加））

## 4. 禁止・注意（ハードルール）
- 架空エピソード禁止／他議員氏名禁止／議事録引用は草川発言＋市答弁ペアのみ／
  抽象・詩的比喩禁止／絵文字なし／クイズの答えは一次情報裏取り必須（Stage1で実施済みが前提）

## 5. 実開催からの更新（腐敗防止）
- 本ドクトリンは実開催の「演出の効きメモ」（🎤報告会DB）と乖離したら更新する。
  更新提案はStage5後の声記録リマインド経由（設計書§7-4）。更新時は本節末尾に改訂履歴を1行追記
```

- [ ] **Step 3: 検証**

Run: `grep -c "^## " /Users/kusakawatakuya/.claude/skills/shisei-houkokukai/references/engagement.md`
Expected: `5`
Run: `grep -l "機械適用禁止" /Users/kusakawatakuya/.claude/skills/shisei-houkokukai/references/engagement.md`
Expected: パスが返る

---

### Task 2: references/kaisetsu_format.md（解説カードPDFテンプレ＋生成手順）

**Files:**
- Create: `/Users/kusakawatakuya/.claude/skills/shisei-houkokukai/references/kaisetsu_format.md`
- Test: `/private/tmp/claude-501/-Users-kusakawatakuya/*/scratchpad/kaisetsu_sample/`（レンダリング検証用・使い捨て）

**Interfaces:**
- Consumes: なし（独立）
- Produces: SKILL.md Stage4 が参照する解説PDFの完全な生成手順。カードのHTML構造（`data-id`属性・3種カードのclass名 `card-note` / `card-yamaba` / `card-time`）を後続が参照する

- [ ] **Step 1: kaisetsu_format.md を書く**

[[feedback_event_runsheet_mobile_pdf_format]] の確定手法を市政報告会解説向けに移植。以下を**実際のコード込み**で含める:

````markdown
# 解説カードPDF 生成フォーマット（kaisetsu_format.md）

## カード構造（HTML）
- 1スライド=1カード。`<section class="card card-note" data-id="s-cover">` のように
  slides.html と同じ data-id を必ず持たせる（IDロック。設計書§6）
- 3種: card-note（通常ノート/クリーム地#f3efe4）・card-yamaba（山場フル台本/lime帯#c7ff4a付き）・
  card-time（時間チェックポイント/濃緑#0f3d27白文字）
- カード内フィールド: スライド見出し／通し番号表示（併記）／話す骨子3行以内／累積時間目安／
  問いかけ・挙手キュー／用語言い換え。山場カードのみフル台本ブロック
- レイアウト: モバイルファースト1カラム `max-width:390px`・絵文字なし・
  ヘッダー（地区名・開催日・会場・開始時刻）

## PDF化手順（確定・ハマりどころ込み）
1. HTML は `width=device-width` レスポンシブで作成、`open` でブラウザ確認
2. print用styleを注入したコピーを Chrome headless で PDF化:
   `@page{size:390px <H>px;margin:0;}` 
   `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome --headless --print-to-pdf=<出力.pdf> <print用.html>`
3. <H>は実測必須: print描画はスクショ実測より約+200px。さらに+40〜60px余裕を足す
4. 実測時は `@media print{html,body{background:#fff}}` にして白余白を pdftoppm→PIL で下から検出
5. 単ページ検証: `strings <PDF> | grep -m1 "/Count"` が `/Count 1` になる高さを下から探索
6. body背景色はページ全体を塗る→ページ高さは中身ぴったりに（色付き長余白の防止）

## 差分再生成（前夜用・設計書§7-1）
- 対象 data-id のカードだけ書き換え→全体を再PDF化（カードHTML自体は1ファイルなので
  再PDF化コストは小さい。高さが変わったら/Count=1を再探索）
````

- [ ] **Step 2: サンプルで実地検証（テンプレが実際に1ページPDFになるか）**

スクラッチパッドに3カード分のサンプルHTML（card-note/card-yamaba/card-time 各1・ダミー文言）を kaisetsu_format.md のテンプレ通りに作成し、手順2〜5を実行。

Run: Chrome headless で PDF 生成 → `strings sample.pdf | grep -m1 "/Count"`
Expected: `/Count 1`（1ページ縦長PDFが生成できる）。失敗したら kaisetsu_format.md の手順を実態に合わせて修正してから完了とする

- [ ] **Step 3: 検証**

Run: `grep -c "data-id" /Users/kusakawatakuya/.claude/skills/shisei-houkokukai/references/kaisetsu_format.md`
Expected: 2以上（カード構造と差分再生成の両方に出現）

---

### Task 3: SKILL.md（オーケストレーション本体）

**Files:**
- Create: `/Users/kusakawatakuya/.claude/skills/shisei-houkokukai/SKILL.md`

**Interfaces:**
- Consumes: Task 1 `references/engagement.md`（5節構成）／Task 2 `references/kaisetsu_format.md`（card-note/card-yamaba/card-time・data-id）／新設エージェント名3本（audience-experience-reviewer / district-issue-scout / district-hazard-analyst = Task 4〜6 と正確に一致させる）
- Produces: スキル本体。frontmatter `name: shisei-houkokukai`

- [ ] **Step 1: frontmatter を書く**

```yaml
---
name: shisei-houkokukai
description: >
  草川たくや（亀山市議会議員）の市政報告会を5ステージでプロデュースするスキル。
  「〇〇地区の報告会準備」「報告会の企画相談」「市政報告会の企画」（Stage1）／
  「報告会の案内レポート作って」「案内文兼レポート」（Stage2）／
  「市政報告会のスライド作って」「〇〇の報告会スライド」（Stage3）／
  「報告会の解説作って」「報告会のスピーカーノート」「報告会の台本」（Stage4・
  「報告会」修飾必須。裸の「台本作って」では起動しない）／
  「報告会の前夜チェック」「明日の報告会の準備確認」（Stage5）で起動。
  1回の起動で1ステージだけを丁寧に進め、各ステージ出口で草川承認を取る。
  進捗の正本はローカル_status.json（Notionミラー）。ステージ名を言わない起動は
  次の未完了ステージを提案。開催まで2週間未満なら短縮経路
  （Stage1簡易版→Stage3→Stage4）を自動提案する。
---
```

- [ ] **Step 2: 本文を書く**

設計書§1〜§7を以下のセクション構成で**手順書として**書き下ろす（設計の背景説明は設計書に任せ、SKILL.mdは実行手順に徹する）:

```markdown
# 共通ルール
（_status.json正本・スキーマ例↓・Notionミラーはベストエフォート・出力先
 ~/outputs/houkokukai/<YYYY-MM-DD>_<地区>/・テンプレ血統デッキの参照パス
 ~/.claude/skills/slide-deck-prep/output/（御幸/小下/木下/太岡寺/城東・移動禁止）・
 起動時にまず_status.jsonを探して状態復元・開催日から残り日数<14なら短縮経路提案）

_status.json スキーマ:
{
  "event": {"district": "", "venue": "", "date": "YYYY-MM-DD", "slot_minutes": 60},
  "schedule": {"distribution_deadline": "", "stage2_deadline": "", "stage3_target": "",
               "stage4_target": "", "stage5_date": ""},
  "stages": {"stage1": {"status": "todo|doing|done", "completed_at": "", "artifacts": [],
             "themes": []}, "stage2": {...}, "stage3": {...}, "stage4": {...}, "stage5": {...}},
  "notion_page_url": ""
}

# Stage1 企画相談
（設計書§3を手順化: 第1段軽量パス4項目→地区解像度ヒアリング（AskUserQuestion1回・最大4問・
 原則1/原則2・🏘️DBの地区特性メモ蓄積）→audience-experience-reviewerテーマ価値モード→
 一次相談→深掘りパス（採用候補のみ・citizen-voice-analyst/policy-archive-miner/
 district-hazard-analyst起動条件）→二次相談→企画シート確定（山場数字はcontent-fact-checkerで
 この時点で裏取り）→逆算スケジュール確定→td.pyタスク登録提案（承認後）→_status.json更新）

# Stage2 案内文兼レポート
（設計書§4を手順化: 既存印刷ラインへ委譲・テーマ整合＋期待醸成フックのみ固有責務・
 安全2ゲート・open即実行）

# Stage3 スライド
（設計書§5を手順化: references/engagement.md を最初にRead・制作規格・品質ループ6手順
 （聴衆冷読み→物理破綻→軽い再照合fact-check→risk-review→承認→data-id凍結））

# Stage4 連動解説
（設計書§6を手順化: references/kaisetsu_format.md を最初にRead・IDロック・
 ノート項目/山場フル台本・community-rally-speaker技法参照・聴衆冷読み台本込み通し→
 安全2ゲート→スマホ縦PDF→open→承認）

# Stage5 前夜チェック
（設計書§7を手順化: 直前差分スキャン（data-id単位差し替え）・想定Q&A・進行チェックリスト・
 声記録リマインド＋演出の効きメモ1行＋engagement.md更新提案）

# 短縮経路
（設計書§1短縮経路の通り: Stage1簡易版（軽量パスのみ＋ヒアリング＋テーマ即決）→Stage3→Stage4。
 Stage2は既存チラシ代替・Stage5は当日朝最小版）
```

- [ ] **Step 3: 検証**

Run: `grep -c "district-issue-scout\|audience-experience-reviewer\|district-hazard-analyst" /Users/kusakawatakuya/.claude/skills/shisei-houkokukai/SKILL.md`
Expected: 3以上（3エージェント全てが本文に登場）
Run: `grep -l "_status.json" /Users/kusakawatakuya/.claude/skills/shisei-houkokukai/SKILL.md && grep -l "references/engagement.md" /Users/kusakawatakuya/.claude/skills/shisei-houkokukai/SKILL.md`
Expected: 両方パスが返る

---

### Task 4: audience-experience-reviewer エージェント

**Files:**
- Create: `/Users/kusakawatakuya/.claude/agents/audience-experience-reviewer.md`

**Interfaces:**
- Consumes: 企画シート（テーマ価値モードの入力）／slides.html・PDF・解説カード（冷読みモードの入力）
- Produces: エージェント名 `audience-experience-reviewer`（SKILL.md Task 3 の記載と一致必須）

- [ ] **Step 1: frontmatter を書く**（既存 natural-design-reviewer.md と同形式）

```yaml
---
name: "audience-experience-reviewer"
description: "Use this agent when a 市政報告会 deliverable for Kusagawa Takuya (草川たくや, Kameyama City council member) needs AUDIENCE-EXPERIENCE REVIEW — the content-side counterpart of natural-design-reviewer. 2 modes: (1) テーマ価値モード (Stage1): judges candidate themes on 『住民が60分を割く価値』『行動変化の見込み』『一般論落ち』, returns 序列＋ボツ推奨＋磨き方; (2) 聴衆冷読みモード (Stage3/4): simulates 2-3 audience personas GENERATED FROM the 企画シート's 当日の顔ぶれ (fallback: 子育て世代/高齢者/政治無関心層) cold-reading the deck/script, returns minute-level 飽きカーブ, 脱落ポイント, 不明用語, クイズ実効性, 終了時の行動意欲 as surgical TODOs keyed by slide data-id. Iteration discipline: 2回目以降は前回未指摘の新規問題のみ. Trigger: '聴衆レビュー', 'テーマ価値批評', '冷読みして', 'audience-experience-reviewer', '報告会の内容レビュー'. Do NOT use for: physical/design breakage (use natural-design-reviewer), fact verification (use content-fact-checker), risk (use content-risk-reviewer)."
model: opus
color: magenta
memory: project
---
```

- [ ] **Step 2: 本文を書く**

設計書§5.5新設①を展開。必須要素: 2モードの入出力定義／ペルソナ生成規則（企画シートの顔ぶれ欄→ペルソナ2〜3、無ければフォールバック3種）／冷読みの観点リスト（分単位飽きカーブ・脱落・不明用語・クイズ実効性・行動意欲）／指摘フォーマット（`[data-id] 指摘 → 直し方`の外科的TODO）／反復規律（前回指摘の記録と新規のみ報告）／「ドクトリン自己申告を信じず成果物を読む」原則／担当外への誘導（物理破綻→natural-design-reviewer等）

- [ ] **Step 3: 検証**

Run: `python3 -c "import yaml,sys; d=yaml.safe_load(open('/Users/kusakawatakuya/.claude/agents/audience-experience-reviewer.md').read().split('---')[1]); print(d['name'])"`
Expected: `audience-experience-reviewer`

---

### Task 5: district-issue-scout エージェント

**Files:**
- Create: `/Users/kusakawatakuya/.claude/agents/district-issue-scout.md`

**Interfaces:**
- Produces: エージェント名 `district-issue-scout`。出力フォーマット「地区×市政テーママップ」＋簡易ハザードフラグ（SKILL.md Stage1 軽量パスが消費）

- [ ] **Step 1: frontmatter を書く**

```yaml
---
name: "district-issue-scout"
description: "Use this agent when Kusagawa Takuya (草川たくや, Kameyama City council member) needs DISTRICT-LENS DISCOVERY of important 市政テーマ for a specified 地区/自治会 from past 議事録・市資料 — the supply-side counterpart to citizen-voice-analyst (demand side) sitting between kameyama-researcher (city-wide facts) and the 報告会 pipeline. Scans _index/ txt cache → kusagawa_archive (01_council/05_resources/02_publications) → Drive primary sources only when insufficient, crossing 地区名＋道路名・学校名・施設名・自治会名 AND 草川語彙並列grep. Returns 地区×市政テーママップ: per theme {時系列経緯/現在ステータス(計画中・予算化済・工事中・完了・停滞)/地区への影響/出典/草川の関与有無} plus 簡易ハザードフラグ (recommends district-hazard-analyst full run if flagged). Guard: 議事録引用は草川発言＋市答弁ペア原則, other members' facts marked 『他議員が引き出した数字』 internally and genericized before any slide use. Trigger: '地区の市政テーマ', '〇〇地区の論点発掘', 'district-issue-scout', '地区テーマスカウト'. Do NOT use for: citizen voices (citizen-voice-analyst), 草川自身の発言 (policy-archive-miner), city-wide research (kameyama-researcher), hazard deep-dive (district-hazard-analyst)."
model: sonnet
color: green
memory: project
---
```

（model: sonnet の理由 = Stage1軽量パス唯一のサブエージェントで探索主体・燃費重視。設計書§3）

- [ ] **Step 2: 本文を書く**

設計書§5.5新設②を展開。必須要素: 調査順序（`~/.claude/agents/knowledge/kusagawa_archive/_index/` txtキャッシュ最優先→アーカイブ実体→Drive）／**吸収したgrep手順を明記**（`grep -rl "<地区名>" ~/.claude/agents/knowledge/kusagawa_archive/{01_council,02_publications,03_themes,05_resources,06_election}/`・地区版ニュース確認 `ls .../02_publications/{reports,leaflets}/ | grep <地区名>`・草川語彙並列 `grep -rl -E "乗って残す|予防型|届ける仕事|一生応援"`）／出力フォーマット（テーママップのmarkdown表構造を具体例付きで）／簡易ハザードフラグの判定基準（アーカイブ内に浸水・土砂・ため池・避難所の地区該当記述があるか）／帰属ガードレール／tool_uses目安30回以内（D5準拠）

- [ ] **Step 3: 検証**

Run: `python3 -c "import yaml; d=yaml.safe_load(open('/Users/kusakawatakuya/.claude/agents/district-issue-scout.md').read().split('---')[1]); print(d['name'])"`
Expected: `district-issue-scout`
Run: `grep -l "_index" /Users/kusakawatakuya/.claude/agents/district-issue-scout.md`
Expected: パスが返る

---

### Task 6: district-hazard-analyst エージェント

**Files:**
- Create: `/Users/kusakawatakuya/.claude/agents/district-hazard-analyst.md`

**Interfaces:**
- Produces: エージェント名 `district-hazard-analyst`。出力「地区防災カルテ」（SKILL.md Stage1深掘りパス・Stage3素材化が消費）

- [ ] **Step 1: frontmatter を書く**

```yaml
---
name: "district-hazard-analyst"
description: "Use this agent when Kusagawa Takuya (草川たくや, Kameyama City council member) needs EXHAUSTIVE district-level HAZARD-MAP ANALYSIS for a specified 地区/自治会 — investigates ALL applicable hazard maps (亀山市総合防災マップ/三重県防災みえ/国交省重ねるハザードマップ/河川別洪水浸水想定(鈴鹿川・安楽川等)/土砂災害警戒区域・特別警戒区域/ため池/南海トラフ震度・液状化/内水氾濫/指定避難所・福祉避難所) down to 字名・自治会名 granularity, then performs CROSS-CHECK ANALYSIS (not map reproduction): 避難所×浸水域・土砂警戒区域の矛盾, リスク区域×通学路・要配慮者施設・孤立リスク, 市の対策の現在地(個別避難計画・防災井戸・災害時トイレ×草川の質問実績). Returns 地区防災カルテ: {該当ハザード一覧＋出典/問題点の指摘/提案の種(policy-expert-disaster-safety接続点)/スライド用図表指示(どのマップのどの範囲を切り出すか＋出典表記)}. Guard: 数値・区域・避難所名はfact-checker必須＋出典明記, マップ画像は出典表記ルール準拠, 『知って備える』フレームで不安を煽らない. Trigger: '地区のハザード分析', '〇〇地区の防災カルテ', 'district-hazard-analyst', 'ハザードマップ調べて分析'. Do NOT use for: national/prefectural policy trends (policy-expert-disaster-safety), city-wide facts (kameyama-researcher), theme discovery (district-issue-scout)."
model: opus
color: red
memory: project
---
```

- [ ] **Step 2: 本文を書く**

設計書§5.5新設③を展開。必須要素: 調査対象の網羅リスト（[[reference_bosai_link_collection]]の5定番リンク＝気象庁亀山2421000・川の防災情報・防災みえ・名阪国道規制・中電停電を起点に、重ねるハザードマップ・県土砂災害情報・市総合防災マップPDFへ拡張）／突合分析の3類型（避難所×リスク区域／リスク区域×通学路・要配慮者施設／対策の現在地×草川実績）／地区防災カルテの出力フォーマット（markdown構造を具体例付きで）／図表指示の書式（マップ名・切り出し範囲・出典表記文言）／ガードレール（fact-checker必須・出典明記・煽らないフレーム・他議員氏名禁止）

- [ ] **Step 3: 検証**

Run: `python3 -c "import yaml; d=yaml.safe_load(open('/Users/kusakawatakuya/.claude/agents/district-hazard-analyst.md').read().split('---')[1]); print(d['name'])"`
Expected: `district-hazard-analyst`

---

### Task 7: 周辺更新（CLAUDE.md・memory）

**Files:**
- Modify: `/Users/kusakawatakuya/CLAUDE.md`（トリガー早見表）
- Modify: `/Users/kusakawatakuya/.claude/projects/-Users-kusakawatakuya/memory/feedback_shisei_houkokukai_slides_claude_code.md`
- Create: `/Users/kusakawatakuya/.claude/projects/-Users-kusakawatakuya/memory/project_shisei_houkokukai_skill.md`
- Modify: `/Users/kusakawatakuya/.claude/projects/-Users-kusakawatakuya/memory/MEMORY.md`

- [ ] **Step 1: CLAUDE.md トリガー早見表に1行追加**（表の既存行の直後・「発信ネタ:」行の下）

```markdown
| 〇〇地区の報告会準備 / 報告会の企画・案内レポート・スライド・解説・前夜チェック | **shisei-houkokukai**（5ステージ制プロデュース・進捗は_status.json正本・急ぎは短縮経路） |
```

- [ ] **Step 2: feedback_shisei_houkokukai_slides_claude_code.md の How to apply 冒頭に移管を追記**

既存本文は残し、How to apply の先頭に以下を挿入:

```markdown
- **2026-07-04移管**: 市政報告会スライドの制作フローは shisei-houkokukai スキル（Stage3）が正。
  本メモの規格（16:9・草川カラー・テンプレ血統・2ゲート）はスキルに継承済み。
  トリガーが来たらまず shisei-houkokukai を起動する。出力先も
  ~/outputs/houkokukai/<日付>_<地区>/03_slides/ に変更（過去デッキは slide-deck-prep/output/ に据え置き・参照専用）。
```

- [ ] **Step 3: project_shisei_houkokukai_skill.md を新設**

```markdown
---
name: project_shisei_houkokukai_skill
description: 市政報告会5ステージプロデューススキル（2026-07-04設計・実装）。企画相談→案内レポート→スライド→連動解説→前夜チェック。新設エージェント3本。初回実走フィードバック待ち
metadata:
  type: project
---

# shisei-houkokukai スキル

2026-07-04 ブレインストーミング→批判的再検討10件反映→実装。設計書＝
`~/.claude/skills/shisei-houkokukai/design/2026-07-04-shisei-houkokukai-design.md`（正本スペック）。

- 5ステージ制・1起動1ステージ・草川承認ゲート・進捗正本 `_status.json`（Notion🎤報告会DBはミラー）
- 面白さ3軸＝参加型クイズ／自分ごと化／未来提示。解説＝ノート＋山場フル台本→スマホ縦PDF
- 新設エージェント: audience-experience-reviewer（テーマ価値＋聴衆冷読み・ペルソナは顔ぶれから生成）／
  district-issue-scout（地区×市政テーママップ・軽量パス唯一のagent）／district-hazard-analyst（地区防災カルテ・突合分析）
- Stage1は二段化（軽量→相談→深掘り）。逆算スケジュール→Todoist登録提案。短縮経路あり
- 次: 次回開催地区で実走→フィードバックをmemory化。engagement.mdは実開催の効きメモで更新する運用
関連: [[feedback_shisei_houkokukai_slides_claude_code]] [[feedback_shisei_houkokukai_voice_capture]] [[project_shisei_houkokukai_db]]
```

- [ ] **Step 4: MEMORY.md の「🔄 進行中プロジェクト」節の先頭に1行追加**

```markdown
- [市政報告会5ステージスキル](project_shisei_houkokukai_skill.md) — 2026-07-04実装。企画→案内→スライド→解説→前夜の5ステージ・新設agent3本（聴衆レビュー/地区テーマ/ハザード）・_status.json正本。初回実走待ち
```

- [ ] **Step 5: 検証**

Run: `grep -c "shisei-houkokukai" /Users/kusakawatakuya/CLAUDE.md`
Expected: 1以上
Run: `grep -l "project_shisei_houkokukai_skill" /Users/kusakawatakuya/.claude/projects/-Users-kusakawatakuya/memory/MEMORY.md`
Expected: パスが返る

---

### Task 8: 全体検証・バックアップ・Notion追記

**Files:**
- なし（検証と外部反映のみ）

- [ ] **Step 1: レジストリ汚染チェック（既知事故の再発防止）**

Run: `find /Users/kusakawatakuya/.claude/agents/knowledge -type d -name .claude`
Expected: 出力なし（入れ子.claudeが無い＝[[feedback_agent_registry_partial_load]]再発なし）

- [ ] **Step 2: ファイル一式の存在確認**

Run: `ls /Users/kusakawatakuya/.claude/skills/shisei-houkokukai/SKILL.md /Users/kusakawatakuya/.claude/skills/shisei-houkokukai/references/engagement.md /Users/kusakawatakuya/.claude/skills/shisei-houkokukai/references/kaisetsu_format.md /Users/kusakawatakuya/.claude/agents/audience-experience-reviewer.md /Users/kusakawatakuya/.claude/agents/district-issue-scout.md /Users/kusakawatakuya/.claude/agents/district-hazard-analyst.md`
Expected: 6ファイル全て存在

- [ ] **Step 3: 名前の相互整合チェック**

Run: `grep -o "audience-experience-reviewer\|district-issue-scout\|district-hazard-analyst" /Users/kusakawatakuya/.claude/skills/shisei-houkokukai/SKILL.md | sort -u | wc -l`
Expected: `3`（SKILL.mdが3エージェントを正確な名前で参照）

- [ ] **Step 4: claude-config へバックアップ**

Run: `bash /Users/kusakawatakuya/claude-config/scripts/sync-to-git.sh`
Expected: 正常終了（スキル消失ガード検知に引っかからないこと。エラー時は出力を草川に報告して停止）

- [ ] **Step 5: エージェントトリガー一覧Notionへ3本追記**

Notion「エージェントトリガー一覧」（[[reference_agent_triggers]]参照・notion-searchで特定）に新設3エージェントの行を追記（名前・発火ワード・Do NOT use）。update_content罠ルール準拠（追記のみ・fetch検証）。

- [ ] **Step 6: 草川へ完了報告**

再起動が必要な旨（スキル・エージェント登録はセッション再起動後に有効）＋初回実走の推奨（次回開催地区でStage1から）を報告して完了。
