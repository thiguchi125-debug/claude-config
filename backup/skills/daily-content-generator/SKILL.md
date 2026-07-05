---
name: daily-content-generator
description: |
  草川たくや（亀山市議会議員）の**当日発信フルパッケージ**を1パスで生成する日次オーケストレータースキル。
  Notion（🎯政策・質問ネタDB（統一・42716725）／📣SNS投稿管理DB／📋市民意見受付BOX／📰ニュースDB／📒nichijo日次ログ）から
  当日テーマ候補を棚卸し→2〜3本を4軸スコアリングで選定→事実検証→
  ブログ＋7SNS（X単発/Xスレッド/Threads/Instagram/Facebook/LINE/YouTube/TikTok）＋
  ショート動画原稿＋差し込み画像プロンプトを一括生成、安全ゲート（content-fact-checker→content-risk-reviewer）通過後に
  `~/outputs/daily-content/<日付>/`（絶対パス・cwd非依存）へ揃える。

  「今日の発信」「日次配信」「daily content」「今日のフルパッケージ」「全チャネル回して」「daily-content-generator」
  「ブログとSNSと動画まとめて」「今日の発信ネタ選んで全部作って」等で起動。
  ohayoスキルで朝の3案提案を確認→草川承認→本スキルでフル展開、という連結運用が標準。

  本スキルは**薄いオーケストレーター**で、実装は既存資産にフル委譲する：
  - テーマ候補棚卸し: Notion MCP直接クエリ
  - 事実検証: policy-researcher / kameyama-researcher 並列
  - ブログ生成: blog-writer（深掘り）or blog-writer-normal（市民向け）
  - SNS生成（7PF）: sns-content-creator
  - ショート動画: short-video-virality-architect
  - 画像プロンプト: nanobanana-prompt-designer
  - 安全ゲート: content-fact-checker → content-risk-reviewer（CLAUDE.md必須）
  - Notion保存: notion-saver

  Do NOT use when:
  - 単発テーマだけ深掘りしたい（→ content-pipeline 直接起動）
  - 録音/文字起こし素材から1記事だけ作る（→ content-pipeline）
  - 議会答弁書・委員会資料（→ council-material-creator）
  - 当日の活動記録からコンテンツ抽出（→ nichijo の「今日のコンテンツ抽出」モード）
  - ショート動画1本だけ（→ short-video-create）
---

# Daily Content Generator

## このスキルが何をするか（30秒サマリ）

**「今日、何を発信するか」を草川が考えなくていい状態にする。**

Notion蓄積資産 → 当日テーマ2〜3本選定 → 全チャネル原稿＋画像プロンプト → 安全ゲート通過 → コピペ可能なファイル群を `~/outputs/daily-content/<日付>/` に整列。

朝の `ohayo` で提示される3案からの「これとこれで全部作って」型指示に対する**フル実行スキル**。

---

## 前提・依存

### MCP接続
- **Notion MCP**（必須）— 主要DBへのアクセス
- **Google Drive MCP**（任意）— 一次資料が必要な場合のみ

### サブエージェント / 既存スキル
| 用途 | 委譲先 |
|---|---|
| 国政動向・他自治体事例 | `policy-researcher` |
| 亀山市現状・議事録 | `kameyama-researcher` |
| 草川過去発言（必須参照） | ローカルgrep `~/.claude/agents/knowledge/kusagawa_archive/` |
| ブログ深掘り | `blog-writer` |
| ブログ市民向け | `blog-writer-normal` |
| 7PF SNS生成 | `sns-content-creator` |
| ショート動画原稿 | `short-video-virality-architect` |
| 画像プロンプト | `nanobanana-prompt-designer` |
| 事実検証ゲート | `content-fact-checker`（**必須**） |
| リスクレビューゲート | `content-risk-reviewer`（**必須**） |
| Notion保存 | `notion-saver` |

### 重要な参照ファイル
- `~/.claude/agents/knowledge/kusagawa_archive/04_compass/voice-dna.md` — 声のDNAコア
- `~/.claude/agents/knowledge/kusagawa_archive/04_compass/policy_compass.md` — 3軸コア
- `~/.claude/agents/knowledge/kusagawa_archive/03_themes/` — テーマ別過去発言集約

### 主要Notion DB
- 🎯政策候補DB: `6f1895ac-`
- 📝一般質問ネタDB: `42716725-`
- 📣SNS投稿管理DB: `1bd98deb-`（data_source_id、タイトル先頭🎬で動画系）
- 📝市民意見リスト: `c2c34bd8-`（旧📦受付BOX354432ec-は廃止統合済）
- 📰ニュースDB: news-briefing で更新
- 📒nichijo日次ログDB: 当日活動記録

