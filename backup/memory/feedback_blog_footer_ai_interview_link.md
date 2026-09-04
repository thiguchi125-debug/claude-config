---
name: feedback_blog_footer_ai_interview_link
description: ブログ記事の定型フッター末尾にAIインタビューのリンクを常時追加する
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 95a7f255-eb2f-4a17-a89c-a60d61c25b04
---

ブログ記事（深掘り・ノーマル両方）の末尾定型フッターに、既存の◆ご意見箱／◆公式LINE／◆Threadsに続けて **◆AIインタビュー** ブロックを追加する。

リンク: `https://depth-interview-kusagawa.vercel.app/interview/kameyama_shisei_zenpan`

**Why:** 2026-07-14 草川指示「今後はブログ記事の最後のリンクにこのAIインタビューを追加して」。AIインタビュー（安野貴博氏depth interviewベース・[[project_ai_interview_config_designer]]）への導線を全ブログ記事に常設するため。

リンク下には安野貴博氏／有賀啓介氏クレジット＋個人情報禁止の定型注意書き（正本＝正本＝agents/ai-interview-sns-poster.md 📌節の一字一句固定文）を必ず入れる。

**How to apply:** 実装済み＝blog-writer.md／blog-writer-normal.md の「定型フッター（変更禁止）」ブロックにThreadsの後へ◆AIインタビュー段落＋リンク＋※注意書き2行を追記。CLAUDE.md D1のフッター記述も更新済。以後blog-writer系はこのフッターをそのまま出力するので手動追記不要。フッター漏れチェック（[[feedback_blog_blog_normal_footer]]系）でもこの4ブロック目を確認。安野貴博・有賀啓介・個人情報の3語が入っているか確認。
