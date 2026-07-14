#!/usr/bin/env python3
"""_pipeline_status.json に discord_intake 等の状態をマージ（既存キー保持）"""
import datetime, json, os, sys

PATH = os.environ.get("PIPELINE_STATUS_PATH") or os.path.expanduser(
    "~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_pipeline_status.json")

key, status, msg = sys.argv[1], sys.argv[2], sys.argv[3]
data = {}
if os.path.exists(PATH):
    with open(PATH) as f:
        data = json.load(f)
data[key] = {
    "status": status,
    "message": msg,
    "updated": datetime.datetime.now().isoformat(timespec="seconds"),
}
tmp = PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
os.replace(tmp, PATH)
