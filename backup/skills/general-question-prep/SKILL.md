---
name: general-question-prep
description: 草川たくや（亀山市議会議員）の一般質問準備プラットフォーム。議会会期ハブ×ネタDB×17エージェントを束ね、kickoff／research／interview／draft／review の5モードで会期単位の準備工程を再現性高く回す。「6月議会キックオフ」「会期立ち上げ」「<テーマ>を調査」「<テーマ>の聞き取り設計」「<テーマ>の通告書を作って」「議会前夜チェック」「振り返り」などで起動。
---

# /general-question-prep スキル

草川たくやの一般質問準備を**会期ハブ単位**で運用するオーケストレーションスキル。

## 基本思想

- **会期ハブ駆動**: 🏛議会会期ハブDB 1ページ ＝ 1会期、ロードマップ／テーマ枠／聞き取り／リハーサル／振り返りを集約
- **既存資産結線**: ネタDB／政策候補DB／市民意見BOX／タスクDB／17エージェントは触らず束ねるだけ
- **5モード分岐**: ユーザー発言から kickoff / research / interview / draft / review のいずれかを判定
- **ガードレール継承**: D5リサーチスコープ・草川発言＋市答弁のみ抽出・他議員名禁止・追及型表現禁止・fact-checker/risk-reviewer通過必須

## 起動モード判定

| モード | トリガー語例 |
|---|---|
| kickoff | 「6月議会キックオフ」「会期立ち上げ」「会期準備スタート」 |
| research | 「<テーマ名>を調査」「research」「リサーチして」 |
| interview | 「<テーマ名>の聞き取り設計」「ヒアリング計画」「インタビュー設計」 |
| draft | 「<テーマ名>の通告書を作って」「原稿化」「通告書ドラフト」 |
| review | 「議会前夜チェック」「振り返り」「答弁ログ」 |

判定不能時は最初に確認：
```
モードを選んでください：
1. kickoff（会期立ち上げ・テーマ候補出し）
2. research（テーマごとに4エージェント並列調査）
3. interview（聞き取り計画／AIインタビュー設定）
4. draft（通告書→本番原稿→想定答弁）
5. review（前夜マニュアル／事後振り返り）
```

## Notionリソース

| 用途 | data_source_id |
|---|---|
| 🏛議会会期ハブDB | `16842e7f-f34f-4242-a68c-fb59efcc2bc1` |
| 🏛議会会期ハブDB page URL | https://www.notion.so/61bebeba2d814946bf8d817cd9dd3fcf |
| 📝一般質問ネタDB | `42716725-fece-497f-9782-705076539de4` |
| 🎯政策候補DB | `6f1895ac-3373-43b8-97d7-7ee4aa2791e0` |
| 📝市民意見リスト（永続意見ログ・現行）| `c2c34bd8-1e16-492e-aab0-d3f497d18d4d` |
| ✅タスクDB | `292cf503-a68f-81c6-b9dd-000b3ffdd2ce` |
| 🗂️プロジェクトDB | `292cf503-a68f-81fe-bd40-000b64314f2e` |

## 🏛議会会期ハブDB プロパティ実装メモ

`質問時間（分）` は実装上 `質問時間` という名前で作成されている（() がプロパティ名に含まれると update_page 等で扱いにくいため）。COMMENT='答弁込み45分' で意味は確定。**SKILL内で property 更新する際は必ず `質問時間` を使うこと。**

`フェーズ` は SELECT 型で実装（STATUS 型はDDLで初期オプション設定不可のため）。値は `kickoff` `research` `interview` `draft` `review` `完了` の6種類。

## 共通ガードレール

- D5 リサーチスコープ厳守（tool_uses 30回以内目安）
- 議事録は草川発言＋市答弁のみ抽出
- 他議員の名前を本番原稿に載せない（中立紹介はOK）
- 「次の議会で追及」型表現禁止
- draft モードは保存前に content-fact-checker → content-risk-reviewer 通過必須

---

## モード分岐の実装

### 共通前処理

