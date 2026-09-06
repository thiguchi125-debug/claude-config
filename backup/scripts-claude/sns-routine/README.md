> **2026-09-06: `com.kusagawa.discord-intake`（夜間3:10 triage）は停止。** plistは `~/Library/LaunchAgents/_disabled_2026-09-06/`。日中メモはTodoist Inbox一本。Bot・スクリプトは温存。

# sns-routine — Discord投げ込み夜間自動振り分け＋候補パック生成＋動画夜間フル制作＋SNS便4本（SNSルーティン**v3**）

2026-07-14構築（v2）→ **2026-07-23 v3化（完成原稿直接納品）**。詳細は memory `project_sns_routine_v2.md`、仕様書 v3=`~/.claude/projects/-Users-kusakawatakuya/specs/2026-07-23-sns-routine-v3-design.md`／v2=`2026-07-14-sns-routine-v2-design.md` を参照。

## 🆕 v3の要点（2026-07-23〜）

v2の「候補メニュー→返信で選ぶ→45分後納品」は返信ゼロ→生成ゼロで滞ったため廃止。**push便が完成短文原稿（X/Threads/FB＋写真日はInsta）をDMへ直接納品**し、返信は修正したい時だけ。

- **時刻**: 朝納品6:45／朝返信7:30／**夕納品19:30**（16:30から変更・当日の活動投げ込みを夜まで拾うため）／**夕返信20:15**
- **品質メカニズム**: 新風枠毎便1本必須（WebSearch追加探索可）／一次記事WebFetch本文調査必須／`_theme_history.json` 14日クールダウン（ステータスページ「テーマ履歴ミラー」節に写し）／iJAMPはGmail経由スキャン（`from:ijamp.jiji.com newer_than:1d`・サイトスクレイピング禁止・原文転載禁止・公開一次情報乗り換え必須）
- **見える化**: triageが📮投げ込み台帳DB（data_source `7a444c29-ef25-4139-9033-c24e9bd78528`・DBページ 48d0d7b4a68f4fc587536be382efecec）へ全件記録＋毎夜「🧾今夜の振り分け」レシートDM
- **障害耐性**: DM納品はNotion障害と切り離し（Notion分はqueue退避）／claude -p失敗15分後1回リトライ／起動時ネット疎通待ち／`_menu_state.json`→`_delivery_state.json`（`{"leg","date","delivery_msg_id"}`）に単純化
- **allowedTools追加**: `WebSearch,WebFetch,mcp__claude_ai_Gmail__*`（sns_leg.sh）
- **discord_api.py追加**: fetch/readに`attachments`フィールド、`download <msg_id> <dir>`コマンド（Insta用写真取得）
- v2ファイル一式のバックアップ: `_backup_2026-07-23_v3/`

### v3.1（2026-07-25・遅延並走事故の修理）

7/23夕便がMacスリープで翌朝まで凍結→7/24朝便と並走し同テーマ（にんにく）を二重納品。7/24夜はバッテリー駆動（残9%→3%）でスリープ連発し22:55遅延納品。対策3点を sns_leg.sh に実装:

1. **遅延発火ガード**: 定時から120分超遅れて起動した便は自走せず見送り（status=error記録・次の定時便が繰越）
2. **排他ロック**: `_leg.lock.d`（mkdirロック・macOSにflockが無いため）で便同士の並走を禁止。5時間超の残置ロックは奪取
3. **caffeinate -i**: 実行中のアイドルスリープ抑止（※バッテリー駆動時の蓋閉じスリープは防げない→**Macは電源接続が前提**）

あわせて `_auto_intake.sh` の write_status を全置換→マージ書込みに修理（毎晩2:30にsns_*等の監視キーが消えていた）。

以下はv2時代の記述（3ステージ夜間intake・監査・復元手順は現役。「メニュー」「16:30/17:15」表記は上記v3が正）。

## ⚠️ SNS便4本はローカルMac launchd化済み（2026-07-14・クラウドRoutineは無効化）