### 絶対ルール（CLAUDE.md準拠）
1. **冒頭挨拶**: ブログ1行目は必ず「こんにちは、亀山市議会議員の草川たくやです。」
2. **議会質問アーカイブ常時参照**: 全テーマでローカルgrep必須
3. **議事録は草川発言＋市回答ペアのみ抽出**（他議員質疑は読み飛ばし）
4. **他議員氏名は対外発信物に記載しない**
5. **安全ゲート必須**: content-fact-checker → content-risk-reviewer の順で必ず通過
6. **HIGH以上のリスク検出時**: 草川にASK_USERで本人判断を仰ぐ
7. **CRITICAL検出時**: 即停止し草川に通知
8. **事実と推論を分離**: 私見には「私は」「と考える」等の標識
9. **架空エピソード禁止**: 実体験/一次情報/公式データのみ
10. **「届かないを終わらせる」「届かなくても届く」等の禁止フレーズ使用禁止**（MEMORY.md参照）

### 一次ソース優先順位
①亀山市公式サイト・議事録 → ②三重県・国の省庁サイト・統計 → ③国会・地方議会の公的議事録 → ④査読論文・公的調査 → ⑤報道（補助）

---

## ワークフロー（5ステップ）

### Step 1: テーマ候補の棚卸し（Notion探索 + 既発信重複チェック）

**1-1. 候補抽出**

以下5ソースから並列で候補を抽出：

```
A. 🎯政策候補DB(6f1895ac-) — 直近30日更新 × ステータス≠「発信済み/完了」
B. 📝一般質問ネタDB(42716725-) — 直近の議会で扱った/扱う予定
C. 📝市民意見リスト(c2c34bd8-) — 直近2週間の未返信／フォロー対象
D. 📰ニュースDB — 当日のニュース（亀山市・三重県・関心テーマ）
E. 📒nichijo日次ログ — 直近3日の活動記録から抽出されたコンテンツ素材
```

**1-2. 時事フック判定**

当日が以下に該当するか確認：
- 議会日程（本会議・委員会・所信表明等）
- 法令施行日・制度切替日（例: 太陽光FIP切替、児童手当拡充、こども基本法等）
- 季節事象（母子保健月間／防災週間／新年度施策周知期間／予算編成期）
- 亀山市カレンダー上の関連イベント

**1-3. 既発信重複チェック（必須）**

📣SNS投稿管理DB(1bd98deb-) の「完了」ステータス × 直近14日分を取得 → 同一テーマ連投回避。
既発信テーマは原則除外、または「新しい角度」での再投稿のみ可。

**1-4. 草川過去発言アーカイブgrep（必須）**

各候補テーマについて：
```bash
grep -rl "<キーワード>" ~/.claude/agents/knowledge/kusagawa_archive/{01_council,02_publications,05_resources,06_election}/
```
過去発言が1件でもあるテーマを優先（実績ベースで語れる）。

---

### Step 2: テーマ選定（2〜3本に絞る・4軸スコアリング）

各候補を以下4軸×10点で採点し、合計上位2〜3本を選定。

| 軸 | 評価観点 | 配点 |
|---|---|---|
| **時事性** | 議会日程・施策スケジュール・季節事象との合致度 | 10 |
| **政策価値** | EBPM観点で語れるか（アウトプット/アウトカム指標が示せるか） | 10 |
| **共感性** | 子育て・健康・地域インフラ等、生活実感に紐づくか | 10 |
| **情報の鮮度** | 一次ソースが直近更新で、新しい論点を提示できるか | 10 |

**軸足チャネル指定**

選定後、各テーマに軸足を1つ割当：
- 政策深掘り型 → **ブログ軸**（他はブログの縮約・派生）
- 共感・現場ストーリー型 → **ショート動画軸**（動画→SNSティーザー展開）
- 速報・時事即応型 → **X軸**（X単発→他PFへ縮約）

軸足が決まると他チャネルは自動的に派生形になり、生成効率が上がる。

---

### Step 3: 事実検証（一次ソース確認）

各テーマについて `policy-researcher` と `kameyama-researcher` を**並列起動**し、ファクトシートを作成。

