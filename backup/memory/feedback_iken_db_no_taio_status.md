---
name: feedback-iken-db-no-taio-status
description: 📝市民意見リストDBに「対応状況」プロパティは存在しない。未対応の集計は「未完了（要対応）」ビューで行う
metadata:
  type: feedback
---

📝市民意見リスト（永続意見ログ・data_source `c2c34bd8-1e16-492e-aab0-d3f497d18d4d`）の実スキーマに **`対応状況` プロパティは無い**。あるのは 件名／受付ID／受付日／期限／経路／地区／緊急度（高中低）／分類タグ／担当課／対応メモ／次アクション／相談者／連絡先／匿名／関連タスク／関連自治会 など。

未対応・対応中の集計は、DBに用意されている **「未完了（要対応）」ビュー** を使う：
`https://app.notion.com/p/8a36d28a0e1d4fb595a09107f663aa1e?v=b89658fa-0a79-4f00-974a-8ebb71a8055c`

**Why:** oyasumi SKILL.md の Step 1-D／Step 4 は「`対応状況` が `未対応`/`対応中` の全件」と書いているが、その条件でクエリを組むと必ず空振りする。2026-08-21 の夜間runで判明。

**How to apply:** 市民意見の未対応件数を出すときは上記ビューを `notion-query-data-sources` の view モードで叩く。page_size 40 でも `has_more` が返る規模（2026-08-21時点で40件以上）なので、正確な総数が要るならページングする。oyasumi / ohayo / citizen-inquiry-responder の該当記述は要修正。

関連＝[[feedback-oyasumi-blocked-by-content-gate]]
