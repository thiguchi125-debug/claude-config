---
name: news-briefing-gate-scope
description: news-briefing v4-local をレビューするとき、drafts の txt だけ見ると 議会活用メモ が未検査で通過する。Notionページ側も必ず突合する
metadata:
  type: feedback
---

news-briefing v4-local の成果物をレビューするときは、drafts/ の txt 4本だけでレビューを完了させない。各ニュース項目の Notion ページには `議会活用メモ`（1項目200〜300字・①草川過去発言 ②亀山現状ギャップ ③問い立て）と `概要` プロパティがあり、**これらは draft txt に書き出されない**。

**Why:** 2026-08-28分の実査で、draft txt には存在しない亀山市職員の実名（産業環境部の参事氏名）が Notion ページの `議会活用メモ` にだけ入っていた。CLAUDE.md「Notion保存も『発信』＝保存前に安全ゲート」に対し、ゲートが本文の一部しか覆っていない構造欠陥。fact-checker も同じ穴を通過している（未レビュー領域の固有名詞は裏取りされていない）。

**How to apply:** news-briefing 由来のレビュー依頼を受けたら、(1) draft txt をレビューし、(2) ダイジェスト内の `[Notion](...)` リンクを最低でも亀山・三重カテゴリの全件 fetch して `概要` と `議会活用メモ` を突合する。差分があれば「ゲート範囲の乖離」として指摘し、恒久対策として v4-local の draft 書き出しに `議会活用メモ` 全文を含めるよう提案する。

関連: [[shokuin-jitsumei-naibu-taigai]]
