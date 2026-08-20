---
name: feedback-oyasumi-blocked-by-content-gate
description: 無人夜間runのoyasumiはcontent_safety_gateにcreate-pagesを止められ、デイリーサマリと週次レポートをNotionに作れない
metadata:
  type: feedback
---

`~/.claude/hooks/content_safety_gate.py` の免除は **update-page の3ページID限定**（📥未分類インテーク / 📮SNS便ステータス / 🌅朝のダッシュボード `722beb9e...`）と「🔖台帳行だけの本文」だけ。**create-pages は「新規は必ず検査」で免除対象外**。

そのため headless の oyasumi は Step 6（デイリーサマリ）と Step 7（週次レポート）の `notion-create-pages` が必ず deny される。gate.py の `--pass` は「content-fact-checker と content-risk-reviewer をこのセッションで実際に通した」という宣言であり、無人runで自己申告して突破してはいけない（2026-08-06 a2 の事故が根拠）。

**Why:** 2026-08-21 01:09 の夜間runで実際に発生。ゲートは「市民が読む文章」を止める設計だが、内部集約ログのデイリーサマリまで巻き込んでいる。2026-08-11に同種の事故（未分類インテークへ退避できず育休退園の相談が宙に浮いた）があり EXEMPT_PAGES が作られたが、デイリーサマリは救われていない。

**How to apply:** 無人runでは create-pages を強行せず `~/outputs/oyasumi/<日付>/` にmd保存し、朝のダッシュボード（免除対象）の「📔 昨夜のまとめ」にローカルパスと要対応を書いて草川へ引き継ぐ。恒久解は EXEMPT_PAGES ではなく「親ページが 📔夜のまとめ `34ecf503-a68f-8182-99d3-fabb7e7c4c5e` / 📅週次レポート `34ecf503-a68f-81b0-9275-d34249f59cf6` の create-pages を免除する」条件を hook に足すこと（どちらも公開経路なし）。草川の承認が要る。

関連＝[[feedback-safety-gates-before-notion-save]]／[[feedback-gate-json-concurrent-overwrite]]
