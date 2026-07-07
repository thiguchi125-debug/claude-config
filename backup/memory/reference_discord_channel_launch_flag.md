---
name: discord-channel-launch-flag
description: DiscordチャンネルでClaude Codeを起動する正しいフラグ形式と、反応しない時の診断手順
metadata: 
  node_type: memory
  type: reference
  originSessionId: a66b1e0e-b293-4076-9f9c-c1a90e60a66b
---

# Discordチャンネル起動フラグの正本（2026-07-07確定）

**正**: `claude --channels plugin:discord@claude-plugins-official`
**誤**: `claude --channels plugin:discord:discord` — CLIパーサーは `plugin:<プラグイン名>@<マーケットプレイス>` か `server:<名前>` のみ受理。`:`区切りだと登録されず、MCPログに `Channel notifications skipped: server plugin:discord:discord not in --channels list for this session` が出て受信通知が全部捨てられる（Bot側の送信・fetchは正常に動くので気づきにくい）。

## 反応しない時の診断手順
1. MCPログ確認: `~/Library/Caches/claude-cli-nodejs/-Users-kusakawatakuya/mcp-logs-plugin-discord-discord/` の最新.jsonlで「Channel notifications skipped」を探す
2. トークン/Intent確認: `curl -H "Authorization: Bot <token>" https://discord.com/api/v10/applications/@me` → flags bit19（MESSAGE_CONTENT_LIMITED）が立っていればOK
3. 残存プロセス: 過去セッションのbunサーバーが `ps aux | grep "discord/0.0.4"` で多数残ることがある（各ターミナルタブのclaudeセッションの子）。古いタブを閉じれば消える

## 設定の所在
- トークン: `~/.claude/channels/discord/.env`（Bot=kusakawa-assistant）
- アクセス: `~/.claude/channels/discord/access.json`（dmPolicy=allowlist・草川のDiscord ID 1122069094166958121 のみ許可）
- DMチャンネルID: 1499359623013208104
