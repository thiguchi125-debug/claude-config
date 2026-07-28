---
name: feedback_sns_blog_link_required
description: 連動ブログがあるSNS投稿は公式LINE・Threads・Xに必ずブログURLを入れて閲覧を促す（媒体別の置き場所つき）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f6cee28f-1650-4ec3-9b0c-500dc2924d8e
  modified: 2026-07-28T00:09:12.523Z
---

連動するブログ記事がある発信では、**公式LINE・Threads・X に必ずブログURLを入れて閲覧を促す**（2026-07-28 草川指示）。プレースホルダ（`[ブログ公開URL]`）のまま納品しない。

**媒体別の置き場所**

| 媒体 | 置き場所 |
|---|---|
| Threads | 自己リプライ |
| X | リプライ欄（本文には入れない。リーチが落ちるため [[feedback_x_post_lean_one_message]] と整合） |
| 公式LINE | **本文末尾**（コメント欄がないため。ご意見箱リンクの前に置く） |
| Facebook | 投稿者自身のコメント |
| YouTube・TikTok | ピン留めコメント |
| Instagram | キャプションにリンクが効かないため「詳しくはプロフィールリンクのブログへ」のまま |

**Why:** SNSは尺・字数の制約で結論しか書けず、数字の出所や他自治体の事例といった裏付けが落ちる。ブログに全文があるのに導線がないと、いちばん説得力のある部分が読まれないまま終わる。LINEだけコメント欄がないので本文に入れる必要があり、機械的に「コメント欄へ」と処理すると抜ける。

**How to apply:**
- ブログURLは **go2senkyo形式** `https://go2senkyo.com/seijika/168135/posts/<id>`（`168135` が草川のID）。Notion投稿管理DBの公開URLプロパティから取得する。
- 文面の型＝「ブログに全文をまとめました。よろしければご一読ください。」＋URL。LINEは本文の流れに馴染ませて「質問と答弁のやり取り、他の自治体の事例まで、ブログに全文をまとめました。」のように中身を一言添える。
- ブログ未公開でURLが取れない段階では、SNS側を先に確定させず**ブログ公開→URL取得→SNS差し込み**の順にする。プレースホルダで保存すると差し替え忘れが起きる。
- 実装は `~/.claude/agents/sns-content-creator.md` 末尾の恒久ガードルール節に常駐（[[feedback_rules_reside_in_agents]]）。
