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

# ネットワーク疎通待ち（スリープ復帰直後のWi-Fi未接続対策・最大3分）
# nightly_intake.sh と同じ実装。2026-07-26にENOTFOUNDで落ちた再発防止（2026-07-27追加）
wait_net() {
  local i
  for i in $(seq 1 18); do
    curl -s -m 5 -o /dev/null "https://api.anthropic.com/" && return 0
    sleep 10
  done
  echo "[$(TS)] net wait timeout (3min)" >> "$LOG"
  return 1
}

cd "$HOME"
RUN_OK=0
for ATTEMPT in 1 2; do
  wait_net
  if "$CLAUDE_BIN" -p "$(cat "$PROMPT_FILE")" \
      --model claude-sonnet-5 \
      --allowedTools "$ALLOWED_TOOLS" \
      >> "$LOG" 2>&1; then
    # rc=0でも「🚨中止」で終わるケース（Notion MCP本物の不在）を検出してstatusに反映
    # 認証系の不在はリトライでは直らないため、ここでは再試行せず即中止する
    if tail -5 "$LOG" | grep -q '🚨 news-briefing'; then
      python3 "$DIR/update_status.py" news_briefing error "ニュース収集 6:05 中止（Notion MCP不在等・ログ確認）"
      echo "[$(TS)] ---- news_briefing end (aborted) ----" >> "$LOG"
      exit 1
    fi
    RUN_OK=1
    break
  fi
  RC=$?
  echo "[$(TS)] claude -p failed (rc=$RC, attempt $ATTEMPT)" >> "$LOG"
  # ログイン切れ（Not logged in）はリトライしても直らないので即抜ける
  if tail -5 "$LOG" | grep -q 'Not logged in'; then
    echo "[$(TS)] not logged in -> no retry" >> "$LOG"
    python3 "$DIR/update_status.py" news_briefing error "ニュース収集 6:05 失敗（claude CLI未ログイン・対話セッションで /login が必要）"
    echo "[$(TS)] ---- news_briefing end (error) ----" >> "$LOG"
    exit 1
  fi
  [ "$ATTEMPT" = "1" ] && { echo "[$(TS)] retrying in 10min" >> "$LOG"; sleep 600; }
done

if [ "$RUN_OK" = "1" ]; then
  python3 "$DIR/update_status.py" news_briefing ok "ニュース収集 6:05 完了"
  echo "[$(TS)] ---- news_briefing end (ok) ----" >> "$LOG"
  # 1行通知（2026-09-06）: 件数だけ #納品 へ
  SUMMARY=$(grep -oE "新規登録[0-9]+件|続報[0-9]+件" "$LOG" | tail -2 | tr '\n' '・' | sed 's/・$//')
  python3 "$DIR/discord_api.py" notify "ニュース便 $(date +%-m/%-d) 完了：${SUMMARY:-件数不明}（📰ニュースDB／おはようで表示）" >> "$LOG" 2>&1 || true
else
  python3 "$DIR/update_status.py" news_briefing error "ニュース収集 6:05 失敗（2回試行・ログ確認・朝便はアーカイブ由来で継続）"
  echo "[$(TS)] ---- news_briefing end (error) ----" >> "$LOG"
  exit 1
fi
