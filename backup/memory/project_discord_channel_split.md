---
name: project-discord-channel-split
description: Discord Bot DMを用途別3チャンネル（投げ込み／納品／ログ）に分離。2026-08-11に開通・運用中
metadata: 
  node_type: memory
  type: project
  originSessionId: 248b953f-2726-48b0-9092-1ff21ee621ad
  modified: 2026-08-11T13:45:32.908Z
---

Discordの送受信を1本のBot DMから **`#投げ込み`／`#納品`／`#ログ`** の3チャンネルへ分離する。**2026-08-11に開通済み・運用中**（草川がOAuthでMANAGE_CHANNELSを許可→`setup_channels.sh --create` でBotが3チャンネルを作成→疎通確認まで完了）。
チャンネルID: 投げ込み `1536732207740100648`／納品 `1536732210374246420`／ログ `1536732212639039578`（guild `1499356623448178778`・DM `1499359623013208104`）。読み取りは投げ込み＋納品＋DMの3本。

**なぜ:** 実測（2026-07-29〜08-11）でシステム→草川156件・約81,000字、草川→システム9件・約1,000字＝**17対1**。1,000字超のSNS原稿22件が壁になり、2026-08-07に転送された市民相談（両親同時育休で年中の子が退園）が埋もれて相談者を4日待たせた。草川の言葉＝「長い投稿文案を送られてきても対応が難しいし重要なメッセージを見逃す原因になる」。草川が「絶対に見逃したくない」と選んだのは①市民からの声の確認②返事が必要な問いかけ③納品できたという事実（システム異常は非選択＝ohayoの🚨で足りる）。

**（履歴）草川の手番だった作業＝2026-08-11に完了:** Botはサーバー `kusakawatakuya`（guild `1499356623448178778`）に参加済みで**招待は不要**。ただし Manage Channels 権限がなくBotからは作れない（403で確認済み）。
1. サーバーにテキストチャンネル `投げ込み` `納品` `ログ` を作る
2. `bash ~/.claude/scripts/sns-routine/setup_channels.sh`（検出→設定→各チャンネルへ疎通確認の1通、まで自動。未設定のものはスキップするのでDMに誤爆しない）

別ルート＝`https://discord.com/oauth2/authorize?client_id=1499353373080555620&scope=bot&permissions=117840` を開いてMANAGE_CHANNELSを与えれば `setup_channels.sh --create` でチャンネル作成から自動。Bot権限が1つ増えるのでどちらを選ぶかは草川判断。
Bot現在の権限（2026-08-11実測・67584＋@everyone）= VIEW_CHANNEL／SEND_MESSAGES／READ_MESSAGE_HISTORY／ADD_REACTIONS／ATTACH_FILES。MANAGE_CHANNELS・MANAGE_ROLES・ADMINISTRATORは無し。
2026-08-11にこの案内をDMへ送信済み（msg_id 1536727175716278422）。

**実装のポイント:**
- `discord_api.py` に `channels()／out_channel()／in_channels()／discover()／set_channels()`、`post` に `--to inbox|delivery|log` と `--reply-to` を追加。
- **未設定の用途はDMへ落ちる**ので、チャンネルを作る前でも壊れない。既存テスト10件パス。
- 読み取りは `#投げ込み＋#納品＋DM`。`#納品` を読むのはSNS便への返信（「Bで」「パス」）がそこに来るため。`#ログ` は書き専用。
- **カーソルは `last_processed_id` 1本のまま。** Discordのidは時刻順の通し番号なので `after=` が全チャンネルで正しく効く。チャンネル別カーソルを作らないこと（複雑になるだけ）。
- 受領レシートは `--to inbox --reply-to <元msg_id>` で**草川が投げた元メッセージへの返信**として返す。独立メッセージだと何への返事か分からなくなる。
- 呼び出し側は `triage_prompt.md`（レシート・タスク提案→inbox）と `leg_morning_push.md`／`leg_evening_push.md`（原稿→delivery・記録→log）に振り分け表を記載済み。

詳細手順は `~/.claude/scripts/sns-routine/README.md` の「用途別チャンネル」節。関連: [[feedback_discord_task_proposal_retire_loses_urgent]] / [[project_sns_routine_v2]]

---

## 2026-08-26 投げ込み専用に縮小（草川指示・現在の運用）

**3チャンネル分離では足りなかった。** 分離後も配信量が減らず、8/26夕便1回で **9通・約6,800字**、
うちFacebook原稿が3バージョン（原案→差し替え版→最終版）届いた。草川からの返信は **8/24以降ゼロ**で、
問いかけと承認待ちだけが溜まっていた。草川の言葉＝「discordで長文章を送られても読む気がしない」。

**現在の形＝Discordは草川→システムの投げ込み口だけ。**
- `discord_api.py` に `INBOX_ONLY = True` / `POST_ALLOWED = ("inbox",)` を追加。
  `post --to delivery` と `--to log` は **スクリプトが SystemExit で拒否する**（rc=1・実送信なし）。
  送れるのは `--to inbox`（投げ込みへの受領レシート・`--reply-to` 付き）だけ。
- 完成原稿の受け渡しは **drafts/ と 📣投稿管理DB のみ**。Discordには流さない。
- 夜間intake 3:10（`triage_prompt.md`）は inbox にしか post していないので、そのまま動く。
- 戻すときは `INBOX_ONLY = False`。バックアップ＝`discord_api.py.bak_20260826`。

関連: [[project_sns_routine_v2]]