当初SNS便4本（朝便プッシュ/朝返信/夕便プッシュ/夕返信）はクラウドRoutineとして構築したが、**クラウド実行環境が discord.com への通信をブロックする**ことが実運用テストで判明した（`CONNECT 403`・2026-07-14確認）。Macは `sleep=0` で夜間も常時稼働しており、既存の夜間パイプライン（`nightly_intake.sh`・`sunday_audit.sh`）がlaunchdで安定稼働している実績があるため、SNS便4本もローカルMac launchd実行に切り替えた。副次効果として、Discordトークンが `~/.claude/channels/discord/.env` から一切外に出ない（クラウド側でNotion経由トークン取得する必要がなくなった）ぶんセキュリティも向上している。

- **無効化したクラウドRoutine4本**（claude.ai/code/routines で確認・停止可能。trigger idは環境固有のため要確認）: 朝便プッシュ6:45／朝返信処理7:30／夕便プッシュ16:30／夕返信処理17:15
- **ロジックの正本**は `_routines_phase3/{morning_push,morning_reply,evening_push,evening_reply}.md`（クラウド版・参照用に保持。実行はされない）
- **実行される版**は `leg_{morning_push,morning_reply,evening_push,evening_reply}.md`（ローカル版。curl直叩き＋Notion設定ページからのトークン取得を `discord_api.py post/read` 呼び出しに差し替えただけで、返信解釈・PF生成規則・リスク自己チェック・動画モード・候補選定・ステータスページ更新等のロジックは一字一句同一）
- **起動ランナー**: `sns_leg.sh <leg名>`（後述）
- **plist4枚**: `com.kusagawa.sns-morning-push` (6:45) / `com.kusagawa.sns-morning-reply` (7:30) / `com.kusagawa.sns-evening-push` (16:30) / `com.kusagawa.sns-evening-reply` (17:15)

## nightly_intake.sh の3ステージ構成

1. **ステージ1 triage振り分け**: Discord新着 or 前夜提案の残りがある夜のみ `triage_prompt.md` で headless claude -p 実行。0件夜は起動しない（`discord_intake` status）。triage失敗時は即 `exit 1` でステージ2/3も実行しない。
2. **ステージ2 候補パック生成**: 新着/pending処理があった夜、または**毎週月曜は新着0件でも必ず** `pack_prompt.md` で headless claude -p 実行。📮発信候補パックページ（`39dcf503-a68f-8101-beac-c2883ed87e70`）の「生成ガイド」節（30日超で鮮度切れ時のみ再生成）と「本日の候補」節（毎回全置換・最大8本）を書く。失敗しても `exit 1` にせず `sns_pack` error記録のみでステージ3へ継続（`update_status.py sns_pack ok|error`）。
3. **ステージ3 動画夜間フル制作**: `_video_queue.txt` が非空の時だけ `video_stage_prompt.md` で headless claude -p 実行（0件夜はclaude起動なし＝トークンゼロ）。`_video_queue.txt` はステージ2の pack_prompt.md が📮SNS便ステータスページ（`39dcf503-a68f-811b-bdd3-cce4e418187a`）の「動画リクエスト」節から未処理行を転記して毎回上書きする（stage3側が処理後に空へ戻す）。short-video-createスキル相当のフル制作（セリフ→安全ゲート→挿入画像→7PF→📣DB保存→Drive📱動画素材ミラー）を行い、ステータスページの該当行を`[x]`化＋履歴節に1行追記（`sns_video` status）。

## 構成ファイル

