---
name: feedback-discord-triage-partial-write-resume
description: Discord夜間triageは途中死すると「Notion登録済み・カーソル未前進」の半端状態で残る。再処理夜は必ず重複チェックを先にやる
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c82a8ec2-2ab8-492c-8c58-c2ea80adf864
  modified: 2026-07-26T10:31:43.338Z
---

Discord投げ込み夜間triage（`~/.claude/scripts/sns-routine/`）は、処理が複数ステップ（📝市民意見リスト等へ保存 → 📮投げ込み台帳登録 → 🔖日次ログ追記 → react → advance）に分かれているため、途中で通信断・API切断が起きると **「Notionには登録済みだがカーソルは未前進」** の半端な状態で残る。翌回 `_new_messages.json` に同じメッセージが再び載る。

**Why:** 2026-07-26 16:30便が「市民意見リストへ登録成功。台帳登録と日次ログ特定を並行で進めます。」の直後に `API Error: Connection closed mid-response` で落ちた。17:00の再試行で同じ1件（msg 1530499178881355778・川崎一色の公園要望）が再投入され、素直に処理すると📝市民意見リストに二重登録するところだった。

**How to apply:** `_new_messages.json` を処理する前に、そのメッセージが既に保存済みでないかを確認する。最速の判定は **📮投げ込み台帳DB（`7a444c29-ef25-4139-9033-c24e9bd78528`）を msg_id で引く**（全件必須の登録なので、行があれば完了・無ければ未完了）。台帳に無くても保存先DB側に先に入っている可能性があるので、`_intake.log` の末尾で前回便の落ちた位置を確認し、保存先を notion-search で1回引いてから create する。既に在ればcreateせず、**残りの工程（台帳・🔖台帳行・react・advance・レシートDM）だけを追いつかせる**。関連: [[feedback_system_closing_loops_rot]]
