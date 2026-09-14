---
name: feedback_blog_obsidian_annotate_notion_final_only
description: "ブログは作業中の正本をObsidian vault 50_発信/ブログ/に置き #注記で直す。Notionには「完成」後に完成版だけ1回保存"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ac17d186-dee6-4222-9454-35f7b99680ff
  modified: 2026-09-14T03:41:37.635Z
---

2026-09-14 草川指示「ブログ記事もobsidianの注記で編集できるように仕組みを整えて　完全に完成版だけnotion保存」（西野公園プール記事でNotion保存済みv2に修正が入った時）。

**Why:** 途中版をNotionに保存すると草川はNotion上で読んで直すことになり、注記の置き場がなく往復も重い。Notionは完成後の鏡（[[obsidian-vault-workflow]]）。

**How to apply:**
- 原稿は `~/Documents/ObsidianVault/50_発信/ブログ/<日付>_<テーマ>_v<n>.md` → `obs_open.sh` で開く。手順の正本＝同フォルダ README.md／OPERATIONS.md【C】D6
- 「注記入れた」→ `grep -n "#注記"` → 上書きせず次版＋冒頭に注記対応表
- 安全ゲート・貼り付けHTML・Notion保存は草川の「完成」の後に1回ずつ。完成前にNotionへ保存・上書きしない
- 関連 [[feedback-blog-paste-html-is-the-delivery-step]] [[feedback_safety_gates_before_notion_save]]
