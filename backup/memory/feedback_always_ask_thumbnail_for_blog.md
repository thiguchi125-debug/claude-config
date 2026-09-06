---
name: feedback-always-ask-thumbnail-for-blog
description: ブログ作成時はサムネ画像（アイキャッチ/OGP）を作るかどうかを必ず1問で尋ねる。勝手に作らない・勝手に省かない
metadata:
  type: feedback
---

ブログを作るとき（spark／content-pipeline／blog-writer(-normal) 直接呼び出しのいずれでも）、本文の承認と同じタイミングで「サムネ画像を作りますか？」を必ず尋ねる。

**Why:** 2026-09-06に草川から「サムネ画像を作成するかどうか必ず尋ねてくれるといいかも」と明示依頼。サムネの要否は記事ごとに変わり、勝手に作ると画像ゲートで燃費が悪く、勝手に省くと投稿時に手戻りする。

**How to apply:** AskUserQuestion 1問（作る／作らない）。「作る」なら content-pipeline のサムネ工程（1600×900・feed-visual-reviewer）へ。既に草川がサムネ要否を言っている場合は聞かない（[[feedback-ask-bundling-and-upfront-reflection]]）。
