---
name: notion-createdtime-is-utc
description: Notion createdTime（SQL直クエリ／APIの…Z値）はUTC。JSTに直さず日付として読むと日付・経過日数・件数が最大9時間ぶんずれる。夜間SNSパック等の日次ジョブで実害が出た
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 609dd889-c864-47fa-b987-2e425783de67
  modified: 2026-08-14T01:06:34.614Z
---

Notion の `createdTime`（`notion-query-data-sources` の SQL 直クエリや API が返す `...Z` 付きの値）は **UTC**。
`date(createdTime)` や「YYYY-MM-DD 部分だけ見る」でJST日付として扱うと、**JST 00:00〜09:00 に作られたページが前日扱い**になる。

**Why:** 2026-08-14 の夜間SNS発信候補パックで実害が出た。
- `createdTime 2026-08-12 22:14:23Z` を「8/12深夜の登録」と書き、そこから「8/13以降の新規登録は0件」と結論した。実体は **2026-08-13 07:14 JST**＝8/13朝便の納品ページ（`_sns_legs.log` の morning_push 06:45–07:17:48 と一致）。結論が反転する誤り。
- 💡ネタ「紀勢本線のICカード決済」は `2026-07-22 18:11:31Z` ＝ **JST 2026-07-23 03:11 作成**。にもかかわらず「2026-07-22作成」が7/30分〜8/14分のパック十数本に伝播し、経過日数が全部+1日ずれていた（三重の証拠: `_intake.log` の 7/23 triage が「投げ込みはJST 7/23 00:08」と明記）。
- `date(createdTime) >= 'YYYY-MM-DD'` という窓指定は、実際には **JST その日 09:00 以降**という窓になる。朝便（06:45起動）の登録が丸ごと窓から落ちるため件数が過少になる。

**How to apply:** 亀山の日次ジョブ成果物（発信候補パック・triage・ohayo/oyasumi集計）で Notion の createdTime 由来の日付・経過日数・件数を検証するときは、
①まず「その値はUTCか」を確認し、②+9時間してJST日付に直してから突合し、③窓指定クエリは `>= '前日T15:00:00Z'` 相当かを確認する。
JSTへの直しは `_sns_legs.log` / `_intake.log` の実行時刻（JST生ログ）と突き合わせると一発で裏が取れる。
