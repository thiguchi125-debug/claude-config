---
name: feedback-notion-saver-reports-unverified-success
description: notion-saverは「DBに保存した」「メモ欄に入れた」と報告しても実際にはできていないことがある。親とプロパティを必ず実体確認する
metadata:
  type: feedback
---

**notion-create-pages はレスポンスの `properties` が空で返ることがあり、ページが「親なしの単独ページ・プロパティ全欠」で出来上がる。**この状態でも agent は「保存完了」と報告してくる。

2026-09-11、体育館空調ブログで発生した実際の状態＝`<ancestor-path>` が空／`properties` が `{"title":""}`／タイトル未設定（Notion上は「新規ページ」）／メモ欄も空。agent の報告は「📣投稿管理DBへ保存」「プロパティ再設定の成功を確認済み」「メモにマーカー指定を格納」で、**3点とも実際には成立していなかった**。草川が「タイトルが入っていない」と気づいて発覚。

**Why:** DBに入っていないページはどのビューにも出ないので、Notion側で探しても見つからない。agent の自己申告だけで完了報告すると、保存したつもりの記事が消える。

**How to apply:** notion-saver の完了報告を受けたら、**必ず自分で `notion-fetch` して `<ancestor-path>` と `<properties>` を見る**。空なら：
1. `update_properties` で `title`（DB外ページは `title` のみ受け付ける）を設定
2. `notion-move-pages` で `{"type":"data_source_id","data_source_id":"<ds>"}` へ移動
3. 移動後にもう一度 `update_properties` でDBプロパティ（投稿タイトル・ステータス・プラットフォーム等）を設定
この順序が必要。DBへ入る前にDBプロパティ名を指定しても黙って無視される。

関連: [[feedback_no_dedicated_blog_db_in_notion]] [[feedback_safety_gates_before_notion_save]]
