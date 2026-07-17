#!/bin/bash
# SNSルーティンv2 Phase1+Phase3: Discord投げ込み夜間振り分け（launchd 3:10起動）
# ステージ1=triage振り分け／ステージ2=候補パック生成／ステージ3=動画夜間フル制作
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

# ---- ステージ1: triage振り分け（新着 or 前夜提案の残りがある夜のみ実行） ----
if [ "$COUNT" -eq 0 ] && [ "$PENDING" -eq 0 ]; then
  echo "[$(TS)] no new messages, no pending" >> "$LOG"
  python3 "$DIR/update_status.py" discord_intake ok "新着0件"
else
  echo "[$(TS)] $COUNT new messages (pending=$PENDING) -> claude -p" >> "$LOG"
  cd "$HOME"
  if "$CLAUDE_BIN" -p "$(cat "$DIR/triage_prompt.md")" \
      --allowedTools "Read,Write,Edit,Bash(python3 $DIR/discord_api.py *),Bash(python3 $HOME/.claude/scripts/todoist/td.py *),mcp__claude_ai_Notion__*,mcp__claude_ai_Todoist__*" \
      >> "$LOG" 2>&1; then
    python3 "$DIR/update_status.py" discord_intake ok "${COUNT}件処理"
    echo "[$(TS)] stage1 done" >> "$LOG"
  else
    echo "[$(TS)] TRIAGE_ERROR" >> "$LOG"
    python3 "$DIR/update_status.py" discord_intake error "triage失敗（${COUNT}件・原本保全済・翌夜再処理）"
    echo "[$(TS)] ---- end (triage error, stage2/3 skipped) ----" >> "$LOG"
    exit 1
  fi
fi

# ---- ステージ2: 候補パック生成（新着/pending処理があった夜、または週1回月曜は新着0件でも必ず） ----
DOW=$(date +%u)
if [ "$COUNT" -gt 0 ] || [ "$PENDING" -eq 1 ] || [ "$DOW" = "1" ]; then
  echo "[$(TS)] stage2 pack -> claude -p (dow=$DOW)" >> "$LOG"
  cd "$HOME"
  if "$CLAUDE_BIN" -p "$(cat "$DIR/pack_prompt.md")" \
      --allowedTools "Read,Write,Bash(grep *),mcp__claude_ai_Notion__*" \
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
VQ="$DIR/_video_queue.txt"
if [ -s "$VQ" ]; then
  echo "[$(TS)] stage3 video -> claude -p" >> "$LOG"
  cd "$HOME"
  if "$CLAUDE_BIN" -p "$(cat "$DIR/video_stage_prompt.md")" \
      --allowedTools "Read,Write,Edit,Bash(python3 /Users/kusakawatakuya/.claude/agents/knowledge/design_system/*),Bash(grep *),Bash(cp *),Bash(mkdir *),Bash(/Applications/Google Chrome.app/Contents/MacOS/Google Chrome *),mcp__claude_ai_Notion__*" \
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
