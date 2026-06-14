---
name: project_notion_project_platform
description: Todoistプロジェクトに対応したNotion情報蓄積母艦「🗂プロジェクト・プラットフォーム」DB（2026-06-14新設）
metadata: 
  node_type: memory
  type: project
  originSessionId: db89e985-42f1-43bf-87c3-952f2cc20543
---

# 🗂 プロジェクト・プラットフォーム（2026-06-14新設）

**Why:** Todoist＝実行（軽い行動タスク）／Notion＝情報蓄積（経緯・関係者・資料・決定事項）の役割分担を完成させるため、Todoistの主要アクティブPJに対応したNotion蓄積母艦を新設。旧🗂️プロジェクトDB(292cf503・Todoist移行で役割終了)とは別の新規DB。

**How to apply:**
- **DB**: 「🗂 プロジェクト・プラットフォーム」 page=`37a71464-f1b3-4f5e-ad72-128933acf558` / data_source=`8975c6a9-583b-412c-b9f1-fadde30fd565`。親=プロジェクト＆タスク(292cf503a68f802da262d7e0dab4ebf3)。
- **スキーマ**: プロジェクト名(title)／領域(select:🗳選挙2026/🏛議員活動/📋政策・議会/🎪地域・イベント/📣発信)／種別(select:イベント/地区市民相談/選挙WS/政策テーマ/団体・協会/継続案件)／ステータス(select:構想/準備中/進行中/開催待ち/完了/保留)／開催日・期限(date)／優先度(高中低)／関係者(text)／担当課・連携先(text)／Todoistリンク(url=`https://app.todoist.com/app/project/<id>`)／関連Notion(text)／最終更新(auto)。
- **各ページ本文テンプレ**: ## 📌概要 / ## 👥関係者・連絡先 / ## 📅経緯ログ / ## 📂資料・リンク / ## ✅決定事項 / ## ➡️次の一手。← ここに情報を蓄積する。
- **初期投入17PJ（主要アクティブのみ）**: 🎪コスモス祭り2026/🎮eスポーツ/🛹スケートパーク/中庄お祭り/温泉で産後ケア/まちづくり団体/モルック/三重大応援団/川崎文化祭/SKfeelBallet／🏛井田川地区・南部地区・神辺地区(木下)市民相談・山下太陽光・サル対策／🗳9地区訪問・選挙運営人材確保。
- **運用**: Todoist↔Notionの自動同期は不可（手動連携）。Todoistで動かす→Notionに経緯/資料/決定を蓄積。新規の主要PJが立ったら同DBに行を追加（種別=地区市民相談/イベント/政策テーマ等で分類）。

- **スマートインテーク（2026-06-14実装・CLAUDE.md最上位ルール）**: 草川がトピック情報を入力したら、保存先指定が無くても「①正規DB(市民意見/一般質問ネタ/政策候補/報告会)②本DBの該当PJページの📅経緯ログ③Todoist該当箱のタスク」の3面を判定→確認→一括保存する。詳細はCLAUDE.md「情報入力の自動振り分け保存」。
- **既存ページリンク**: 各PJページの📂資料・リンクにmention-page形式で関連既存ページを貼付済（神辺→木下報告会DB／南部→楠平尾報告会＋フォロー／井田川→一般質問ネタ「新団地アクセス複合課題」／eスポーツ→協会2026年間計画）。[[feedback_notion_link_deeplink]]準拠。

関連: [[project_todoist_task_migration]] [[feedback_shisei_houkokukai_voice_capture]] [[feedback_notion_link_deeplink]]
