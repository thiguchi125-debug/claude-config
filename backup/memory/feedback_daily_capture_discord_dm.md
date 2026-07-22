---
name: daily-capture-discord-dm
description: 日中メモの捕捉面はDiscord bot DM一本（Google Keep EOD貼り付け運用は2026-07-23廃止）。夜間3:10 triageが全振り分けを自動処理
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 90e2e505-3eae-4fd3-89d0-f94b477b41ca
  modified: 2026-07-22T15:04:34.952Z
---

2026-07-23確定。日中の記録・メモ・タスク・声・発信ネタの捕捉面は**Discord bot DMに一本化**。旧Google Keep→EOD貼り付け運用（2026-07-03設計）は「貼り付けが面倒で実際やれない」という草川本人の申告で**廃止**（旧memory feedback_keep_eod_daily_log_intake.md は削除済）。

**Why:** Keep運用は「1日の終わりにPCへ全文コピペ」という手動工程が締めになっており、実行されず日次ログが空洞化。Discord夜間振り分け（launchd `com.kusagawa.discord-intake` 3:10・`nightly_intake.sh`→triage_prompt.md）が既にKeep記法相当の全振り分け（タスク候補提案／声:→📝市民意見／発信:→💡ストック／雑記→nichijo日次ログ／不明→📥未分類）を実装済みだったため、追加実装ゼロで摩擦ゼロ化できた。

**How to apply:**
- 草川がスマホからbot DMに投げるだけ。記法：素の行=日次ログ／「タスク:」「☐」=タスク化候補（提案→返信承認→翌夜Todoist登録）／「声:」=市民意見／「発信:」「ひらめき:」=💡ストック
- Macが3:10に寝ていても次回起床時にlaunchdが実行（実測7/22は6:00起動）。エラー時はカーソル非前進で原本保全→再処理＝**紛失は構造的にゼロ**
- 2026-07-23に nightly_intake.sh へ堅牢化追加：①起動時ネットワーク疎通待ち（discord.com gateway・最大3分）②fetch/triage失敗時30分後1回リトライ。2026-07-18〜21の4夜連続失敗（ENOTFOUND/Connection closed＝スリープ復帰直後のWi-Fi未接続）の再発防止
- 会話中でKeep貼り付けを促す・待つ動きはしない。日次ログ関連の案内はDiscord DM投げ込みを正とする

関連: [[project_sns_routine_v2]] / smart-intake / nichijo
