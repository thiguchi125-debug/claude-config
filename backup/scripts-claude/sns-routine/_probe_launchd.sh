#!/bin/bash
# 一時診断用: 便と同じallowedTools構成でNotion MCPがdeferredになるか確認
set -u
DIR="$HOME/.claude/scripts/sns-routine"
OUT="$DIR/_probe_launchd.log"
CLAUDE_BIN="/Users/kusakawatakuya/.local/bin/claude"
ALLOWED_TOOLS="Read,Write,Bash(python3 $DIR/discord_api.py *),Bash(grep *),Bash(date *),mcp__claude_ai_Notion__*"
{
  echo "===== probe2 start $(date '+%F %T') ====="
  cd "$HOME" && "$CLAUDE_BIN" -p "重要: ツールを一切呼ばずに、いま自分に見えている状態だけを報告してください。
1) mcp__claude_ai_Notion__notion-fetch のスキーマが最初からロード済みで即座に呼べる状態か？
2) それとも <system-reminder> で deferred と示され、ToolSearch でのロードが必要な状態か？
回答は次の1行だけ: 'EAGER' または 'DEFERRED' または 'NOT_PRESENT'" \
    --allowedTools "$ALLOWED_TOOLS" 2>&1
  echo ""
  echo "===== probe2 end $(date '+%F %T') ====="
} >> "$OUT" 2>&1
