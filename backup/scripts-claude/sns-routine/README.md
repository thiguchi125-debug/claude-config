# sns-routine — Discord投げ込み夜間自動振り分け＋候補パック生成＋動画夜間フル制作（SNSルーティンv2 Phase1+3）

2026-07-14構築。Phase3（候補パック夜間生成／triage返信スキップ／動画夜間実行）2026-07-14追加。詳細は memory `project_sns_routine_v2.md`、仕様書 `~/.claude/projects/-Users-kusakawatakuya/specs/2026-07-14-sns-routine-v2-design.md` を参照。

## nightly_intake.sh の3ステージ構成

1. **ステージ1 triage振り分け**: Discord新着 or 前夜提案の残りがある夜のみ `triage_prompt.md` で headless claude -p 実行。0件夜は起動しない（`discord_intake` status）。triage失敗時は即 `exit 1` でステージ2/3も実行しない。
2. **ステージ2 候補パック生成**: 新着/pending処理があった夜、または**毎週月曜は新着0件でも必ず** `pack_prompt.md` で headless claude -p 実行。📮発信候補パックページ（`39dcf503-a68f-8101-beac-c2883ed87e70`）の「生成ガイド」節（30日超で鮮度切れ時のみ再生成）と「本日の候補」節（毎回全置換・最大8本）を書く。失敗しても `exit 1` にせず `sns_pack` error記録のみでステージ3へ継続（`update_status.py sns_pack ok|error`）。
3. **ステージ3 動画夜間フル制作**: `_video_queue.txt` が非空の時だけ `video_stage_prompt.md` で headless claude -p 実行（0件夜はclaude起動なし＝トークンゼロ）。`_video_queue.txt` はステージ2の pack_prompt.md が📮SNS便ステータスページ（`39dcf503-a68f-811b-bdd3-cce4e418187a`）の「動画リクエスト」節から未処理行を転記して毎回上書きする（stage3側が処理後に空へ戻す）。short-video-createスキル相当のフル制作（セリフ→安全ゲート→挿入画像→7PF→📣DB保存→Drive📱動画素材ミラー）を行い、ステータスページの該当行を`[x]`化＋履歴節に1行追記（`sns_video` status）。

## 構成ファイル

- `discord_api.py` — Discord REST薄ラッパー（fetch/react/post/advance）
- `nightly_intake.sh` — 毎晩実行される本体（3ステージ順次実行。詳細は上記）
- `triage_prompt.md` — ステージ1振り分けプロンプト（SNS便・タスク提案への短い返信はreact okのみで保存対象外にするルール2026-07-14追記）
- `pack_prompt.md` — ステージ2候補パック生成プロンプト（voice-dna圧縮・リスク8軸・禁止表現・PF別体裁を生成ガイド節に、アーカイブgrep接地済み候補を本日の候補節に書く。2026-07-14新規）
- `video_stage_prompt.md` — ステージ3動画夜間フル制作プロンプト（2026-07-14新規）
- `update_status.py` — `_pipeline_status.json` の `discord_intake` / `sns_pack` / `sns_video` キー更新
- `_state.json` — `dm_channel_id` と `last_processed_id`（カーソル。全件処理成功時のみ前進）
- `_notion_queue.jsonl` — Notion書込不能時のフォールバック退避（ohayoが翌朝flush）
- `_pending_tasks.jsonl` — タスク化候補の提案控え（草川のDiscord返信「①OK」等と翌夜突合→Todoist登録後に消し込み）
- `_video_queue.txt` — ステージ2が書き出す動画リクエストキュー（非空の時だけステージ3起動。2026-07-14新規）
- `test_discord_api.py` — discord_api.py のオフラインunittest（`python3 test_discord_api.py -v`）
- `_intake.log` / `_launchd_stdout.log` / `_launchd_stderr.log` — 実行ログ

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

## トラブル時

- ログ確認: `~/.claude/scripts/sns-routine/_intake.log`
- 手動再実行: `~/.claude/scripts/sns-routine/nightly_intake.sh`
- launchd再キック: `launchctl kickstart gui/$(id -u)/com.kusagawa.discord-intake`
- 状態監視: `_pipeline_status.json` の `discord_intake` キー（ohayoが毎朝確認）

## セキュリティ注意

Discordトークンは `~/.claude/channels/discord/.env` の `DISCORD_BOT_TOKEN`。本READMEを含め、このディレクトリ配下にトークンをログ・コミットしない。