1. ユーザー発言からモード判定（trigger語マッチ）
2. 判定不能なら上記「モードを選んでください」を提示
3. モード確定後、対応する Step セクションへジャンプ。**ただし 2026-05-12 時点では kickoff モードのみ実装済。research / interview / draft / review が指定された場合は「現在 Phase C-1（kickoffのみ）実装段階です。テーマ確定後、Phase D-1 以降の追記をお待ちください（plan: 2026-05-12-ippan-shitsumon-prep-platform-plan.md）」と返して終了する。**
4. 各モード終了時、🏛議会会期ハブDB の「フェーズ」プロパティを次フェーズへ進める
   - kickoff 完了 → research
   - research 完了 → interview
   - interview 完了 → draft
   - draft 完了 → review
   - review 完了 → 完了

### モード別実行 Step

詳細は本ファイル下部の `## kickoff モード` `## research モード` `## interview モード` `## draft モード` `## review モード` 各セクション参照。

---

## kickoff モード

**目的:** 新会期の会期ハブページ整備＋ネタDBからテーマ候補10〜15件を草川に提示してテーマ2〜3本を確定。

### 入力

- 会期名（例: 「2026年6月議会」）
- 通告締切日
- 本会議日（範囲）
- 一般質問予定日（任意）

### Step 1: 会期ハブページ存在確認

会期ハブDBを `mcp__claude_ai_Notion__notion-fetch` で取得（data_source_id: `16842e7f-f34f-4242-a68c-fb59efcc2bc1`）し、`会期名` 列で入力会期名と一致するページがあるか確認：

- 該当ページ無し → Step 2 へ
- 該当ページ有り → Step 4 へ（既存ページ流用）

### Step 2: 会期ハブページ create

```
mcp__claude_ai_Notion__notion-create-pages
  parent:
    type: data_source_id
    data_source_id: 16842e7f-f34f-4242-a68c-fb59efcc2bc1
  pages:
    - icon: "🏛"
      properties:
        会期名: <入力会期名>
        date:通告締切:start: <入力>
        date:通告締切:is_datetime: 0
        date:本会議日:start: <入力開始>
        date:本会議日:end: <入力終了>
        date:本会議日:is_datetime: 0
        date:一般質問日:start: <入力 / 任意>
        date:一般質問日:is_datetime: 0
        質問時間: 45
        フェーズ: "kickoff"
      content: <ロードマップ5セクションテンプレ（A-3 6月議会ページと同形式）>
```

⚠️ プロパティ名は `質問時間`（「（分）」なし）。`質問時間（分）` で update_page を呼ぶと property-not-found エラーになる。

### Step 3: ロードマップを通告締切から逆算で埋める

通告締切を D とすると：
- D-21〜D-20：kickoff
- D-20：テーマ確定
- D-19〜D-14：research
- D-13〜D-9：interview
- D-8〜D-3：draft
- D-2〜D-1：最終確認
- D：通告日
- 本会議日：review（前夜・事後）

メモプロパティに自動算出した日付テーブルを書き戻す。

### Step 4: ネタDBから候補10〜15件抽出

📝一般質問ネタDB (ds: `42716725-fece-497f-9782-705076539de4`) を `notion-query-database-view` または `notion-search` で：
- ステータス: 調査中／質問案／未整理／収集 のいずれか
- 優先度: high > medium > low の順
- 更新日: 新しい順
- 上限30件取得

抽出後、以下3軸で並べ替えて10〜15件に絞る：
1. **優先度**（high > medium > low）
2. **分野バランス**（子育て／教育／福祉／DX／インフラ／産業／まちづくり／防災から最低4分野）
3. **市民意見熱量**（📝市民意見リスト `c2c34bd8-` で同テーマ言及数 = タイブレーク用。旧 `354432ec-` 受付BOXは2026-05-02廃止済）

### Step 4.5: 答弁・約束台帳から回収候補を抽出（toben-tracker連携・2026-07-08追加）

`~/.claude/agents/knowledge/kusagawa_archive/07_commitments/ledger.json` を読み、以下に該当するレコードを回収候補として抽出：

- status が `未回収` / `進行中` / `停滞` のいずれか
- かつ due_hint が今会期（例: 「2026-09議会」）・今年度予算・直近の計画改定に一致、または経過2会期以上

ファイルが無い・records が空なら本Stepはスキップ（エラーにしない）。詳細スキーマは同ディレクトリ SCHEMA.md。

### Step 5: 候補一覧を草川に提示

