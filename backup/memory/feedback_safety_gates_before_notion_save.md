---
name: notion
description: 「保存するだけ」は例外にならない。content-fact-checker→content-risk-reviewer を通す前にNotion（📣投稿管理DB等）へ書き込まない
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 47f93789-db16-42a8-b380-0842c4d6553f
  modified: 2026-08-05T10:21:11.142Z
---

drafts/ にある完成版原稿をNotionへ保存するだけの依頼でも、**保存前に content-fact-checker → content-risk-reviewer を必ず通す**。前セッションで通過済みという前提や、ファイルに「FINAL」と付いていることを根拠にしてはいけない。通していないなら「未検証」と明示し、通すか草川の判断を仰ぐまで保存しない。メモ欄に「安全ゲート通過済」と書けるのは、**このセッションで自分が通した時だけ**。

**Why:** 2026-08-05、体育館空調0%の原稿一式（ブログ／SNS7種／ショート動画）をNotionへ保存する際、「保存＝ファイリング」と解釈して両ゲートを飛ばした。結果、草川本人から2度の指摘を受けて初めて検証が動いた。
- 1件目（草川指摘）：「11万5千世帯に避難指示」は避難指示の**対象**世帯数であり避難者数ではない（実避難者は8/5 14時で7,155人）。数字を大きく見せて論を張る形になっていた。
- 2件目（同）：リスクレビューは8軸すべて未実施。事後に回したところ、熊本地震の扱いが草川自身の確立ルール [[feedback_disaster_rescue_phase_no_local_pivot]] と [[feedback_hashtag_policy_x_instagram]] の例外規定に抵触する疑いがHIGHで出た。**先に通していれば書き直し前に分かっていた。**

**How to apply:**
- 保存・投稿・共有など「外に出る側」の操作の直前が唯一のゲート位置。生成直後ではなく保存直前に置く（会話で原稿を直し続けた案件はここが唯一の関門になる）。
- ファクトは一次情報まで遡る。PDFは `pdftotext -layout` で原文照合（[[feedback_no_fabricated_stories]]・D4ルール）。全国集計値は自分で再計算して突合する。
- リスクは8軸を機械的に全部見る。特に**他地域の災害を導入に使った原稿**は [[feedback_disaster_rescue_phase_no_local_pivot]] と地元ハッシュタグの例外を必ず当てる。
- HIGH以上は保存せずASK_USER、CRITICALは即停止。
- 記憶依存の締めは腐る（[[feedback_system_closing_loops_rot]]）。Notion書き込みをPreToolUse hookで機械的に止める方式（`todoist_calendar_guard.py` 相当）を検討する。
