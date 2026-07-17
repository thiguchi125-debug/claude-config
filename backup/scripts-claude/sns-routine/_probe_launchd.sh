#!/bin/bash
set -u
DIR="$HOME/.claude/scripts/sns-routine"
OUT="$DIR/_probe_launchd.log"
CLAUDE_BIN="/Users/kusakawatakuya/.local/bin/claude"
ALLOWED_TOOLS="Read,Write,Bash(python3 $DIR/discord_api.py *),Bash(grep *),Bash(date *),ToolSearch,mcp__claude_ai_Notion__*"
{
  echo "===== probe3 (fix candidate) start $(date '+%F %T') ====="
  cd "$HOME" && "$CLAUDE_BIN" -p "【MCPツールの扱い・最優先】mcp__claude_ai_Notion__* はdeferred（スキーマ未ロード）で始まる場合がある。その状態は「未接続」ではない。Notionを使う前に必ず ToolSearch で query=\"select:mcp__claude_ai_Notion__notion-fetch,mcp__claude_ai_Notion__notion-search\" を実行してスキーマをロードすること。ToolSearchを試す前に「Notion未接続」と判定することを禁止する。

タスク: 上記に従いNotionツールをロードし、notion-fetch で id=391cf503-a68f-8194-be35-fec5aede8a5e を取得。成功したら 'NOTION_REACHED' とだけ、本当に到達不能なら 'NOTION_MCP_ABSENT' とだけ出力。" \
    --allowedTools "$ALLOWED_TOOLS" 2>&1
  echo ""
  echo "===== probe3 end $(date '+%F %T') ====="
} >> "$OUT" 2>&1
