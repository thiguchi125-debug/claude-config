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
# 自動ジョブでは /kugiri の引き継ぎメモを注入させない（2026-09-30: 注入されると
# 引き継ぎへの返事だけ書いて rc=0 で終わり、収集ゼロのまま ok 扱いになっていた）
export KUGIRI_NO_HANDOFF=1
# launchd はロケール未設定。日本語の加工で文字化け→Discord通知が毎日落ちていた（2026-09-30）
export LANG=ja_JP.UTF-8 LC_ALL=ja_JP.UTF-8

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
      --model claude-sonnet-5 --effort medium \
      --allowedTools "$ALLOWED_TOOLS" \
      >> "$LOG" 2>&1; then
    # rc=0でも「🚨中止」で終わるケース（Notion MCP本物の不在）を検出してstatusに反映
    # 認証系の不在はリトライでは直らないため、ここでは再試行せず即中止する
    # rc=0でも完了行が無ければ収集していない（別の話題に返事して終わった等）→失敗扱いで再試行
    if ! tail -15 "$LOG" | grep -qE '(✅ )?news-briefing v4-local 完了|🚨 news-briefing'; then
      echo "[$(TS)] 完了行なし＝収集していない (attempt $ATTEMPT)" >> "$LOG"
      [ "$ATTEMPT" = "1" ] && { echo "[$(TS)] retrying in 10min" >> "$LOG"; sleep 600; }
      continue
    fi
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
  # Discord完了通知は2026-09-30廃止（成否はohayoの🚨で確認）
else
  python3 "$DIR/update_status.py" news_briefing error "ニュース収集 6:05 失敗（2回試行・ログ確認・朝便はアーカイブ由来で継続）"
  echo "[$(TS)] ---- news_briefing end (error) ----" >> "$LOG"
  exit 1
fi
