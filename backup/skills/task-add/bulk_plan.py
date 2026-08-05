#!/usr/bin/env python3
"""既存Todoistタスクを一括で作業ブロックに割り付ける（task-add 一括モード）。

単発のtask-addと決定的に違うのは、**1件割り付けるたびにその結果を埋まり時間として
次のタスクに反映する**こと。タスクごとに独立して sessions.py を呼ぶと、全タスクが
同じ空き枠を取り合って同じ時間帯に何十件も重なる。

順序は EDF（期限の早い順・同点なら優先度の高い順）。
"""
import importlib.util
import json
import os
import sys
from datetime import date, timedelta

spec = importlib.util.spec_from_file_location(
    "s", os.path.expanduser("~/.claude/skills/task-add/sessions.py"))
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)

events_path, tasks_path, today_str, now_str, horizon_str = sys.argv[1:6]
today = date.fromisoformat(today_str)
now_minute = int(now_str[:2]) * 60 + int(now_str[3:5])

days = s.load_days(events_path)
tasks = json.load(open(tasks_path, encoding="utf-8"))
withdue = sorted((t for t in tasks if t["due"]),
                 key=lambda t: (t["due"], -t["priority"]))

results, overdue = [], []
for t in withdue:
    if t["due"] < today_str:
        overdue.append(t)
        continue
    due = min(t["due"], horizon_str)          # 窓の外は評価しない
    rows = s.daily_slots(days, today_str, due, now_minute)
    total = sum(r[1] for r in rows)
    need = t["slots"]
    min_days = -(-need // s.MAX_SLOTS_PER_DAY)
    if len(rows) < min_days or total < need:
        verdict = "🚫"
    elif total < need * 1.5:
        verdict = "⚠️"
    else:
        verdict = "✅"
    blocks, unplaced = s.plan_blocks(
        rows, need, 2 if verdict == "✅" else s.MAX_SLOTS_PER_DAY)
    # 割り付けた分を埋まり時間として days に反映（次のタスクが同じ枠を取らない）
    for d, st, en in blocks:
        days.setdefault(d.isoformat(), {"busy": [], "allday": []})["busy"].append((st, en))
    results.append({**t, "verdict": verdict, "blocks": [
        {"date": d.isoformat(), "start": s.hhmm(st), "end": s.hhmm(en)}
        for d, st, en in blocks], "unplaced": unplaced})

json.dump({"results": results, "overdue": overdue},
          open("bulk_plan.json", "w"), ensure_ascii=False, indent=1)

full = [r for r in results if not r["unplaced"]]
part = [r for r in results if r["unplaced"] and r["blocks"]]
none = [r for r in results if not r["blocks"]]
nblocks = sum(len(r["blocks"]) for r in results)
print("■ 期限切れ（今日より前・割付対象外）: {}件".format(len(overdue)))
print("■ 割付できた: {}件（作業ブロック {}件 = {}時間）".format(
    len(full), nblocks, sum(len(r["blocks"]) for r in full) * 1.0))
print("■ 一部だけ割付: {}件".format(len(part)))
print("■ まったく置けない: {}件".format(len(none)))
print("■ ブロック総数: {}件".format(nblocks))
print()
cnt = {}
for r in results:
    for b in r["blocks"]:
        cnt[b["date"]] = cnt.get(b["date"], 0) + 1
print("日別ブロック数:")
for k in sorted(cnt):
    print("  {} {}件".format(k, cnt[k]))
