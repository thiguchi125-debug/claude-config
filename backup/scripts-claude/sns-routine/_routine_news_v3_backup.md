# クラウドRoutine trig_01WXgkt4JqANvhi1YuQLGsEQ v3.1プロンプト退避（2026-07-14・Phase 2更新前のロールバック用）

- name: 毎朝ニュースブリーフィング v3.1 (草川議員 6:00 JST)
- cron: 0 21 * * * (UTC) = 6:00 JST
- model: claude-sonnet-4-6
- mcp_connections: Notion のみ（Gmail未接続＝iJAMP枠は実行されていなかった）
- allowed_tools: Bash, Read, Write, WebSearch, WebFetch, mcp__Notion__notion-create-pages, mcp__Notion__notion-search, mcp__Notion__notion-fetch, mcp__Notion__notion-update-page

## プロンプト全文（v3.1）

# 草川たくや 朝のニュースブリーフィング v3.1（2026-07-03再構築・クラウドRoutine 6:00 JST）

毎朝6:00 JST（UTC 21:00）に動く自動収集Routine。3カテゴリ・合計3〜7件厳選でNotion📰ニュースDBに登録し、固定のダイジェストページを更新する。

**v3.1の背景（重要）**: 旧v3はdedup照合にDB viewクエリを使っていたが、viewのフィルタで過去ページが見えず重複登録事故（水道濁り5ページ目）を起こした。v3.1は**DBクエリゼロ**で動く：重複照合は自己管理の「dedupインデックス」ページ1枚、朝の読み出しは「ダイジェスト」ページ1枚。

## 固定ページ（ID直指定・変更禁止）
- 📰ニュースDB（登録先）: data_source_id `29e5c1a2-d64d-4822-81fd-0d642c3f07bc`
- 📰dedupインデックス（重複照合）: page `391cf503-a68f-8110-88a7-c5a70e6741c8`
- 📰今朝のニュースダイジェスト（ohayoが読む）: page `391cf503-a68f-8194-be35-fec5aede8a5e`

## 絶対ルール
- ❌ `notion-query-data-sources`（SQL）は**使用禁止**（Businessプラン限定でブロックされる）
- ❌ DB viewクエリも使わない（フィルタで欠落する）。使うのは fetch / search / create-pages / update-page のみ
- ❌ 新規登録の前に必ずdedupインデックス照合。インデックスが読めない場合は**新規登録を中止**しダイジェストにエラーを書く（重複を出すくらいなら登録しない方がマシ）
- Bashで `TZ=Asia/Tokyo date '+%Y-%m-%d (%a)'` を実行して本日と曜日を取得（曜日誤記防止）

## Step 0: dedupインデックス読込（1 fetch）

`notion-fetch` page `391cf503-a68f-8110-88a7-c5a70e6741c8`。「継続案件の正ページ」リストと直近30日の登録行（`日付 | 見出し | テーマキー | 記事URL | NotionページURL`）を取得。

## Step 1: 並列リサーチ（WebSearch 4〜5本を1メッセージ並列）

- **A. 亀山・三重**（最大2件・人命安全最優先）: `亀山市 ニュース`と`亀山市 OR 関町 OR 井田川 site:city.kameyama.mie.jp OR 中日新聞 OR NHK三重`の2本。**検索結果が薄い日は`三重県 ニュース 今日`で県域に広げて0件を回避**
- **B. 関心テーマ**（曜日ローテ・1〜2件）: 月=子育て/火=教育/水=都市計画/木=医療健康/金=防災/土=AI・行政DX/日=亀山強化。検索語は「省31日以内の新着が出る具体語」で（例: 金「防災 自治体 新制度 2026」）
- **C. 国政動向**（最大1件・週1制限）: 省庁報道発表 1本

有望URLだけWebFetch（並列）。**本文で配信日を確認し、48時間以内の新着でなければ除外**。古い事案の蒸し返し記事（まとめ記事・振り返り記事）は「新しい事実があるか」で判断し、新事実なしなら除外。

## Step 2: 3層重複判定（全候補必須）

- **Layer 1**: 記事URLがインデックスのURLと一致 → 即除外
- **Layer 2**: 見出しがインデックスの見出しと主要キーワード70%以上一致 → 新規禁止、該当Notionページに続報追記（`notion-update-page` insert_content 末尾：`---\n## 続報（YYYY-MM-DD）\n新規情報1〜2文\n→ 元記事: URL`）
- **Layer 3**: インデックスの「継続案件の正ページ」テーマ（水道濁り・太陽光条例・シャープ売却・鈴鹿川水難・新名神事故・防災庁・誰でも通園・駅前信号機・新防災気象情報）に該当 → 同じく正ページに続報追記のみ
- **Layer 4**: 「【国政動向】」はインデックスに過去7日分があれば新規禁止（月曜のみ新規可）

## Step 3: 新規分をDB登録（1回のcreate-pages）

parent: `{"data_source_id": "29e5c1a2-d64d-4822-81fd-0d642c3f07bc"}`。properties: `見出し`(60字以内)／`date:日付:start`=今日(JST)・`date:日付:is_datetime`=0／`カテゴリ`=`亀山市・三重県`/`国政・自治体`/`関心テーマ`の3択／`関心テーマ`(multi)／`情報源`／`userDefined:URL`（実在確認済のみ）／`概要`(80字)／`亀山関連度`(★1〜5)／`議会活用メモ`（①草川過去発言の有無=notion-searchで確認して1文②亀山市現状ギャップ=計画名/条例/統計/所管課の1つ以上③問い立てor次アクション1つ）／`活用`=`演説`/`SNS`/`一般質問`/`ブログ`/`静観`（全件必須）／`ステータス`=`新着`。

## Step 4: ダイジェスト更新（ohayoが読む唯一の出口）

page `391cf503-a68f-8194-be35-fec5aede8a5e` を `notion-update-page` replace_content で**本日分に全置換**（冒頭の説明段落は残す）：
```
毎朝6時のニュース収集Routine（v3.1）が本日分を全置換する固定ページ。ohayoが毎朝この1ページだけを読む（DBクエリ不要）。手動編集禁止。

## YYYY-MM-DD（曜）✅ 新規N件・続報M件・除外K件

### 新規
- [★4] 見出し（情報源・配信日）→ 活用: 演説 — 概要80字 — 議会活用メモの③を1行 — [記事](URL) / [Notion](ページURL)

### 続報（既存ページに追記済み）
- 案件名: 新情報1文 → [Notion](正ページURL)

### [dedup判定ログ]
- 候補名: Layer判定結果と最終アクション（1行ずつ）
（エラーがあった場合は冒頭に 🚨行）
```

## Step 5: dedupインデックス更新＋ライフサイクル

1. 本日の新規分を「直近登録」に追記（`日付 | 見出し | テーマキー | 記事URL | NotionページURL`）。30日超の行は削除。新しい継続案件を検知したら「継続案件の正ページ」にも追加。
2. インデックス上の**7日超過ページ**のうちステータスが`新着`のものを `notion-update-page` update_properties で `確認済` に変更（最大5件/日・殩れ防止の漸進処理）。

## 完了ログ（stdout）
`✅ news-briefing v3.1 完了 新規N・続報M・除外K・確認済遷移L`

## ロールバック手順
RemoteTrigger update trig_01WXgkt4JqANvhi1YuQLGsEQ で job_config.ccr.events[0].data.message.content を上のプロンプト全文に戻し、mcp_connectionsをNotionのみに、modelをclaude-sonnet-4-6に戻す。
