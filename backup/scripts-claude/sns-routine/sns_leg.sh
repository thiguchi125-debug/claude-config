#!/bin/bash
# SNSルーティンv3: SNS便4本（morning_push/morning_reply/evening_push/evening_reply）共通ランナー
#
# ⚠️ 2026-08-26 簡素化: 稼働しているのは evening_push の1本だけ。
#    morning_push / morning_reply / evening_reply は launchd を停止し
#    ~/Library/LaunchAgents/_stopped_2026-08-26/ へ退避した（草川指示「最低限のシンプルな運用」）。
#    Discordへの納品も廃止（discord_api.py の INBOX_ONLY で機械的に拒否）。
#    完成原稿の受け渡しは drafts/ と 📣投稿管理DB のみ。このランナー自体は4本とも
#    動かせる状態で残してあるので、戻すときは plist を戻すだけでよい。
# v3（2026-07-23）: メニュー選択制を廃止し、push便が完成原稿をDMへ直接納品する。
#   - push便=毎回 claude -p 起動（朝6:45／夕19:30）
#   - reply便=修正返信の処理専用（朝7:30／夕20:15）。_delivery_state.json（当日のpush便が書く）が
#     無い/古い/leg不一致、または本人の新規返信が0件なら claude を起動せず即 ok で終了（ゼロコストガード）
#   - claude -p 失敗時は15分後に1回だけ再試行（2026-07-22朝便ENOTFOUND対策）
#   - 起動時にネットワーク疎通待ち（スリープ復帰直後のWi-Fi未接続対策・最大3分）
# クラウドRoutineがdiscord.comへの接続をブロックする（CONNECT 403確認済・2026-07-14）ため
# Macのlaunchdでローカル実行する。Macはsleep=0で夜間も稼働しトークンはローカル.envのみに留まる。
set -u
DIR="$HOME/.claude/scripts/sns-routine"
LOG="$DIR/_sns_legs.log"
DELIVERY_STATE="$DIR/_delivery_state.json"
CLAUDE_BIN="/Users/kusakawatakuya/.local/bin/claude"
TS() { date "+%Y-%m-%d %H:%M:%S"; }

LEG_ARG="${1:-}"
case "$LEG_ARG" in
  morning_push)   IS_PUSH=1; EXPECT_LEG="morning"; LABEL="朝納品便 6:45";  SCHED_MIN=405  ;;
  evening_push)   IS_PUSH=1; EXPECT_LEG="evening"; LABEL="夕納品便 19:30"; SCHED_MIN=1170 ;;
  morning_reply)  IS_PUSH=0; EXPECT_LEG="morning"; LABEL="朝返信処理 7:30"; SCHED_MIN=450 ;;
  evening_reply)  IS_PUSH=0; EXPECT_LEG="evening"; LABEL="夕返信処理 20:15"; SCHED_MIN=1215 ;;
  *)
    echo "usage: sns_leg.sh <morning_push|morning_reply|evening_push|evening_reply>" >&2
    exit 2
    ;;
esac

STATUS_KEY="sns_${LEG_ARG}"
PROMPT_FILE="$DIR/leg_${LEG_ARG}.md"

