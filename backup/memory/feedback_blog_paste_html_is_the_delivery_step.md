---
name: feedback-blog-paste-html-is-the-delivery-step
description: ブログは「貼り付け用HTMLをブラウザで開く」まで作って初めて納品。Notionからのコピペは ** が生で出て緑マーカーも落ちる
metadata:
  type: feedback
---

**ブログ制作の最後の工程は「貼り付け用HTMLを生成してブラウザで開く」まで。**ここまでやらないと納品ではない（2026-09-11 草川指示「ハイライト付きでhtml表示するところまで一連の流れに加えて」）。

**Why:** Notionページからブログ編集画面へコピペすると、①`**太字**` が**記号のまま生で入る**②緑の蛍光マーカーが落ちる。草川の言葉では「最悪」。Notionは保管用であって、貼り付け元ではない。

**How to apply:** 本文が両ゲート＋gate.pyを通ったら、Notion保存と**並べて**必ずこれを実行する。

```
python3 ~/.claude/scripts/blog_paste_html.py <draft.md> --marks <marks.txt> \
  --label "<テーマ> v<n>・<日付>" -o ~/outputs/blog-marking/<日付>_<テーマ>_blog_paste.html
open <出力先>
```

- `marks.txt` ＝蛍光マーカーを引く一文を1行1本、**原稿のmarkdown表記のまま完全一致**で書く（規則＝[[feedback_blog_marker_rules]] 明るい緑1色・1章1本・全7本・「判断が変わる一文」だけ）。スクリプトは未一致を警告し、全部当たらなければ exit 1 を返す
- 出力は `~/outputs/blog-marking/` に集約（既存の型＝`<日付>_<テーマ>_blog_paste.html`）
- 見出しは `h3` ＋「■ 」＋左のライムバー、マーカーは `background-color:#c6f8c2`、本文の `**` は `<strong>` に変換される
- 本文中の `【画像：…】` 行は**赤い破線の枠**になる。ブログ編集画面でその枠ごと画像に差し替える
- 草川への案内は「上部の枠の下から末尾までを選択してコピー」。**Notionから取らない**ことを毎回添える

関連: [[feedback_blog_marker_rules]] [[feedback_no_dedicated_blog_db_in_notion]] [[feedback_safety_gates_before_notion_save]] [[feedback_open_folder_after_generating_files]]
