---
name: feedback-discord-task-proposal-retire-loses-urgent
description: Discord夜間triageのタスク提案は返信がないと2晩で退避される。緊急度ではなく返信の有無で仕分けるため、最重要案件ほど未分類の箱に落ちる
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 248b953f-2726-48b0-9092-1ff21ee621ad
  modified: 2026-08-10T23:04:46.220Z
---

夜間triage（`~/.claude/scripts/sns-routine/triage_prompt.md` 手順5〜6）はタスクを**登録せず提案だけ**してDiscordへDMを送り、「①OK」の返信を待つ。返信が2晩無いと `retire_no_reply` で📥未分類インテークへ退避する。この導線は**緊急度を一切見ていない**ので、最重要案件ほど静かに消える。

**Why:** 2026-08-11に草川が「discordから投げたはずだけどどこに登録されているの？」と聞いて発覚。育休退園の市民相談（IKN-196・相談者は8/7から返信待ち・9月復園が懸かる時間切れ案件）は8/9夜に提案2件が作られたが、8/10・8/11の無応答で `retire_queued` になっていた。さらに `content_safety_gate.py` が退避先への本文書き込みをdenyし、📥未分類インテークにすら入らず `_notion_queue.jsonl` に滞留。📮投げ込み台帳の「保存先」欄は「Todoist提案中」のままで、**ohayoはこの欄を読まない**ため朝も出てこなかった。同じ経路で「みずきが丘の信号の注意喚起」（交通安全）も2026-08-05に退避済み。草川の結論＝「discordは現状どこに行ったかわからなくなるので使えない」。捕捉面としては機能するが、**承認ゲートを置く場所としては破綻している**。

**How to apply:**
- 「Discordに投げた〇〇どこ？」と聞かれたら、Notion検索だけで終わらせず **必ず `~/.claude/scripts/sns-routine/_pending_tasks.jsonl` と `_notion_queue.jsonl` を開く**。Notionに市民意見・ネタDBが出来ていても、タスクだけ提案止まりで死んでいることがある
- `status` が `retire_queued` / `retired_no_reply` の行は**捨てられた仕事**。緊急度を見て復活させる
- 手動で登録し直したら `_pending_tasks.jsonl` の該当行を `status: registered` ＋ todoist_id ＋ resolved_note で消し込む（今夜のtriageが再処理・再退避しないように）
- ohayoで「Todoist提案中」の滞留を可視化する仕組みが無いのが穴。朝に出す導線を作るまでは、草川から聞かれたときにこのファイルを開くのが唯一の発見手段
- 関連: [[feedback_discord_triage_partial_write_resume]] / [[feedback_system_closing_loops_rot]]（自動トリガー有=生／記憶依存の締め=腐る、の実例）
