#!/bin/bash
# gyakusan 週次自動実行（launchd 毎週月曜6:30・2026-08-20 自動化）
# 従来は「月曜のohayoが呼ぶ」設計だったが、30日で月曜のohayoは1回だけ＝実質止まっていた。
# 単独で回して結果を _gyakusan_status.json に残し、次にohayoを回したときに拾わせる。
# 正本手順は ~/.claude/skills/gyakusan/SKILL.md
set -u
DIR="$HOME/.claude/scripts/gyakusan"
LOG="$DIR/_gyakusan.log"
CLAUDE_BIN="/Users/kusakawatakuya/.local/bin/claude"
UPDATE_STATUS="$HOME/.claude/scripts/sns-routine/update_status.py"
TS() { date "+%Y-%m-%d %H:%M:%S"; }
echo "[$(TS)] ---- gyakusan start ----" >> "$LOG"

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

# td.py は読み取りのみ許可（add/done は渡さない＝勝手な登録を構造的に不可能にする）
ALLOWED_TOOLS="Read,Write,Bash(python3 $HOME/.claude/scripts/todoist/td.py week),Bash(python3 $HOME/.claude/scripts/todoist/td.py list *),Bash(python3 $UPDATE_STATUS *),Bash(date *),ToolSearch,mcp__claude_ai_Google_Calendar__*,mcp__claude_ai_Notion__*"

cd "$HOME"
CLAUDE_OK=0
for ATTEMPT in 1 2; do
  if "$CLAUDE_BIN" -p "$(cat "$DIR/gyakusan_prompt.md")" \
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
  python3 "$UPDATE_STATUS" gyakusan error "claude -p が2回とも失敗（$DIR/_gyakusan.log 参照）" 2>/dev/null
fi
echo "[$(TS)] ---- gyakusan end (ok=$CLAUDE_OK) ----" >> "$LOG"
