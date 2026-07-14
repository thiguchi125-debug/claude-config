# sns-routine — Discord投げ込み夜間自動振り分け（SNSルーティンv2 Phase1）

2026-07-14構築。詳細は memory `project_sns_routine_v2.md`、仕様書 `~/.claude/projects/-Users-kusakawatakuya/specs/2026-07-14-sns-routine-v2-design.md` を参照。

## 構成ファイル

- `discord_api.py` — Discord REST薄ラッパー（fetch/react/post/advance）
- `nightly_intake.sh` — 毎晩実行される本体（fetch→headless claude -pで振り分け→advance）
- `triage_prompt.md` — headless claude -p に渡す振り分けプロンプト
- `update_status.py` — `_pipeline_status.json` の `discord_intake` キー更新
- `_state.json` — `dm_channel_id` と `last_processed_id`（カーソル。全件処理成功時のみ前進）
- `_notion_queue.jsonl` — Notion書込不能時のフォールバック退避（ohayoが翌朝flush）
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
