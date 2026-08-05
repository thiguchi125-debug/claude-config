#!/usr/bin/env python3
"""既存Todoistタスクを一括で作業ブロックに割り付ける（task-add 一括モード）。

**このスクリプトは提案を作るだけで、カレンダーには何も書かない。**
出力した bulk_plan.json を草川に見せ、調整を受けてから初めて登録する。

単発のtask-addと違う点は2つ。

1. **累積割り付け**。1件割り付けるたびにその結果を埋まり時間として次のタスクへ
   反映する。タスクごとに独立して sessions.py を呼ぶと、全タスクが同じ空き枠を
   取り合って同じ時間帯に何十件も重なる。

2. **現実性フィルタ**（task_windows）。空いているかより先に「相手がいる時間か」
   「自分の手番か」を見る。2026-08-06 の初回実行では、空き時間があるという理由
   だけで日曜に市役所照会を8件・18時以降に7件置き、「連絡待ち」のタスクにまで
   ブロックを作ってしまった。カレンダーは埋まるが1件も実行できない。

順序は EDF（期限の早い順・同点なら優先度の高い順）。
"""
import importlib.util
import json
import os
import sys
from datetime import date

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)
import task_windows  # noqa: E402

_spec = importlib.util.spec_from_file_location("s", os.path.join(_DIR, "sessions.py"))
s = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(s)

# 1日に置く作業ブロックの総数上限。平日と休日で分ける。
# 上限を設けないと、空いている日に13件並べるような案が出る（初回実行の実害）。
CAP_WEEKDAY, CAP_WEEKEND = 4, 2


def cap_for(d):
    return CAP_WEEKEND if d.weekday() >= 5 else CAP_WEEKDAY


def main():
    events_path, tasks_path, today_str, now_str, horizon_str = sys.argv[1:6]
    now_minute = int(now_str[:2]) * 60 + int(now_str[3:5])

    days = s.load_days(events_path)
    tasks = json.load(open(tasks_path, encoding="utf-8"))
    withdue = sorted((t for t in tasks if t["due"]),
                     key=lambda t: (t["due"], -t["priority"]))

    used = {}                       # 日付 -> その日に置いたブロック総数
    planned, skipped, overdue, unplaceable = [], [], [], []

    for t in withdue:
        if t["due"] < today_str:
            overdue.append(t)
            continue
        kind, skip = task_windows.classify(t["content"], t.get("labels", ()))
        if skip:
            skipped.append({**t, "skip": skip})
            continue

        rows = s.daily_slots(days, today_str, min(t["due"], horizon_str), now_minute)
        # その日の総ブロック上限に達している日は、このタスクには使わせない
        rows = [(d, 0 if used.get(d.isoformat(), 0) >= cap_for(d) else n, w, f)
                for d, n, w, f in rows]
        total, need = sum(r[1] for r in rows), t["slots"]
        min_days = -(-need // s.MAX_SLOTS_PER_DAY)
        if len(rows) < min_days or total < need:
            verdict = "🚫"
        elif total < need * 1.5:
            verdict = "⚠️"
        else:
            verdict = "✅"

        blocks, unplaced = s.plan_blocks(
            rows, need, 2 if verdict == "✅" else s.MAX_SLOTS_PER_DAY,
            window_fn=task_windows.window_fn(kind))
        for d, st, en in blocks:
            k = d.isoformat()
            days.setdefault(k, {"busy": [], "allday": []})["busy"].append((st, en))
            used[k] = used.get(k, 0) + 1

        row = {**t, "kind": kind.key, "kind_label": kind.label,
               "verdict": verdict, "unplaced": unplaced,
               "blocks": [{"date": d.isoformat(), "start": s.hhmm(st),
                           "end": s.hhmm(en)} for d, st, en in blocks]}
        (planned if blocks else unplaceable).append(row)

    out = {"planned": planned, "skipped": skipped,
           "overdue": overdue, "unplaceable": unplaceable}
    json.dump(out, open(os.path.join(os.getcwd(), "bulk_plan.json"), "w"),
              ensure_ascii=False, indent=1)
    report(out, used)


def report(out, used):
    nb = sum(len(r["blocks"]) for r in out["planned"])
    print("■ 提案ブロック {}件 ／ 対象タスク {}件".format(nb, len(out["planned"])))
    print("■ 除外（相手の手番）: {}件".format(len(out["skipped"])))
    print("■ 期限切れ（割付対象外）: {}件".format(len(out["overdue"])))
    print("■ 置けなかった: {}件".format(len(out["unplaceable"])))
    print("\n※ カレンダーにはまだ何も書いていない。草川の調整を受けてから登録する。")
    print("\n日別:")
    for k in sorted(used):
        d = date.fromisoformat(k)
        print("  {} ({}) {}件 / 上限{}".format(
            k, "月火水木金土日"[d.weekday()], used[k], cap_for(d)))


if __name__ == "__main__":
    main()
