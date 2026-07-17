#!/bin/bash
# 一時診断用: launchd環境でNotion MCPに到達できるかを記録する（原因特定後に削除）
set -u
OUT="$HOME/.claude/scripts/sns-routine/_probe_launchd.log"
CLAUDE_BIN="/Users/kusakawatakuya/.local/bin/claude"
{
  echo "===== probe start $(date '+%F %T') ====="
  echo "--- whoami / id ---"; whoami; id
  echo "--- env ---"; env | sort
  echo "--- security list-keychains ---"; security list-keychains 2>&1
  echo "--- claude mcp list ---"; cd "$HOME" && "$CLAUDE_BIN" mcp list 2>&1
  echo "--- claude -p notion probe ---"
  cd "$HOME" && "$CLAUDE_BIN" -p "Notion MCPが使えるなら 'NOTION_OK' とだけ、使えないなら 'NOTION_MCP_ABSENT' とだけ出力。" \
    --allowedTools "mcp__claude_ai_Notion__*" 2>&1
  echo ""
  echo "===== probe end $(date '+%F %T') ====="
} >> "$OUT" 2>&1