```
Agent(subagent_type="policy-researcher",
  prompt="テーマ: {theme}
  以下を一次ソース付きで調査:
  1. 国の政策・法制度（法律名・通知名・年月日明記）
  2. 統計データ（全国・三重県・亀山市比較）
  3. 先進自治体事例3本以上（人口5万人規模優先）
  4. 失敗・中止事例も含める
  スコープ厳守: voice-dna・3pillars等のローカル既存資料は明示依頼時のみ参照。
  tool_uses 30回以内目安。")

Agent(subagent_type="kameyama-researcher",
  prompt="テーマ: {theme}
  亀山市の現状・既存施策・担当課・議会過去議論（草川発言含む）・三重県動向。
  スコープ厳守同上。")
```

**ファクトシート（`facts.md`）の構成**：
- **確定事実**: 一次ソースURL＋該当箇所引用（15字未満）
- **数値・期日・固有名詞**: ソース付き一覧
- **草川過去発言**: archive grep結果から該当箇所抜粋
- **推論・私見**: 「これは草川の見解」と明記
- **未確認事項**: 確認できなかった点を正直にリスト化

このファクトシートを後段すべての原稿の**素材**として固定。ファクトシートにない数字・固有名詞は原稿に書かない。

---

### Step 4: チャネル別原稿生成

各テーマ × 各チャネルでマトリクスを埋める。**軸足チャネルから生成→他は縮約派生**の順で効率化。

#### 4-1. ブログ（軸となる長文）

判定:
- **深掘りモード** → `blog-writer` 起動（1500〜2500字、5段構成、政策論考）
- **市民向けモード** → `blog-writer-normal` 起動（800〜1500字、柔軟構成、平易な日本語）

判定基準: 政策深掘り＝深掘り、活動報告/イベント告知＝市民向け。

```
Agent(subagent_type="blog-writer",  # or blog-writer-normal
  prompt="テーマ: {theme}
  ファクトシート: {facts.md の内容}
  軸足: {ブログ or 派生}
  CLAUDE.md D1-D5原則準拠。フッター（◆ご意見箱／◆公式LINE／◆Threads）省略禁止。
  冒頭挨拶必須。タイトル50字以内。")
```

#### 4-2〜4-7. SNS 7PF + ショート動画

**sns-content-creator** に1回で7PF全件を委譲（標準）：

```
Agent(subagent_type="sns-content-creator",
  prompt="テーマ: {theme}
  ファクトシート: {facts.md}
  ブログURL/抜粋: {blog.md の冒頭500字 or 仮置きURL}
  軸足: {軸足チャネル}
  生成対象: Threads / X単発 / Xスレッド / Instagram / Facebook / LINE / YouTube概要 / TikTok概要
  各PFの定型・字数・トーンはエージェント側ルール準拠。
  ハッシュタグ・公選法ガード必須。")
```

**ショート動画原稿は別途 `short-video-virality-architect` に委譲**：

```
Agent(subagent_type="short-video-virality-architect",
  prompt="テーマ: {theme}
  ファクトシート: {facts.md}
  尺: 45〜60秒
  出力: 3バリアント（A=フック最強/B=共感ストーリー/C=議論喚起）
  各バリアントcut-by-cut表、テロップ、B-roll指示、CTA含む。")
```

#### 4-8. 差し込み画像プロンプト

`nanobanana-prompt-designer` に委譲（ショート動画原稿を入力として渡す）：

```
Agent(subagent_type="nanobanana-prompt-designer",
  prompt="テーマ: {theme}
  動画原稿: {short_video_script.md}
  生成対象:
  - ブログヘッダー画像（16:9）
  - Instagram1枚目コピー画像（1:1、画像内テキスト指示込み）
  - Instagramカルーセル用図解（必要枚数、データ可視化）
  - ショート動画サムネ（9:16）
  - 動画内差し込みカット2〜5枚（9:16）
  固定方針: 草川本人画像はAI生成禁止（実写差し込み前提）。亀山ローカル背景活用。
  著作権リスク回避。日本語フォント崩れ対策（英数字のみ or 事後別途乗せ前提）。")
```

---

### Step 5: 安全ゲート通過（CLAUDE.md必須）

**5-1. content-fact-checker** を全原稿に対して順次起動

```
Agent(subagent_type="content-fact-checker",
  prompt="以下の原稿群の数値・固有名詞・法令・統計を一次情報まで遡って検証:
  - blog.md
  - x_single.txt / x_thread.txt
  - threads.txt / instagram.md / facebook.txt / line.txt
  - short_video_script.md
  ファクトシート: {facts.md}
  検証不可・不確実な箇所は『未確認』マークで返す。")
```

**5-2. content-risk-reviewer** を全原稿に対して順次起動

