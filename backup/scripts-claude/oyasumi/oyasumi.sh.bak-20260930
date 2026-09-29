#!/bin/bash
# oyasumi 夜間自動実行（launchd 23:30起動・2026-08-20 自動化）
# 手動起動（「おやすみ」）が1ヶ月0件で夜のまとめが止まっていたため、
# form-intake / news-briefing と同じ夜間バッチ方式に寄せた。
# 正本手順は ~/.claude/skills/oyasumi/SKILL.md（oyasumi_prompt.md はそれを読ませる薄いラッパー）
set -u
DIR="$HOME/.claude/scripts/oyasumi"
LOG="$DIR/_oyasumi.log"
CLAUDE_BIN="/Users/kusakawatakuya/.local/bin/claude"
UPDATE_STATUS="$HOME/.claude/scripts/sns-routine/update_status.py"
TS() { date "+%Y-%m-%d %H:%M:%S"; }
echo "[$(TS)] ---- oyasumi start ----" >> "$LOG"

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

ALLOWED_TOOLS="Read,Write,Edit,Bash(python3 $HOME/.claude/scripts/todoist/td.py *),Bash(python3 $UPDATE_STATUS *),Bash(date *),Bash(grep *),Bash(head *),Bash(tail *),Bash(wc *),ToolSearch,mcp__claude_ai_Notion__*,mcp__claude_ai_Google_Drive__*,mcp__claude_ai_Google_Calendar__*"

cd "$HOME"
CLAUDE_OK=0
for ATTEMPT in 1 2; do
  if "$CLAUDE_BIN" -p "$(cat "$DIR/oyasumi_prompt.md")" \
      --allowedTools "$ALLOWED_TOOLS" \
      >> "$LOG" 2>&1; then
    CLAUDE_OK=1
    break
  fi
  RC=$?
  echo "[$(TS)] claude -p failed (rc=$RC, attempt $ATTEMPT)" >> "$LOG"
  [ "$ATTEMPT" = "1" ] && { echo "[$(TS)] retrying in 20min" >> "$LOG"; sleep 1200; wait_net; }
done

if [ "$CLAUDE_OK" != "1" ]; then
  python3 "$UPDATE_STATUS" oyasumi error "claude -p が2回とも失敗（$DIR/_oyasumi.log 参照）" 2>/dev/null
fi
echo "[$(TS)] ---- oyasumi end (ok=$CLAUDE_OK) ----" >> "$LOG"