- `discord_api.py` — Discord REST薄ラッパー（fetch/react/post/advance/audit/**read**）。`post`は送信成功時にメッセージidをstdoutに1行出力する（2026-07-14ローカル便化で追加）。`read <after_msg_id>`は指定id以降の全メッセージ（bot含む・`is_user`フラグで区別）を昇順JSON出力する読み取り専用コマンド（カーソル・リアクション不変更）
- `sunday_audit.sh` — 日曜監査（迷子ゼロ締め工程。`discord_api.py audit 7`で直近7日の生メッセージ全件取得→草川本人の未リアクションメッセージを検出。0件なら`sns_audit ok`、N件なら`sns_audit error`＋`_audit_report.md`に詳細出力。AUDIT_FLOOR（2026-07-14 00:00 JST）より古い履歴＝運用開始前カーソル初期化スキップ分は対象外。Claude起動なし・トークンゼロ。launchd `com.kusagawa.sns-audit`（日曜3:20）。2026-07-14新規）
- `nightly_intake.sh` — 毎晩実行される本体（3ステージ順次実行。詳細は上記）
- `triage_prompt.md` — ステージ1振り分けプロンプト（SNS便・タスク提案への短い返信はreact okのみで保存対象外にするルール2026-07-14追記）
- `pack_prompt.md` — ステージ2候補パック生成プロンプト（voice-dna圧縮・リスク8軸・禁止表現・PF別体裁を生成ガイド節に、アーカイブgrep接地済み候補を本日の候補節に書く。2026-07-14新規）
- `video_stage_prompt.md` — ステージ3動画夜間フル制作プロンプト（2026-07-14新規）
- `sns_leg.sh` — **SNS便4本（朝便プッシュ/朝返信/夕便プッシュ/夕返信）共通ランナー**（2026-07-14ローカル化で新規）。`sns_leg.sh <morning_push|morning_reply|evening_push|evening_reply>` で呼ぶ。reply系はゼロコストガード（`_menu_state.json`が当日・leg一致・かつ`discord_api.py read`で本人の新規返信が1件以上ある場合のみclaude起動、それ以外は`sns_<leg> ok`で即終了）。push系は毎回claude起動。ステータスキーは`sns_morning_push`/`sns_morning_reply`/`sns_evening_push`/`sns_evening_reply`
- `leg_morning_push.md` / `leg_morning_reply.md` / `leg_evening_push.md` / `leg_evening_reply.md` — SNS便4本のローカル実行プロンプト（`_routines_phase3/`の対応版からロジックを継承。共通セットアップのcurl/Notion設定ページ取得手順のみ`discord_api.py post/read`呼び出しに差し替え。push系はメニュー送信後に`_menu_state.json`書き込み手順を追加。それ以外の文言は一字一句同一。2026-07-14新規）
- `_menu_state.json` — その日のpush便が書く軽量ガード用ファイル（`{"leg":"morning|evening","date":"YYYY-MM-DD","menu_msg_id":"..."}`）。正本はNotion📮SNS便ステータスページ「現在のメニュー」節、これは`sns_leg.sh`がclaude起動要否を判定するための補助
- `update_status.py` — `_pipeline_status.json` の `discord_intake` / `sns_pack` / `sns_video` / `sns_morning_push` / `sns_morning_reply` / `sns_evening_push` / `sns_evening_reply` / `sns_audit` キー更新
- `_state.json` — `dm_channel_id` と `last_processed_id`（カーソル。全件処理成功時のみ前進）
- `_notion_queue.jsonl` — Notion書込不能時のフォールバック退避（ohayoが翌朝flush）
- `_pending_tasks.jsonl` — タスク化候補の提案控え（草川のDiscord返信「①OK」等と翌夜突合→Todoist登録後に消し込み）
- `_video_queue.txt` — ステージ2が書き出す動画リクエストキュー（非空の時だけステージ3起動。2026-07-14新規）
- `test_discord_api.py` — discord_api.py のオフラインunittest（`python3 test_discord_api.py -v`）
- `_intake.log` / `_launchd_stdout.log` / `_launchd_stderr.log` — 夜間パイプライン実行ログ
- `_sns_legs.log` / `_sns_legs_launchd_stdout.log` / `_sns_legs_launchd_stderr.log` — SNS便4本の実行ログ（2026-07-14新規）

## launchd スケジューリング

`~/Library/LaunchAgents/` 配下は git バックアップ対象外の領域（OS管理領域のため）だが、
`~/claude-config/scripts/sync-to-git.sh` が `com.kusagawa.*.plist` を自動で
`~/claude-config/backup/launchd/` にコピーしてバックアップ済み。
このREADMEは Mac 再セットアップ時に手元で内容を確認できるよう、実物を転記した控え。

### plist全文（`~/Library/LaunchAgents/com.kusagawa.discord-intake.plist`）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.kusagawa.discord-intake</string>

  <key>ProgramArguments</key>
  <array>
    <string>/Users/kusakawatakuya/.local/bin/kusagawa-pipeline-bash</string>
    <string>/Users/kusakawatakuya/.claude/scripts/sns-routine/nightly_intake.sh</string>
  </array>

  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/Users/kusakawatakuya/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    <key>HOME</key>
    <string>/Users/kusakawatakuya</string>
  </dict>

  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>3</integer>
    <key>Minute</key>
    <integer>10</integer>
  </dict>

  <key>StandardOutPath</key>
  <string>/Users/kusakawatakuya/.claude/scripts/sns-routine/_launchd_stdout.log</string>
  <key>StandardErrorPath</key>
  <string>/Users/kusakawatakuya/.claude/scripts/sns-routine/_launchd_stderr.log</string>

  <key>RunAtLoad</key>
  <false/>
</dict>
</plist>
```

### 再登録コマンド（Mac再セットアップ時）

```bash
# 1. plistファイルを上記内容で ~/Library/LaunchAgents/com.kusagawa.discord-intake.plist に作成
# 2. bootstrap（初回登録）
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.kusagawa.discord-intake.plist

# 3. 動作確認（手動即時実行）
launchctl kickstart gui/$(id -u)/com.kusagawa.discord-intake

# 4. 登録状態の確認
launchctl print gui/$(id -u)/com.kusagawa.discord-intake
```

`/Users/kusakawatakuya/.local/bin/kusagawa-pipeline-bash` はDriveパイプライン等と共用のランナー本体（`~/claude-config/backup/launchd/` にも保全済み）。存在しない場合はそちらから復元。

### plist全文（SNS便4本・2026-07-14ローカル化で新規登録）

`~/Library/LaunchAgents/com.kusagawa.sns-morning-push.plist`（6:45）:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.kusagawa.sns-morning-push</string>

  <key>ProgramArguments</key>
  <array>
    <string>/Users/kusakawatakuya/.local/bin/kusagawa-pipeline-bash</string>
    <string>/Users/kusakawatakuya/.claude/scripts/sns-routine/sns_leg.sh</string>
    <string>morning_push</string>
  </array>

  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/Users/kusakawatakuya/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    <key>HOME</key>
    <string>/Users/kusakawatakuya</string>
  </dict>

  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>6</integer>
    <key>Minute</key>
    <integer>45</integer>
  </dict>

  <key>StandardOutPath</key>
  <string>/Users/kusakawatakuya/.claude/scripts/sns-routine/_sns_legs_launchd_stdout.log</string>
  <key>StandardErrorPath</key>
  <string>/Users/kusakawatakuya/.claude/scripts/sns-routine/_sns_legs_launchd_stderr.log</string>

  <key>RunAtLoad</key>
  <false/>
</dict>
</plist>
```

`~/Library/LaunchAgents/com.kusagawa.sns-morning-reply.plist`（7:30・`morning_push`引数を`morning_reply`に、`Hour`/`Minute`を7/30に、`Label`を`com.kusagawa.sns-morning-reply`に置き換えるだけで他は同一）

`~/Library/LaunchAgents/com.kusagawa.sns-evening-push.plist`（16:30・引数`evening_push`・`Hour`/`Minute`=16/30・`Label`=`com.kusagawa.sns-evening-push`）

`~/Library/LaunchAgents/com.kusagawa.sns-evening-reply.plist`（17:15・引数`evening_reply`・`Hour`/`Minute`=17/15・`Label`=`com.kusagawa.sns-evening-reply`）

### 再登録コマンド（SNS便4本・Mac再セットアップ時）

```bash
# 1. 上記4パターンのplistを ~/Library/LaunchAgents/com.kusagawa.sns-{morning-push,morning-reply,evening-push,evening-reply}.plist に作成
# 2. bootstrap（初回登録・4本まとめて）
for f in sns-morning-push sns-morning-reply sns-evening-push sns-evening-reply; do
  launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.kusagawa.$f.plist
done

# 3. 登録状態の確認
launchctl list | grep sns-

# 4. 動作確認が必要な場合のみ手動即時実行（通常は本番時刻を待つ）
launchctl kickstart gui/$(id -u)/com.kusagawa.sns-morning-push
```

## トラブル時

- ログ確認（夜間パイプライン）: `~/.claude/scripts/sns-routine/_intake.log`
- ログ確認（SNS便4本）: `~/.claude/scripts/sns-routine/_sns_legs.log`
- 手動再実行（夜間パイプライン）: `~/.claude/scripts/sns-routine/nightly_intake.sh`
- 手動再実行（SNS便1本）: `~/.claude/scripts/sns-routine/sns_leg.sh <morning_push|morning_reply|evening_push|evening_reply>`
- launchd再キック: `launchctl kickstart gui/$(id -u)/com.kusagawa.discord-intake`（夜間パイプライン）／`launchctl kickstart gui/$(id -u)/com.kusagawa.sns-morning-push`等（SNS便）
- 状態監視: `_pipeline_status.json` の `discord_intake` / `sns_pack` / `sns_video` / `sns_morning_push` / `sns_morning_reply` / `sns_evening_push` / `sns_evening_reply` / `sns_audit` キー（ohayoが毎朝確認）

## セキュリティ注意

Discordトークンは `~/.claude/channels/discord/.env` の `DISCORD_BOT_TOKEN`。本READMEを含め、このディレクトリ配下にトークンをログ・コミットしない。SNS便4本のローカル化（2026-07-14）により、トークンはこのローカル.envから一切外に出ない構成になった（クラウドRoutine時代はNotion「🔧SNSルーティン設定」ページ経由で取得していたが、この経路は廃止済み）。

---

## 用途別チャンネル（2026-08-11〜）

### なぜ分けたか

それまでは送受信すべてを1本のBot DMに流していた。実測（2026-07-29〜08-11）で

| 向き | 件数 | 文字数 |
|---|---|---|
| システム→草川 | 156件 | 約81,000字 |
| 草川→システム | 9件 | 約1,000字 |

**17対1**。1,000字超のSNS原稿が22件あり、草川の投げ込み（1日0〜3件・数十字）が壁に埋もれる。
2026-08-07に転送された市民相談（両親同時育休で年中の子が退園）が見落とされ、
相談者を4日待たせた事故の直接原因がこれ。→ [[feedback_discord_task_proposal_retire_loses_urgent]]

### 構成

| チャンネル | 用途 | `--to` |
|---|---|---|
| `#投げ込み` | 草川→システム。受領レシートと「返事が要る問いかけ」だけを**元メッセージへの返信**で返す | `inbox` |
| `#納品` | コピペ用の完成原稿（ヘッダ・X・Threads・Facebook・Instagram・最終通） | `delivery` |
| `#ログ` | 安全ゲート記録・稼働状況・エラー・その他の記録（読むだけのもの） | `log` |

- **読み取り**は `#投げ込み`＋`#納品`＋DM の3つ（`in_channels()`）。`#納品` を読むのはSNS便への返信（「Bで」「パス」「〇〇直して」）がそこに来るため。`#ログ` は書き専用。
- **未設定の用途は自動でDMに落ちる。** サーバー未設定でも従来どおり動く（後方互換）。
- Discordのメッセージidは時刻順の通し番号なので、`last_processed_id` カーソルは1本のまま全チャンネルに使える。チャンネルごとにカーソルを持たない。

### セットアップ（草川の手番・初回のみ）

Botは既にサーバー `kusakawatakuya` に参加済み（招待不要）。ただし**チャンネル作成権限がない**ので、そこだけ手で作る。

1. Discordアプリでサーバー `kusakawatakuya` を開く
2. テキストチャンネルを3つ作る: `投げ込み` / `納品` / `ログ`
3. 以下を1回実行（検出→設定→各チャンネルへ疎通確認の1通、まで自動）

```bash
bash ~/.claude/scripts/sns-routine/setup_channels.sh
```

**別ルート:** Botに MANAGE_CHANNELS を与えるなら、下のURLを1回開いて認証すればチャンネル作成から自動でできる。
`https://discord.com/oauth2/authorize?client_id=1499353373080555620&scope=bot&permissions=117840`
そのうえで `bash ~/.claude/scripts/sns-routine/setup_channels.sh --create`。
Botの権限が1つ増える（この非公開サーバー内のみ）ので、手で3つ作るほうが安心ならそちらでよい。

Bot現在の権限（2026-08-11実測）= VIEW_CHANNEL／SEND_MESSAGES／READ_MESSAGE_HISTORY／ADD_REACTIONS／ATTACH_FILES。MANAGE_CHANNELSは無し（403確認済み）。

DM運用へ戻したいときは `discord_api.py channels --inbox - --delivery - --log -`。
