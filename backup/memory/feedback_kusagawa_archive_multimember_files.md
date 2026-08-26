---
name: feedback-kusagawa-archive-multimember-files
description: kusagawa_archiveの01_council配下には草川以外の議員の質疑を丸ごと含む「その日の一般質問全体」ファイルが混ざっており、ファイル名では見分けられない
metadata:
  type: feedback
---

`01_council/mydrive_一般質問1令和7年12月10日_Rgugss.txt` のような**日付だけの通し会議録**は、草川以外の議員の質疑ブロックを丸ごと含む。ファイル名に `kusagawa` / `草川` が入っていないものは全議員分と考えてよい。

**Why:** 2026-08-27 の news-briefing で、このファイルから「健康都市を宣言している亀山市における予防医療の推進」「COPD」「骨粗鬆症検診は40歳から5歳刻み」を草川の過去発言として引きかけた。話者行を遡ったところ **すべて森美和子議員（12番）の質疑**だった。grepのヒット行だけを見ると草川の発言に見えてしまう。

**How to apply:**
- grepでヒットしたら、必ず `awk '/^○/' ` で**直前の話者行**を確認してから引用する。草川は `○４番（草川卓也君登壇）`。
- 確実なのは `01_council/*kusagawa*` `01_council/*草川*` に絞ってgrepすること。第一手はこちら。
- 議長職の `○議長（森 美和子君）` は議事進行であり、他議員の質疑混入とは別物（この行があるだけでは汚染ではない）。

関連: [[feedback-no-other-council-members-names]] [[feedback-read-agent-spec-before-writing]]