チャットに以下を出力：

```
🏛 <会期名> kickoff
通告締切: <D>（残<X>日）

【📌 回収候補（過去答弁の約束・台帳より）M件】
R. <テーマ> | <答弁者>が「<引用20字>…」（<会期>・<type>） | 状態: <status>
   → 今会期で進捗を質すか、テーマ候補に昇格するか

【テーマ候補 N件】
1. <テーマ名> | 分野: <X> | 優先度: <Y> | 市民意見ヒット数: <Z>件
   背景: <30字>
   過去発言: <あり/なし>
   想定答弁難度: <◎○△×>
2. ...

→ 草川さん、2〜3本選んでください（番号またはテーマ名で指定）
```

### Step 6: 草川判断後の確定処理

選定テーマごとに以下を実行：

1. ネタDB該当ページの「会期ハブ」relation に `<会期名>` のページを紐付け
2. ネタDB該当ページのステータスを `質問案` に更新
3. ネタDBページ本文に8セクション骨子を末尾に append（既存本文がある場合は **本文末尾に追記** ／既存本文への破壊的書き込み禁止）
4. 🏛会期ハブページの「テーマ枠」 relation に該当ページを追加
5. 🏛会期ハブのフェーズを `research` へ進める：
   ```
   mcp__claude_ai_Notion__notion-update-page
     page_id: <会期ハブページid>
     command: update_properties
     properties: { フェーズ: "research" }
   ```
6. ✅タスクDB (ds: `292cf503-a68f-81c6-b9dd-000b3ffdd2ce`) に research フェーズの主要タスクを inbox 登録
   - 「<テーマ>: 4エージェント並列調査実施（5/14〜5/19）」期限 D-14
   - 「<テーマ>: 所管課ヒアリングアポ取得」期限 D-13

### Step 7: 8セクション骨子テンプレ

ネタDB該当ページ本文末尾に以下を append：

```
---

## 1. 論点サマリ
（30〜60字で問いを1文化／背景3行）

## 2. 草川の過去発言（archive grep結果）
（policy-archive-miner 自動追記・research モードで埋まる）

## 3. 国・他自治体動向
（policy-researcher 自動追記・research モードで埋まる）

## 4. 亀山の現状（数値・計画・条例）
（kameyama-researcher 自動追記・research モードで埋まる）

## 5. 聞き取りログ
- AIインタビュー: （URL貼付）
- 所管課ヒアリング: 日時／参加者／質問項目／回答要旨
- 市民意見ピックアップ: 📝市民意見リスト（`c2c34bd8-`）からrelation

## 6. 通告書ドラフト
（council-material-creator 自動追記・draft モードで埋まる）

## 7. 本番原稿
（council-material-creator 自動追記・5000〜8000字・draft モードで埋まる）

## 8. 想定答弁＋再質問カード
（counter-argument-simulator 自動追記・draft モード後半／review 前夜で埋まる）
```

完了後、kickoff モードを終了し、フェーズを research に進めた旨を草川に報告（Step 6 の処理サマリを出力）。

---

（D-1 research／E-1 interview／F-1 draft／G-1 review は将来追記）

---
## 📌 DB統一override（2026-07-05・本文の旧記述より優先）
- **🎯政策候補DB（ds `6f1895ac-` / page b9f8d42a）は凍結済み・新規書込禁止**。🗄️旧アーカイブ内に参照専用で保管（過去分の参照・引用はOK）。
- 政策ネタ・一般質問ネタの**登録/更新はすべて「🎯政策・質問ネタDB（統一パイプライン）」1本**：data_source `42716725-fece-497f-9782-705076539de4` / page `cb47d25e30b14b61b39f56254bf9432a`（🎯政策・質問ハブ=34bcf503-819e配下）。
- 統一DBの使い方：`状況`=収集→未整理→調査中→質問案→提出/通告→実施→完了／`時間軸`=議会直近（3か月以内の議会論点）・中長期（旧政策候補相当）・観察／`ネタ元`に「市政報告会・政策スキャン・AIインタビュー・地域訪問」追加済み。
- 本文中の「政策候補DBへ保存」は「統一DBに時間軸=中長期で保存」と読み替える。凍結DBの案件を再開する時は、その1件だけ統一DBへ昇格させる。
