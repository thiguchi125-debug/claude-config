#!/bin/bash
# SNSルーティンv2 Phase3: 日曜監査（迷子ゼロ締め工程・launchd 3:20起動）
# discord_api.py audit で直近7日の生メッセージ（reactions含む）を取得し、
# 草川本人の未リアクションメッセージを検出する。Claude起動なし・トークンゼロ。
set -u
DIR="$HOME/.claude/scripts/sns-routine"
LOG="$DIR/_intake.log"
REPORT="$DIR/_audit_report.md"
TS() { date "+%Y-%m-%d %H:%M:%S"; }
echo "[$(TS)] ---- sunday_audit start ----" >> "$LOG"

RESULT_JSON="$DIR/_audit_result.json"
if ! python3 "$DIR/discord_api.py" audit 7 > "$RESULT_JSON" 2>>"$LOG"; then
  echo "[$(TS)] AUDIT_FETCH_ERROR" >> "$LOG"
  python3 "$DIR/update_status.py" sns_audit error "監査API取得失敗（ログ確認）"
  echo "[$(TS)] ---- sunday_audit end (fetch error) ----" >> "$LOG"
  exit 1
fi

COUNT=$(python3 -c "import json;print(len(json.load(open('$RESULT_JSON'))))" 2>>"$LOG") || COUNT="?"

if [ "$COUNT" = "0" ]; then
  echo "[$(TS)] no unprocessed messages" >> "$LOG"
  python3 "$DIR/update_status.py" sns_audit ok "未処理0件"
else
  echo "[$(TS)] $COUNT unprocessed messages found" >> "$LOG"
  python3 - "$RESULT_JSON" "$REPORT" "$COUNT" <<'PYEOF'
import json, sys, datetime
result_path, report_path, count = sys.argv[1], sys.argv[2], sys.argv[3]
items = json.load(open(result_path))
lines = []
lines.append("# 日曜監査レポート（迷子候補・未処理メッセージ）")
lines.append("")
lines.append("生成: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
lines.append("未処理: %s件" % count)
lines.append("")
for it in items:
    head = (it.get("content") or "")[:30].replace("\n", " ")
    lines.append("- id=%s ts=%s : %s" % (it.get("id"), it.get("ts"), head))
open(report_path, "w").write("\n".join(lines) + "\n")
PYEOF
  python3 "$DIR/update_status.py" sns_audit error "未処理${COUNT}件"
fi

echo "[$(TS)] ---- sunday_audit end ----" >> "$LOG"
exit 0
