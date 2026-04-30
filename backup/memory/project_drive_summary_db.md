---
name: 📂Drive資料サマリDB & oyasumi/ohayo連携
description: 2026-04-30新設。Google Drive当日更新ファイルをoyasumiが自動収集・要約してDB蓄積、翌朝ohayoが「昨日の新規資料」として表示するフロー。重複は file_id で除外
type: project
originSessionId: f09357e6-3bd1-4d7c-9962-262ae8266731
---
# 📂Drive資料サマリDB & oyasumi/ohayo連携

2026-04-30 新設。「Driveに保存した資料が翌朝のブリーフィングで一覧できないか」というユーザー要望から実装。

## DB
- **タイトル**: 📂 Drive資料サマリ
- **DB top-level ID**: `8815412449ad4de5b3b57145513309df`
- **data_source_id**: `317c4d02-ac0a-48c3-9fc5-56029000e64e`
- **親ページ**: 📔 夜のまとめ（デイリーサマリ）`34ecf503-a68f-8182-99d3-fabb7e7c4c5e`
- **DB URL**: https://app.notion.com/p/8815412449ad4de5b3b57145513309df

## スキーマ（プロパティ）
- `ファイル名`（TITLE）
- `ファイルID`（TEXT）— **重複除外キー**。Google Drive File ID。これでDB全件マッチさせて再登録を防ぐ
- `更新日時`（DATE+datetime）— Driveの `modifiedTime`
- `MIMEタイプ`（SELECT）— PDF/Google Doc/Sheet/Slide/Word/Excel/PowerPoint/Image/Text/その他
- `ファイル容量MB`（NUMBER）
- `Drive URL`（URL）
- `要約`（RICH_TEXT）— 200〜400字、議員業務視点
- `議会活用メモ`（RICH_TEXT）— 一般質問ネタ／市民意見連動／政策候補化候補
- `登録日`（DATE）— oyasumiが処理した日
- `ソース`（SELECT）— oyasumi自動／nichijo手動／手動追加
- `処理ステータス`（SELECT）— 要約済／要約失敗／スキップ／未処理

## oyasumi 側のフロー（追加箇所）
1. **Step 1-E（並列収集）**: `list_recent_files` (orderBy=lastModified, pageSize=25) → modifiedTime=今日(JST)で絞り込み → 📂DBの過去7日file_ID群と突合し既登録は除外 → 上限10件
2. **Step 5.5（新設）**: 各新規ファイルを `read_file_content`（先頭3000字）→ 議員業務視点で200〜400字要約 → 議会活用メモ抽出（該当時のみ）→ 📂DBへ create_pages
3. **Step 6 サマリ**: 「📂 本日のDrive新規資料」セクションを追加（要約済 N件＋失敗K＋スキップS）

## ohayo 側のフロー（追加箇所）
1. **Step 3-4c（新設）**: 📂DBを `登録日=昨日` で query → ファイル名・要約・議会活用メモ・URLを抽出
2. **セクション2.8（新設）**: 朝のダッシュボードに `## 📂 昨日のDrive新規資料` セクションを差込（位置：選挙進捗の直後）
3. **チャット出力**: 「📂 昨日のDrive新規資料」セクションを追加（最大5件、残りはDB誘導）

## Why
- Driveに資料を保存しても放置されがちだった。翌朝に「あの資料こんな内容」と一覧で見えるとリマインドが効く
- 議員業務視点の要約があれば「これは一般質問ネタ／政策候補ドラフト化候補」と即判断できる
- file_idでの重複除外により、過去ファイルを開き直しただけのケースは取りこぼさず、かつ二重登録もしない

## How to apply
- Drive全体を監視対象（フォルダ絞り込みなし）。多すぎる日が出たら exclude pattern 追加で対応
- `list_recent_files` は所有・閲覧した全ファイルを返すので、必ず modifiedTime=今日 でフィルタ（viewedByMeTime のみ今日のファイルは除外）
- 要約は議員業務視点（亀山市政・議会・市民相談・政策候補・選挙のどれに関連するか）。汎用要約ではない
- 上限10件を超えた場合は `処理ステータス=スキップ` で件数だけ集計（要約処理を毎晩無限に走らせない）
- 失敗時は他ファイル処理を止めない（fail-safe）

## 既知の落とし穴
- **タイムゾーン**: Driveは UTC、JST 当日 00:00 = UTC 前日 15:00。modifiedTime のフィルタで間違えると前日分を取り込む／当日分を逃す
- **list_recent_files の癖**: orderBy=`lastModified` でも、自分が編集していないファイル（共有Drive内・他者編集）も拾う。ノイズと判断したら exclude pattern 追加
- **大型ファイル**: 動画・大型バイナリ等は `read_file_content` 失敗するので `要約失敗` ステータスで登録（メタ情報のみ）

## 派生タスク
- 監視フォルダの絞り込みが必要になったら oyasumi Step 1-E に exclude/include filter 追加
- DBに政策候補DB / 一般質問ネタDB / 市民意見DBへのリレーションを追加するとライフサイクル連携できる（v2）
