---
name: feedback_line_500chars_no_hashtag
description: 公式LINE配信は500文字以内・ハッシュタグなし（500字はURL込みで数える）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f6cee28f-1650-4ec3-9b0c-500dc2924d8e
  modified: 2026-07-28T00:32:00.061Z
---

**公式LINEの配信文は500文字以内、ハッシュタグは付けない**（2026-07-28 草川指示）。

**Why:** LINEは長文だとトークルームで折りたたまれて読まれない。ハッシュタグはLINEでは検索・回遊の機能を持たないので、付けても意味がなく文字数を食うだけ。

**How to apply:**
- **500字は URL を含む全体で数える**。go2senkyoのブログURL＝約50字、AIインタビューURL（`depth-interview-kusagawa.vercel.app/interview/...`）＝約76字。リンク2本で126字使うので、**本文に使えるのは実質370字前後**。
- 字数超過時は**リンクを削らず本文を削る**（[[feedback_sns_blog_link_required]]と[[feedback_line_ai_interview_over_form]]でリンク2本は必須のため）。削る順＝①定型の言い回し（「よろしければご一読ください」→「ご一読ください」／「伺った内容は私のもとに届き、市政に活かしていきます」→削除）②修飾句 ③最後に事実。**数字と出所注記（「6月議会の答弁で」等）は最後まで残す。**
- 冒頭は `こんにちは、草川たくやです。`、終止は `皆さんの声、これからもお聞かせください。`（既存仕様）。
- 実例＝2026-07-27 亀山駅前送迎環境のLINE（本文353字＋URL126字＝479字）。
