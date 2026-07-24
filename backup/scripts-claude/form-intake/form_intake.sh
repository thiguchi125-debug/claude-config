#!/bin/bash
# ご意見箱フォーム夜間自動取込（launchd 3:30起動）
# 正本手順は ~/.claude/skills/form-intake/SKILL.md（intake_prompt.mdはそれを読んで実行する薄いラッパー）
set -u
DIR="$HOME/.claude/scripts/form-intake"
LOG="$DIR/_intake.log"
CLAUDE_BIN="/Users/kusakawatakuya/.local/bin/claude"
UPDATE_STATUS="$HOME/.claude/scripts/sns-routine/update_status.py"
TS() { date "+%Y-%m-%d %H:%M:%S"; }
echo "[$(TS)] ---- form_intake start ----" >> "$LOG"

# ネットワーク疎通待ち（スリープ復帰直後のWi-Fi未接続対策・最大3分）
wait_net() {
  local i
  for i in $(seq 1 18); do
    curl -s -m 5 -o /dev/null "https://www.googleapis.com/generate_204" && return 0
    sleep 10
  done
  echo "[$(TS)] net wait timeout (3min) -> continue anyway" >> "$LOG"
  return 1
}
wait_net

# ToolSearch必須: headlessではDrive/Notion MCPがdeferredで起動するため（2026-07-17修理と同じ対策）
ALLOWED_TOOLS="Read,Write,Edit,Bash(python3 $UPDATE_STATUS *),Bash(base64 *),Bash(wc *),Bash(tail *),Bash(head *),Bash(grep *),Bash(date *),ToolSearch,mcp__claude_ai_Google_Drive__*,mcp__claude_ai_Notion__*"

cd "$HOME"
CLAUDE_OK=0
for ATTEMPT in 1 2; do
  if "$CLAUDE_BIN" -p "$(cat "$DIR/intake_prompt.md")" \
      --allowedTools "$ALLOWED_TOOLS" \
      >> "$LOG" 2>&1; then
    CLAUDE_OK=1
    break
  fi
  RC=$?
  echo "[$(TS)] claude -p failed (rc=$RC, attempt $ATTEMPT)" >> "$LOG"
  [ "$ATTEMPT" = "1" ] && { echo "[$(TS)] retrying in 30min" >> "$LOG"; sleep 1800; wait_net; }
done

if [ "$CLAUDE_OK" = "1" ]; then
  echo "[$(TS)] ---- form_intake end (ok) ----" >> "$LOG"
else
  python3 "$UPDATE_STATUS" form_intake error "フォーム取込失敗（2回試行・state未更新=取りこぼしなし・翌夜再試行 or 手動「フォーム取り込んで」）"
  echo "[$(TS)] ---- form_intake end (error) ----" >> "$LOG"
  exit 1
fi
