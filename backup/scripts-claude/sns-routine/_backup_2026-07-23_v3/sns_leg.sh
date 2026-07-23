#!/bin/bash
# SNSルーティンv2 Phase3ローカル化: SNS便4本（morning_push/morning_reply/evening_push/evening_reply）共通ランナー
# クラウドRoutineがdiscord.comへの接続をブロックする（CONNECT 403確認済・2026-07-14）ため
# Macのlaunchdでローカル実行する。Macはsleep=0で夜間も稼働しトークンはローカル.envのみに留まる。
#
# reply系はゼロコストガード: _menu_state.json（当日のpush便が書く）が無い/古い/leg不一致、
# または本人の新規返信が0件なら claude を起動せず即 ok で終了する。
# push系は毎回 claude -p を起動する。
set -u
DIR="$HOME/.claude/scripts/sns-routine"
LOG="$DIR/_sns_legs.log"
MENU_STATE="$DIR/_menu_state.json"
CLAUDE_BIN="/Users/kusakawatakuya/.local/bin/claude"
TS() { date "+%Y-%m-%d %H:%M:%S"; }

LEG_ARG="${1:-}"
case "$LEG_ARG" in
  morning_push)   IS_PUSH=1; EXPECT_LEG="morning"; LABEL="朝便プッシュ 6:45" ;;
  evening_push)   IS_PUSH=1; EXPECT_LEG="evening"; LABEL="夕便プッシュ 16:30" ;;
  morning_reply)  IS_PUSH=0; EXPECT_LEG="morning"; LABEL="朝返信処理 7:30" ;;
  evening_reply)  IS_PUSH=0; EXPECT_LEG="evening"; LABEL="夕返信処理 17:15" ;;
  *)
    echo "usage: sns_leg.sh <morning_push|morning_reply|evening_push|evening_reply>" >&2
    exit 2
    ;;
esac

STATUS_KEY="sns_${LEG_ARG}"
PROMPT_FILE="$DIR/leg_${LEG_ARG}.md"
ALLOWED_TOOLS="Read,Write,Bash(python3 $DIR/discord_api.py *),Bash(grep *),Bash(date *),mcp__claude_ai_Notion__*"

echo "[$(TS)] ---- sns_leg ${LEG_ARG} start ----" >> "$LOG"

if [ "$IS_PUSH" -eq 0 ]; then
  # ---- reply系ゼロコストガード ----
  TODAY=$(TZ=Asia/Tokyo date +%Y-%m-%d)

  if [ ! -f "$MENU_STATE" ]; then
    echo "[$(TS)] no _menu_state.json -> skip (no claude launch)" >> "$LOG"
    python3 "$DIR/update_status.py" "$STATUS_KEY" ok "メニューなし"
    echo "[$(TS)] ---- sns_leg ${LEG_ARG} end (skipped) ----" >> "$LOG"
    exit 0
  fi

  MENU_LEG=$(python3 -c "import json,sys
try:
    d=json.load(open('$MENU_STATE'))
    print(d.get('leg',''))
except Exception:
    print('')" 2>>"$LOG")
  MENU_DATE=$(python3 -c "import json,sys
try:
    d=json.load(open('$MENU_STATE'))
    print(d.get('date',''))
except Exception:
    print('')" 2>>"$LOG")
  MENU_MSG_ID=$(python3 -c "import json,sys
try:
    d=json.load(open('$MENU_STATE'))
    print(d.get('menu_msg_id',''))
except Exception:
    print('')" 2>>"$LOG")

  if [ "$MENU_DATE" != "$TODAY" ] || [ "$MENU_LEG" != "$EXPECT_LEG" ] || [ -z "$MENU_MSG_ID" ]; then
    echo "[$(TS)] _menu_state.json stale/mismatch (date=$MENU_DATE leg=$MENU_LEG expect=$EXPECT_LEG today=$TODAY) -> skip" >> "$LOG"
    python3 "$DIR/update_status.py" "$STATUS_KEY" ok "メニューなし"
    echo "[$(TS)] ---- sns_leg ${LEG_ARG} end (skipped) ----" >> "$LOG"
    exit 0
  fi

  READ_JSON=$(python3 "$DIR/discord_api.py" read "$MENU_MSG_ID" 2>>"$LOG")
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
    echo "[$(TS)] 0 user replies since menu_msg_id=$MENU_MSG_ID -> skip (no claude launch)" >> "$LOG"
    python3 "$DIR/update_status.py" "$STATUS_KEY" ok "返信なし"
    echo "[$(TS)] ---- sns_leg ${LEG_ARG} end (skipped) ----" >> "$LOG"
    exit 0
  fi

  echo "[$(TS)] $USER_COUNT user replies found -> claude -p" >> "$LOG"
fi

# ---- push系は常に、reply系は新規返信ありのときだけここに到達 ----
cd "$HOME"
if "$CLAUDE_BIN" -p "$(cat "$PROMPT_FILE")" \
    --allowedTools "$ALLOWED_TOOLS" \
    >> "$LOG" 2>&1; then
  python3 "$DIR/update_status.py" "$STATUS_KEY" ok "${LABEL} 実行完了"
  echo "[$(TS)] ---- sns_leg ${LEG_ARG} end (ok) ----" >> "$LOG"
else
  RC=$?
  echo "[$(TS)] claude -p failed (rc=$RC)" >> "$LOG"
  python3 "$DIR/update_status.py" "$STATUS_KEY" error "${LABEL} 失敗（ログ確認・翌便が繰越処理）"
  echo "[$(TS)] ---- sns_leg ${LEG_ARG} end (error) ----" >> "$LOG"
  exit 1
fi
