---
name: feedback_notion_sql_plan_gate
description: Notion MCPのSQLクエリ(query-data-sources)はBusinessプラン限定で恒久ブロック。viewクエリは可だがフィルタ欠落の罠。堅牢なのはfetch/search/固定ページパターン
metadata:
  type: feedback
---

2026-07-03確定（実測）: `notion-query-data-sources`（SQLモード）は **「This tool requires a Business plan or higher with Notion AI」で恒久ブロック**（草川のワークスペースは対象外プラン）。`notion-query-database-view` は動くが、**viewに設定されたフィルタの範囲しか返さない**（📰ニュースDBのviewは6/26の3件しか返さず、これがdedup素通り→水道濁り5ページ重複事故の直接原因）。

**Why:** 「DBの全レコードを取りたい」用途にSQLは使えず、viewは不完全。スキル/Routineがこれらに依存すると、プランゲートやviewフィルタ変更でサイレントに壊れる。

**How to apply:**
1. スキル・エージェント・クラウドRoutineで `notion-query-data-sources`（SQL）を**書かない**。
2. 一覧取得が必要な定常処理は「**自己管理の固定ページ**」パターンにする（例: news v3.1のdedupインデックス＋ダイジェスト。書く側が毎回メンテし、読む側はfetch 1回）。
3. 単発検索は notion-search（data_source_url指定可）、単体取得は notion-fetch。
4. viewクエリを使う場合は「そのviewのフィルタで何が欠けるか」を必ず確認してから。
5. 「プラン制約でブロック」と報告する前に、SQLを使っていないか・view URLに?v=があるかを疑う（今朝のohayoはSQLを叩いて「view も駄目」と誤報告した）。

関連: [[project_notion_ohayo_news_v3_renewal]] / [[feedback_news_db_query_pitfall]]
