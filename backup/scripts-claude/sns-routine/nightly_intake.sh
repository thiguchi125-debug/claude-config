#!/bin/bash
# SNSルーティンv2 Phase1: Discord投げ込みの夜間振り分け（launchd 3:10起動）
set -u
DIR="$HOME/.claude/scripts/sns-routine"
LOG="$DIR/_intake.log"
CLAUDE_BIN="/Users/kusakawatakuya/.local/bin/claude"
TS() { date "+%Y-%m-%d %H:%M:%S"; }
echo "[$(TS)] ---- start ----" >> "$LOG"

NEW_JSON="$DIR/_new_messages.json"
if ! python3 "$DIR/discord_api.py" fetch > "$NEW_JSON" 2>>"$LOG"; then
  echo "[$(TS)] FETCH_ERROR" >> "$LOG"
  python3 "$DIR/update_status.py" discord_intake error "Discord API取得失敗（原本はDiscordに保全）"
  exit 1
fi

COUNT=$(python3 -c "import json;print(len(json.load(open('$NEW_JSON'))))")
PENDING=$(test -s "$DIR/_pending_tasks.jsonl" && echo 1 || echo 0)
if [ "$COUNT" -eq 0 ] && [ "$PENDING" -eq 0 ]; then
  echo "[$(TS)] no new messages, no pending" >> "$LOG"
  python3 "$DIR/update_status.py" discord_intake ok "新着0件"
  exit 0
fi

echo "[$(TS)] $COUNT new messages (pending=$PENDING) -> claude -p" >> "$LOG"
cd "$HOME"
if "$CLAUDE_BIN" -p "$(cat "$DIR/triage_prompt.md")" \
    --allowedTools "Read,Write,Edit,Bash(python3 $DIR/discord_api.py *),Bash(python3 $HOME/.claude/scripts/todoist/td.py *),mcp__claude_ai_Notion__*,mcp__claude_ai_Todoist__*" \
    >> "$LOG" 2>&1; then
  python3 "$DIR/update_status.py" discord_intake ok "${COUNT}件処理"
  echo "[$(TS)] done" >> "$LOG"
else
  echo "[$(TS)] TRIAGE_ERROR" >> "$LOG"
  python3 "$DIR/update_status.py" discord_intake error "triage失敗（${COUNT}件・原本保全済・翌夜再処理）"
  exit 1
fi