```
Agent(subagent_type="content-risk-reviewer",
  prompt="以下の原稿群を8軸スキャン:
  個人情報／機密／公選法／名誉毀損／差別／利益相反／品位／物議
  対象: blog.md / 各SNS / short_video_script.md / image_prompts.md
  HIGH以上は草川へのASK_USER問いかけ文を含めて返す。
  CRITICALは即停止。")
```

**5-3. 結果反映**

- APPROVE → そのまま Step 6 へ
- REVISE → 指摘箇所を修正して 5-1 再実行
- ASK_USER → 草川に問いかけて判断を仰ぐ
- REJECT → 該当テーマを当日リストから外す

---

### Step 6: 出力統合とファイル配置

`~/outputs/daily-content/<YYYY-MM-DD>/` 配下に保存。

```
outputs/daily-content/2026-05-21/
├── 00_summary.md              # 当日テーマ一覧・スコア・配信時間目安・要確認事項
├── theme-01_<slug>/
│   ├── facts.md               # 一次ソース・確定事実・未確認事項
│   ├── blog.md                # 冒頭挨拶〜フッター完備
│   ├── x_single.txt           # 140字
│   ├── x_thread.txt           # 3〜5ポスト
│   ├── threads.txt            # 350字前後
│   ├── instagram.md           # キャプション + カルーセル指示
│   ├── facebook.txt           # 500〜800字
│   ├── line.txt               # 300字以内 + 配信時間メモ
│   ├── short_video_script.md  # 3バリアント・セリフ・テロップ・B-roll
│   ├── image_prompts.md       # 全画像プロンプト
│   └── _gate_log.md           # fact-checker / risk-reviewer の結果ログ
├── theme-02_<slug>/
│   └── (同構成)
└── theme-03_<slug>/
    └── (同構成)
```

**`00_summary.md` のフォーマット**:

```markdown
# 本日のテーマ（2026-05-21）

## テーマ01: <テーマ名>
- 軸足: ブログ
- スコア: 時事8 / 政策9 / 共感6 / 鮮度8 = 31
- 一次ソース: <URL>
- 主張: <一文>
- 配信時間目安: ブログ朝7時 / X単発昼12時 / ショート動画夜19時
- 過去発信参照: <archive grepヒット件数とパス>

## テーマ02: ...
## テーマ03: ...

## 要確認事項（草川判断待ち）
- [ ] テーマ01のリスクHIGH: 〜〜について本人判断を仰ぐ
- [ ] テーマ02のfacts.md未確認項目: 〜〜の数字を草川手元資料で確認

## 既発信重複チェック結果
- 過去14日に同一テーマなし（OK）
or
- テーマ02は5/15に既発信 → 新しい角度（〜〜）で再投稿の判断待ち
```

---

## 出力時のユーザーへの提示フォーマット

```
本日のフルパッケージ生成完了（2026-05-21）

📌 テーマ01: <テーマ名> [軸足: ブログ / スコア: 31]
   一次ソース: <URL>
   主張: <一文>

📌 テーマ02: <テーマ名> [軸足: ショート動画 / スコア: 29]
   ...

📌 テーマ03: <テーマ名> [軸足: X / スコア: 27]
   ...

全原稿を outputs/daily-content/2026-05-21/ に出力済み。
安全ゲート: 全テーマ通過（or HIGH×N件、草川判断待ち）

要確認事項:
- <リスト>

どのテーマから公開しますか？
（A: 全て承認→Notion保存 / B: テーマ単位で確認 / C: 個別修正指示）
```

---

## EBPM原則（全原稿共通）

- **アウトプット（やったこと）とアウトカム（どう変わったか）を必ず分けて書く**
- 数値は出典付きで、比較対象（他自治体・全国平均・経年変化）を併記
- 「効果がある」と書く場合は、効果測定方法も併記。測定方法が無ければ「今後の検証項目」として残す
- 「〇〇すべき」と書く場合は、根拠となる先行事例・統計を明示

---

## 品質チェックリスト（Step 5 と並行して自動実行）

- [ ] 各原稿に一次ソースURLが少なくとも1本入っている
- [ ] 事実と私見が文体で区別されている（私見には「私は」「と考える」等の標識）
- [ ] 個人名・数値・固有名詞が `facts.md` と一致している
- [ ] 同じ表現を2週間以内に投稿していない（📣SNS投稿管理DB照合済み）
- [ ] 画像プロンプトに実在人物の生成指示が含まれていない
- [ ] ハッシュタグに政争的・差別的表現が含まれていない
- [ ] 引用は15字未満に収まっている
- [ ] 他議員氏名が記載されていない
- [ ] 禁止フレーズ（「届かないを終わらせる」「届かなくても届く」等）が含まれていない
- [ ] ブログ冒頭挨拶 / 末尾フッター完備（D1原則）
- [ ] ブログタイトル50字以内（D3原則）
- [ ] 議会・他議員に対する提言色がない（執行部宛のみ）

