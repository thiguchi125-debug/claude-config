---
name: project-discord-channel-split
description: Discord Bot DMを用途別3チャンネル（投げ込み／納品／ログ）に分離。実装済み・草川のチャンネル作成待ち
metadata: 
  node_type: memory
  type: project
  originSessionId: 248b953f-2726-48b0-9092-1ff21ee621ad
  modified: 2026-08-11T13:14:12.443Z
---

Discordの送受信を1本のBot DMから **`#投げ込み`／`#納品`／`#ログ`** の3チャンネルへ分離する。実装は2026-08-11に完了、**残るのは草川がDiscordアプリでチャンネルを3つ作ることだけ**。

**なぜ:** 実測（2026-07-29〜08-11）でシステム→草川156件・約81,000字、草川→システム9件・約1,000字＝**17対1**。1,000字超のSNS原稿22件が壁になり、2026-08-07に転送された市民相談（両親同時育休で年中の子が退園）が埋もれて相談者を4日待たせた。草川の言葉＝「長い投稿文案を送られてきても対応が難しいし重要なメッセージを見逃す原因になる」。草川が「絶対に見逃したくない」と選んだのは①市民からの声の確認②返事が必要な問いかけ③納品できたという事実（システム異常は非選択＝ohayoの🚨で足りる）。

**草川の手番（初回のみ）:** Botはサーバー `kusakawatakuya`（guild `1499356623448178778`）に参加済みで**招待は不要**。ただし Manage Channels 権限がなくBotからは作れない（403で確認済み）。
1. サーバーにテキストチャンネル `投げ込み` `納品` `ログ` を作る
2. `python3 ~/.claude/scripts/sns-routine/discord_api.py discover --apply`（名前から用途を自動判定して `_channels.json` へ書く）

**実装のポイント:**
- `discord_api.py` に `channels()／out_channel()／in_channels()／discover()／set_channels()`、`post` に `--to inbox|delivery|log` と `--reply-to` を追加。
- **未設定の用途はDMへ落ちる**ので、チャンネルを作る前でも壊れない。既存テスト10件パス。
- 読み取りは `#投げ込み＋#納品＋DM`。`#納品` を読むのはSNS便への返信（「Bで」「パス」）がそこに来るため。`#ログ` は書き専用。
- **カーソルは `last_processed_id` 1本のまま。** Discordのidは時刻順の通し番号なので `after=` が全チャンネルで正しく効く。チャンネル別カーソルを作らないこと（複雑になるだけ）。
- 受領レシートは `--to inbox --reply-to <元msg_id>` で**草川が投げた元メッセージへの返信**として返す。独立メッセージだと何への返事か分からなくなる。
- 呼び出し側は `triage_prompt.md`（レシート・タスク提案→inbox）と `leg_morning_push.md`／`leg_evening_push.md`（原稿→delivery・記録→log）に振り分け表を記載済み。

詳細手順は `~/.claude/scripts/sns-routine/README.md` の「用途別チャンネル」節。関連: [[feedback_discord_task_proposal_retire_loses_urgent]] / [[project_sns_routine_v2]]
