#!/bin/bash
# news_briefing.sh — 朝のニュース収集 v4-local ランナー（2026-07-22新設・毎朝6:05 launchd）
# 経緯: クラウドRoutine（trig_01WXgkt4JqANvhi1YuQLGsEQ）は実行環境が外向きHTTPSを
# 全遮断（WebSearch/WebFetch/curl→403）で毎朝「0件」の空ダイジェスト上書きを続けたため
# 2026-07-22に無効化し、SNS便4本（sns_leg.sh）と同じローカルlaunchd実行に移行した。
# 実行時刻は6:05（クラウド旧6:00の後勝ち不要になったが、6:45朝便に間に合わせる）。
set -u
DIR="$HOME/.claude/scripts/sns-routine"
LOG="$DIR/_news_briefing.log"
CLAUDE_BIN="/Users/kusakawatakuya/.local/bin/claude"
TS() { date "+%Y-%m-%d %H:%M:%S"; }

PROMPT_FILE="$DIR/leg_news_briefing.md"
# ToolSearch は必須: headless実行ではNotion/Gmail MCPがdeferredで起動するため、
# ToolSearchでスキーマをロードしないと「未接続」と誤判定して不発になる（2026-07-17教訓）
ALLOWED_TOOLS="Read,Write,Bash(date *),Bash(grep *),ToolSearch,WebSearch,WebFetch,mcp__claude_ai_Notion__*,mcp__claude_ai_Gmail__*"

echo "[$(TS)] ---- news_briefing start ----" >> "$LOG"

cd "$HOME"
if "$CLAUDE_BIN" -p "$(cat "$PROMPT_FILE")" \
    --allowedTools "$ALLOWED_TOOLS" \
    >> "$LOG" 2>&1; then
  # rc=0でも「🚨中止」で終わるケース（Notion MCP本物の不在）を検出してstatusに反映
  if tail -5 "$LOG" | grep -q '🚨 news-briefing'; then
    python3 "$DIR/update_status.py" news_briefing error "ニュース収集 6:05 中止（Notion MCP不在等・ログ確認）"
    echo "[$(TS)] ---- news_briefing end (aborted) ----" >> "$LOG"
    exit 1
  fi
  python3 "$DIR/update_status.py" news_briefing ok "ニュース収集 6:05 完了"
  echo "[$(TS)] ---- news_briefing end (ok) ----" >> "$LOG"
else
  RC=$?
  echo "[$(TS)] claude -p failed (rc=$RC)" >> "$LOG"
  python3 "$DIR/update_status.py" news_briefing error "ニュース収集 6:05 失敗（ログ確認・朝便はアーカイブ由来で継続）"
  echo "[$(TS)] ---- news_briefing end (error) ----" >> "$LOG"
  exit 1
fi