不合格項目は `00_summary.md` 末尾の「要確認事項」に列挙し、草川判断を仰ぐ。

---

## トークン効率化原則（CLAUDE.md D1〜D5準拠）

- **D1 完全保管原則**: blog-writer出力は一字一句そのまま `outputs/.../blog.md` に Write
- **D2 承認後保存原則**: fact-checker / risk-reviewer 指摘がある状態でNotion保存しない。草川承認→1回でNotion保存
- **D3 タイトル50字以内**: blog-writer規定通り
- **D4 PDFは pdftotext**: WebFetch失敗時は `pdftotext -layout` で抽出
- **D5 リサーチスコープ厳守**: policy-researcher / kameyama-researcher 起動時に「依頼スコープに直接答える資料に限定。tool_uses 30回以内」を必ず指示文に含める
- **目標トークン**: 1日3テーマ × フル展開で **300〜500K**（content-pipeline単発90〜170Kの3倍程度）

---

## ohayoスキルとの連結運用（標準フロー）

```
06:00 ohayo cron → ニュース・タスク・市民意見・発信テーマ3案を朝のダッシュボードに表示
07:00 草川がダッシュボード確認、「テーマ01とテーマ02でフルパッケージ作って」と指示
07:01 daily-content-generator 起動
07:30 outputs/daily-content/<日付>/ に全ファイル揃う
07:45 草川が `00_summary.md` を確認、修正/承認
08:00 承認テーマを順次投稿（ブログ・SNS・動画）
```

ohayoが「発見」、daily-content-generator が「実行」。役割分担を明確にする。

---

## nichijoスキルとの住み分け

| スキル | 起点 | 出力 |
|---|---|---|
| **nichijo（コンテンツ抽出モード）** | **当日の活動記録**から抽出 | 1〜複数テーマ案を提示・本文化は別途 |
| **daily-content-generator** | **Notion蓄積資産（政策候補/議会ネタ/市民意見等）**から発掘 | フルパッケージ（全PF原稿完成形） |

nichijoは「今日やったことから派生させる」、daily-content-generatorは「蓄積から戦略的に選んで全展開」。

---

## 拡張（将来追加候補）

- 投稿予約APIへの直接連携（Buffer / Hootsuite / Meta Graph API）
- ショート動画の自動編集指示（CapCutテンプレ出力）
- 投稿後インプレッション取得→翌日の選定ロジックへフィードバック
- 議事録RAG連携で過去答弁との一貫性チェック
- 月次「発信ヒートマップ」（テーマ × 反応量）の自動生成

---

## トリガーフレーズ早見表

| 発火ワード | 想定状況 |
|---|---|
| 「今日の発信」「日次配信」「daily content」 | 朝の通常運用 |
| 「ブログとSNSと動画まとめて作って」 | フルパッケージ要求 |
| 「全チャネル回して」「フル展開」 | 同上 |
| 「今日の発信ネタ選んで全部作って」 | テーマ選定込み |
| 「街頭演説前のメッセージ準備」 | 街宣前準備 |
| 「daily-content-generator」 | スキル名直接指定 |

朝の ohayo から連結起動するのが標準。単独でも起動可能。

---
## 📌 DB統一override（2026-07-05・本文の旧記述より優先）
- **🎯政策候補DB（ds `6f1895ac-` / page b9f8d42a）は凍結済み・新規書込禁止**。🗄️旧アーカイブ内に参照専用で保管（過去分の参照・引用はOK）。
- 政策ネタ・一般質問ネタの**登録/更新はすべて「🎯政策・質問ネタDB（統一パイプライン）」1本**：data_source `42716725-fece-497f-9782-705076539de4` / page `cb47d25e30b14b61b39f56254bf9432a`（🎯政策・質問ハブ=34bcf503-819e配下）。
- 統一DBの使い方：`状況`=収集→未整理→調査中→質問案→提出/通告→実施→完了／`時間軸`=議会直近（3か月以内の議会論点）・中長期（旧政策候補相当）・観察／`ネタ元`に「市政報告会・政策スキャン・AIインタビュー・地域訪問」追加済み。
- 本文中の「政策候補DBへ保存」は「統一DBに時間軸=中長期で保存」と読み替える。凍結DBの案件を再開する時は、その1件だけ統一DBへ昇格させる。
