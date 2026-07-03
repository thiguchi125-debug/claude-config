---
name: google-keep-eod-1
description: 日中の記録はGoogle Keepに溜め、1日の終わりにClaude Code(PC)へ全文貼り付け。チェックボックス=タスクの記法ルールでログ化/タスク化/発信ネタ化を1パス triage する
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e432a2f4-d5be-45ed-85b5-a48ed3782b0f
---

2026-07-03〜 草川の日次ログ運用を変更。日中の記録は**スマホのGoogle Keep**に溜め、1日の終わりに**Claude Code(PC)へ全文コピペ**（先頭に「日次ログ：」等）。貼り付けを受けたら、nichijo記録モードの入口として下記の**Keep記法ルール**で1パス triage する。

**Why:** スマホ＝軽く捕捉、PC＝Todoist登録＋スマートインテーク3面振り分け、という役割分担（[[nichijo-mobile-project-instructions]]系の思想と同じ）。Keepはチェックボックスが使えるので「印をつけた行だけ昇格・素の行は全部ログ」という曖昧さゼロの判定ができる。捕捉の摩擦を最小にしつつ迷子ゼロを両立するため。

## How to apply（EOD貼り付けを受けたときの手順）

**判定は「デフォルト＝記録／印つき行だけ昇格」。** 記法：

| Keepでの書き方 | 処理 |
|---|---|
| 素の行 | nichijo日次ログ本文に記録するだけ |
| ☐ チェックボックス（未チェック） | **Todoistにタスク登録候補**。期限=今日+3日デフォルト（[[feedback_task_deadline_3days]]）・内容からプロジェクト自動振り分け（🏛議員活動/📋政策/📣発信/家族）。相手待ち=@結果待ち・要検討=@保留 |
| ☑ チェックボックス（チェック済み） | もう済んだこと→**完了ログ**として記録（記録用に登録即完了も可） |
| `発信:` または `💡` で始まる行 | 発信ネタ候補→sparkへ（貯める場合は📣SNS投稿管理DBに💡ストック） |
| `声:` で始まる行 | 市民の声→📝市民意見リスト(`c2c34bd8-`)（[[feedback_shimin_iken_db_consolidation_c2c34bd8]]） |
| `会った:` `面会:` | 接触ログ（🤝組織・業界団体接触ログ 等） |

**1パスの流れ:** ①全行を日次ログに記録 → ②チェックボックス行をタスク候補に、印つき行を発信/声/接触に振り分け → ③**振り分け先を1回だけ提示**（[[feedback_ask_destination_and_deadline_before_register]]）→ ④草川承認 → ⑤一括保存（Todoist登録は td.py・[[project_todoist_task_migration]]）→ ⑥nichijo日次ログ末尾に🔖台帳1行を自動追記。

## 未確定・要ロック
- **Keepのチェックボックスがコピペで何の文字になるか未確認**（`☑`/`☐` か `- [x]`/`- [ ]` か、印が消えたただのテキストか）。初回の実貼り付けで実際のマーカーを確認してこのルールに追記し確定させる。それまでは `☑/☐`・`- [x]/- [ ]`・行頭✓/チェック相当を広く拾う。
- 発信化・市民の声・接触ログの各保存前に、個人情報・要配慮情報を含む場合は content-risk-reviewer 経由（CLAUDE.mdスマートインテーク節）。
- Google Keepは日中の主キャプチャ面。従来のClaude.ai「記録」プロジェクト運用と併存/置換のどちらにするかは草川判断（現状は併存でも可、Keep→PC貼り付けが主線）。

関連: nichijo記録モード / [[project_nichijo_mobile]] / smart-intake / [[feedback_task_deadline_3days]]