# ---- 遅延発火ガード（v3.1・2026-07-25追加）----
# Macがバッテリー駆動やスリープで定時に発火できず、数時間遅れて起動した便は見送る。
# 遅延便が翌便と並走して同テーマを二重納品した事故（7/23夕便が7/24朝便と並走）の再発防止。
# 120分以内の遅れは通常運転（多少遅れても納品する価値がある）。
NOW_MIN=$(( 10#$(TZ=Asia/Tokyo date +%H) * 60 + 10#$(TZ=Asia/Tokyo date +%M) ))
LATE_MIN=$(( NOW_MIN - SCHED_MIN ))
if [ "$LATE_MIN" -gt 120 ] || [ "$LATE_MIN" -lt -30 ]; then
  echo "[$(TS)] stale start (scheduled=${SCHED_MIN}min now=${NOW_MIN}min late=${LATE_MIN}min) -> skip" >> "$LOG"
  python3 "$DIR/update_status.py" "$STATUS_KEY" error "${LABEL} 遅延発火のため見送り（Mac電源/スリープ確認・次の定時便が繰越）"
  exit 0
fi

# ---- 排他ロック（v3.1・mkdirロック=macOSにflockが無いため）----
# 便同士の並走を防ぐ。5時間超の残置ロックは異常終了の遺物とみなして奪取。
LOCK="$DIR/_leg.lock.d"
WAITED=0
while ! mkdir "$LOCK" 2>/dev/null; do
  if [ -d "$LOCK" ] && [ -n "$(find "$LOCK" -maxdepth 0 -mmin +300 2>/dev/null)" ]; then
    echo "[$(TS)] stale lock (>5h) -> steal" >> "$LOG"
    rmdir "$LOCK" 2>/dev/null || rm -rf "$LOCK"
    continue
  fi
  if [ "$WAITED" -ge 600 ]; then
    echo "[$(TS)] another leg still running (lock wait 10min timeout) -> skip" >> "$LOG"
    python3 "$DIR/update_status.py" "$STATUS_KEY" error "${LABEL} 他便実行中のため見送り"
    exit 0
  fi
  sleep 30; WAITED=$((WAITED+30))
done
trap 'rmdir "$LOCK" 2>/dev/null' EXIT
# ToolSearch は必須: headless実行ではNotion/Gmail MCPがdeferredで起動するため、
# ToolSearchでスキーマをロードしないと「未接続」と誤判定して納品が不発になる（2026-07-17修理）
# v3追加: WebSearch/WebFetch=新風枠・一次記事の本文調査、Gmail MCP=iJAMPスキャン（規約適合ルート）
ALLOWED_TOOLS="Read,Write,Bash(python3 $DIR/discord_api.py *),Bash(grep *),Bash(date *),ToolSearch,WebSearch,WebFetch,mcp__claude_ai_Notion__*,mcp__claude_ai_Gmail__*"

echo "[$(TS)] ---- sns_leg ${LEG_ARG} start ----" >> "$LOG"

# ネットワーク疎通待ち（最大3分）。タイムアウトしてもclaude側リトライに賭けて続行する
wait_net() {
  local i
  for i in $(seq 1 18); do
    curl -s -m 5 -o /dev/null "https://discord.com/api/v10/gateway" && return 0
    sleep 10
  done
  echo "[$(TS)] net wait timeout (3min) -> continue anyway" >> "$LOG"
  return 1
}
wait_net

if [ "$IS_PUSH" -eq 0 ]; then
  # ---- reply系ゼロコストガード ----
  TODAY=$(TZ=Asia/Tokyo date +%Y-%m-%d)

  if [ ! -f "$DELIVERY_STATE" ]; then
    echo "[$(TS)] no _delivery_state.json -> skip (no claude launch)" >> "$LOG"
    python3 "$DIR/update_status.py" "$STATUS_KEY" ok "納品なし"
    echo "[$(TS)] ---- sns_leg ${LEG_ARG} end (skipped) ----" >> "$LOG"
    exit 0
  fi

  DLV_LEG=$(python3 -c "import json
try:
    d=json.load(open('$DELIVERY_STATE'))
    print(d.get('leg',''))
except Exception:
    print('')" 2>>"$LOG")
  DLV_DATE=$(python3 -c "import json
try:
    d=json.load(open('$DELIVERY_STATE'))
    print(d.get('date',''))
except Exception:
    print('')" 2>>"$LOG")
  DLV_MSG_ID=$(python3 -c "import json
try:
    d=json.load(open('$DELIVERY_STATE'))
    print(d.get('delivery_msg_id',''))
except Exception:
    print('')" 2>>"$LOG")

  if [ "$DLV_DATE" != "$TODAY" ] || [ "$DLV_LEG" != "$EXPECT_LEG" ] || [ -z "$DLV_MSG_ID" ]; then
    echo "[$(TS)] _delivery_state.json stale/mismatch (date=$DLV_DATE leg=$DLV_LEG expect=$EXPECT_LEG today=$TODAY) -> skip" >> "$LOG"
    python3 "$DIR/update_status.py" "$STATUS_KEY" ok "納品なし"
    echo "[$(TS)] ---- sns_leg ${LEG_ARG} end (skipped) ----" >> "$LOG"
    exit 0
  fi

  READ_JSON=$(python3 "$DIR/discord_api.py" read "$DLV_MSG_ID" 2>>"$LOG")
  READ_RC=$?
  if [ $READ_RC -ne 0 ]; then
    echo "[$(TS)] discord_api.py read failed (rc=$READ_RC)" >> "$LOG"
    python3 "$DIR/update_status.py" "$STATUS_KEY" error "Discord受信失敗（ログ確認・翌便が再試行）"
    echo "[$(TS)] ---- sns_leg ${LEG_ARG} end (read error) ----" >> "$LOG"
    exit 1
  fi

  USER_COUNT=$(echo "$READ_JSON" | python3 -c "import json,sys
try:
    msgs=json.load(sys.stdin)
    print(sum(1 for m in msgs if m.get('is_user')))
except Exception:
    print(0)")

  if [ "$USER_COUNT" -eq 0 ]; then
    echo "[$(TS)] 0 user replies since delivery_msg_id=$DLV_MSG_ID -> skip (no claude launch)" >> "$LOG"
    python3 "$DIR/update_status.py" "$STATUS_KEY" ok "返信なし（納品原稿はそのまま有効）"
    echo "[$(TS)] ---- sns_leg ${LEG_ARG} end (skipped) ----" >> "$LOG"
    exit 0
  fi

  echo "[$(TS)] $USER_COUNT user replies found -> claude -p" >> "$LOG"
fi

# ---- push系は常に、reply系は新規返信ありのときだけここに到達 ----
# claude -p 失敗時は15分後に1回だけ再試行（ネットワーク瞬断・API一時障害対策）
cd "$HOME"
CLAUDE_OK=0
for ATTEMPT in 1 2; do
  # caffeinate -i: 実行中のアイドルスリープを抑止（バッテリー駆動時の蓋閉じスリープまでは防げない）
  if /usr/bin/caffeinate -i "$CLAUDE_BIN" -p "$(cat "$PROMPT_FILE")" \
      --max-turns 60 \
      --allowedTools "$ALLOWED_TOOLS" \
      >> "$LOG" 2>&1; then
    CLAUDE_OK=1
    break
  fi
  RC=$?
  echo "[$(TS)] claude -p failed (rc=$RC, attempt $ATTEMPT)" >> "$LOG"
  [ "$ATTEMPT" = "1" ] && { echo "[$(TS)] retrying in 15min" >> "$LOG"; sleep 900; wait_net; }
done

if [ "$CLAUDE_OK" = "1" ]; then
  python3 "$DIR/update_status.py" "$STATUS_KEY" ok "${LABEL} 実行完了"
  echo "[$(TS)] ---- sns_leg ${LEG_ARG} end (ok) ----" >> "$LOG"
else
  python3 "$DIR/update_status.py" "$STATUS_KEY" error "${LABEL} 失敗（2回試行・ログ確認・翌便が繰越処理）"
  echo "[$(TS)] ---- sns_leg ${LEG_ARG} end (error) ----" >> "$LOG"
  exit 1
fi
