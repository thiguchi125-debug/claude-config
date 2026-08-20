#!/bin/bash
# SNSルーティンv2 Phase1+Phase3: Discord投げ込み夜間振り分け（launchd 3:10起動）
# ステージ1=triage振り分け／ステージ2=候補パック生成／ステージ3=動画夜間フル制作
set -u
DIR="$HOME/.claude/scripts/sns-routine"
LOG="$DIR/_intake.log"
CLAUDE_BIN="/Users/kusakawatakuya/.local/bin/claude"
TS() { date "+%Y-%m-%d %H:%M:%S"; }
echo "[$(TS)] ---- start ----" >> "$LOG"

# ---- 朝デッドライン（2026-08-21追加） ----
# 夜間ジョブが retry のスリープを跨いで朝の混雑帯（news-briefing 6:05 / SNS便 6:45）に
# 着地し、5セッション同時稼働でトークンを一気に焼く事故の再発防止。
# 05:30を過ぎたらその夜は打ち切る。Discord原本と _pending_tasks.jsonl は残るので翌夜に回る。
MORNING_DEADLINE=530
past_deadline() {
  local now; now=$((10#$(date +%H%M)))
  [ "$now" -ge "$MORNING_DEADLINE" ] && [ "$now" -lt 1200 ]
}
abort_morning() {
  echo "[$(TS)] ABORT: 朝デッドライン($MORNING_DEADLINE)超過のため中断（$1）。翌夜に持ち越し" >> "$LOG"
  python3 "$DIR/update_status.py" discord_intake error "朝デッドライン超過で中断（$1）・翌夜再処理"
  exit 0
}
past_deadline && abort_morning "起動時点で既に朝"

# ネットワーク疎通待ち（スリープ復帰直後のWi-Fi未接続対策・最大3分）
# 2026-07-18〜21にENOTFOUND/Connection closedで4夜連続失敗した再発防止（2026-07-23追加）
wait_net() {
  local i
  for i in $(seq 1 18); do
    curl -s -m 5 -o /dev/null "https://discord.com/api/v10/gateway" && return 0
    sleep 10
  done
  echo "[$(TS)] net wait timeout (3min)" >> "$LOG"
  return 1
}

NEW_JSON="$DIR/_new_messages.json"
FETCH_OK=0
for ATTEMPT in 1 2; do
  wait_net
  if python3 "$DIR/discord_api.py" fetch > "$NEW_JSON" 2>>"$LOG"; then
    FETCH_OK=1
    break
  fi
  echo "[$(TS)] FETCH_ERROR (attempt $ATTEMPT)" >> "$LOG"
  [ "$ATTEMPT" = "1" ] && { echo "[$(TS)] retrying fetch in 5min" >> "$LOG"; sleep 300; past_deadline && abort_morning "fetch retry待ちで朝になった"; }
done
if [ "$FETCH_OK" = "0" ]; then
  python3 "$DIR/update_status.py" discord_intake error "Discord API取得失敗（2回試行・原本はDiscordに保全）"
  exit 1
fi

COUNT=$(python3 -c "import json;print(len(json.load(open('$NEW_JSON'))))")
PENDING=$(test -s "$DIR/_pending_tasks.jsonl" && echo 1 || echo 0)

# ---- ステージ1: triage振り分け（新着 or 前夜提案の残りがある夜のみ実行） ----
if [ "$COUNT" -eq 0 ] && [ "$PENDING" -eq 0 ]; then
  echo "[$(TS)] no new messages, no pending" >> "$LOG"
  python3 "$DIR/update_status.py" discord_intake ok "新着0件"
else
  echo "[$(TS)] $COUNT new messages (pending=$PENDING) -> claude -p" >> "$LOG"
  cd "$HOME"
  TRIAGE_OK=0
  for ATTEMPT in 1 2; do
    if "$CLAUDE_BIN" -p "$(cat "$DIR/triage_prompt.md")" \
        --allowedTools "Read,Write,Edit,Bash(python3 $DIR/discord_api.py *),Bash(python3 $HOME/.claude/scripts/todoist/td.py *),ToolSearch,mcp__claude_ai_Notion__*,mcp__claude_ai_Todoist__*" \
        >> "$LOG" 2>&1; then
      TRIAGE_OK=1
      break
    fi
    echo "[$(TS)] TRIAGE_ERROR (attempt $ATTEMPT)" >> "$LOG"
    [ "$ATTEMPT" = "1" ] && { echo "[$(TS)] retrying triage in 5min" >> "$LOG"; sleep 300; past_deadline && abort_morning "triage retry待ちで朝になった"; wait_net; }
  done
  if [ "$TRIAGE_OK" = "1" ]; then
    python3 "$DIR/update_status.py" discord_intake ok "${COUNT}件処理"
    echo "[$(TS)] stage1 done" >> "$LOG"
  else
    python3 "$DIR/update_status.py" discord_intake error "triage失敗（${COUNT}件・2回試行・原本保全済・翌夜再処理）"
    echo "[$(TS)] ---- end (triage error, stage2/3 skipped) ----" >> "$LOG"
    exit 1
  fi
fi

past_deadline && abort_morning "stage1完了時点で朝"

# ---- ステージ2: 候補パック生成（新着/pending処理があった夜、または週1回月曜は新着0件でも必ず） ----
DOW=$(date +%u)
# 2026-08-21: 停止中。起動条件が「Discord新着の有無」であって「💡候補の在庫」ではないため、
# ネタDBが空のまま15夜連続で0件パックを生成し続け、1夜あたり約2.7Mトークンを空焼きしていた。
# 仕組みの再設計が済むまでフラグで止める。再開は _pack_disabled を消すだけ。
if [ -f "$DIR/_pack_disabled" ]; then
  echo "[$(TS)] stage2 skipped (_pack_disabled: 再設計待ち)" >> "$LOG"
  python3 "$DIR/update_status.py" sns_pack ok "停止中（再設計待ち）"
elif [ "$COUNT" -gt 0 ] || [ "$PENDING" -eq 1 ] || [ "$DOW" = "1" ]; then
  echo "[$(TS)] stage2 pack -> claude -p (dow=$DOW)" >> "$LOG"
  cd "$HOME"
  if "$CLAUDE_BIN" -p "$(cat "$DIR/pack_prompt.md")" \
      --allowedTools "Read,Write,Bash(grep *),ToolSearch,mcp__claude_ai_Notion__*" \
      >> "$LOG" 2>&1; then
    python3 "$DIR/update_status.py" sns_pack ok "候補パック生成完了"
    echo "[$(TS)] stage2 done" >> "$LOG"
  else
    echo "[$(TS)] PACK_ERROR" >> "$LOG"
    python3 "$DIR/update_status.py" sns_pack error "候補パック生成失敗（triageは正常・翌夜再試行）"
    echo "[$(TS)] stage2 failed (non-fatal, continuing to stage3)" >> "$LOG"
  fi
else
  echo "[$(TS)] stage2 skipped (no new/pending, not Monday)" >> "$LOG"
fi

# ---- ステージ3: 動画夜間フル制作（_video_queue.txt が非空の時だけ起動・0件夜はclaude起動なし） ----
past_deadline && abort_morning "stage2完了時点で朝"
VQ="$DIR/_video_queue.txt"
if [ -s "$VQ" ]; then
  echo "[$(TS)] stage3 video -> claude -p" >> "$LOG"
  cd "$HOME"
  if "$CLAUDE_BIN" -p "$(cat "$DIR/video_stage_prompt.md")" \
      --allowedTools "Read,Write,Edit,Bash(python3 /Users/kusakawatakuya/.claude/agents/knowledge/design_system/*),Bash(grep *),Bash(cp *),Bash(mkdir *),Bash(/Applications/Google Chrome.app/Contents/MacOS/Google Chrome *),ToolSearch,mcp__claude_ai_Notion__*" \
      >> "$LOG" 2>&1; then
    python3 "$DIR/update_status.py" sns_video ok "動画リクエスト処理完了"
    echo "[$(TS)] stage3 done" >> "$LOG"
  else
    echo "[$(TS)] VIDEO_ERROR" >> "$LOG"
    python3 "$DIR/update_status.py" sns_video error "動画フル制作失敗（_video_queue.txt保持・翌夜再試行）"
  fi
else
  echo "[$(TS)] stage3 skipped (no video queue)" >> "$LOG"
fi

echo "[$(TS)] ---- end ----" >> "$LOG"
exit 0
