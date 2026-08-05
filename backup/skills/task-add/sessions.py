#!/usr/bin/env python3
"""確保可能コマ数の算出と実施可能性判定（task-add Step 5-6 の実装）。

カレンダーの予定から「作業に使える30分コマ」を日別に数え、必要コマ数と
突き合わせて ✅可能 / ⚠️タイト / 🚫無理 を判定する。区間のマージ・隙間の
足切り・1日上限を手計算すると間違えるため、必ずこのスクリプトを使う。

使い方:
  python3 sessions.py <events.json> --from 2026-08-03 --due 2026-08-12 --need 8
    events.json = list_events の生JSON（大きい場合は自動保存されたファイルのパス）
    --need      = 必要コマ数（30分=1コマ。想定所要テーブル参照）

設計の正本は同ディレクトリの DESIGN.md。
"""
import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta

BAND_START, BAND_END = 9 * 60, 21 * 60   # 稼働帯 9:00-21:00（全曜日）
SLOT = 30                                # 1コマ = 30分
MAX_SLOTS_PER_DAY = 4                    # 同一タスクには1日最大2セッション = 4コマ
MIN_GAP = 30                             # 30分未満の隙間は使えないものとして捨てる
SESSION_MAX = 60                         # 1ブロック = 最大1セッション = 60分
LUNCH_START, LUNCH_END = 12 * 60, 13 * 60  # 作業ブロックを置かない時間帯（配置専用）

# 終日予定のうち、実際に1日を拘束するとみなす語。
# 草川のカレンダーでは終日予定の大半が「目印」（グラウンドゴルフ・憩いの場等）で
# 実際の拘束は時間指定予定として入っている。終日予定を一律に作業不可日と
# するとほぼ全日が0コマになるため、拘束語を含むものだけを不可日にする。
BLOCKING_ALLDAY = re.compile(r"議会|視察|出張|研修|入院|旅行|終日")
# 【参考】で始まる予定は他人の行事等の参考情報であり、草川を拘束しない
IGNORE_TITLE = re.compile(r"^【参考】")


def load_days(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    days = {}
    for event in data.get("events", []):
        title = event.get("summary") or ""
        if IGNORE_TITLE.search(title):
            continue
        start, end = event.get("start", {}), event.get("end", {})
        if start.get("dateTime"):
            st, et = start["dateTime"], end.get("dateTime", "")
            day = st[:10]
            sm = int(st[11:13]) * 60 + int(st[14:16])
            em = int(et[11:13]) * 60 + int(et[14:16]) if et else sm + 60
            if em < sm:                      # 日跨ぎは当日末で丸める
                em = 24 * 60
            days.setdefault(day, {"busy": [], "allday": []})["busy"].append((sm, em))
        else:
            day = str(start.get("date", ""))[:10]
            if day:
                days.setdefault(day, {"busy": [], "allday": []})["allday"].append(title)
    return days


def slots_for_day(info, from_minute=BAND_START):
    """その日に確保できる30分コマ数・理由・使える空き区間を返す。

    空き区間（[(開始分, 終了分), ...]）まで返すのは、コマ数だけ数えて捨てると
    「いつやるか」をカレンダーに書き戻せないため（作業ブロック生成で使う）。
    """
    if info:
        for title in info.get("allday", []):
            if BLOCKING_ALLDAY.search(title):
                return 0, "終日拘束（{}）".format(title), []
    busy = sorted(info["busy"]) if info else []
    merged = []
    for s, e in busy:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    free, cursor = [], max(BAND_START, from_minute)
    for s, e in merged:
        if s > cursor:
            free.append((cursor, min(s, BAND_END)))
        cursor = max(cursor, e)
        if cursor >= BAND_END:
            break
    if cursor < BAND_END:
        free.append((cursor, BAND_END))
    usable = [(a, b) for a, b in free if b - a >= MIN_GAP]
    slots = sum((b - a) // SLOT for a, b in usable)
    total = sum(b - a for a, b in usable)
    return min(MAX_SLOTS_PER_DAY, slots), "空き{}分".format(total), usable


def daily_slots(days, start, end, now_minute=None):
    """start〜end の各日について (日付, コマ数, 理由, 空き区間) を返す。"""
    out = []
    cur = date.fromisoformat(start)
    last = date.fromisoformat(end)
    while cur <= last:
        key = cur.isoformat()
        from_minute = now_minute if (now_minute and key == start) else BAND_START
        n, why, free = slots_for_day(days.get(key), from_minute)
        out.append((cur, n, why, free))
        cur += timedelta(days=1)
    return out


def latest_start_day(rows, need):
    """その日から最終日までのコマ合計が need 以上になる、最も遅い日。"""
    best = None
    for i in range(len(rows)):
        if sum(r[1] for r in rows[i:]) >= need:
            best = rows[i][0]
    return best


def hhmm(minute):
    return "{:02d}:{:02d}".format(minute // 60, minute % 60)


def split_lunch(free):
    """空き区間から昼(12:00-13:00)を差し引いた区間列を返す（配置専用）。"""
    out = []
    for s, e in free:
        for a, b in ((s, min(e, LUNCH_START)), (max(s, LUNCH_END), e)):
            if b - a >= MIN_GAP:
                out.append((a, b))
    return sorted(out)


def plan_blocks(rows, need, max_per_day):
    """必要コマ数を実際の時間帯（作業ブロック）へ割り付ける。

    1ブロック = 最大1セッション(60分)。1つの空き区間には1ブロックしか置かず、
    日をまたいで散らす。予定の密な日に押し込むより、細く長く進める運用に合う。
    昼(12:00-13:00)は配置対象から外す。コマ数の算出側では昼を除いていないので、
    ここで避けても ✅/⚠️/🚫 の判定は変わらない（配置だけの規則）。
    戻り値: ([(日付, 開始分, 終了分), ...], 割り付けられなかったコマ数)
    """
    plan, left = [], need
    for d, n, _why, free in rows:
        if left <= 0:
            break
        quota = min(n, max_per_day, left)
        placed = 0
        for s, e in split_lunch(free):
            if placed >= quota:
                break
            avail = ((e - s) // SLOT) * SLOT
            take = min(SESSION_MAX, (quota - placed) * SLOT, avail)
            if take < MIN_GAP:
                continue
            plan.append((d, s, s + take))
            placed += take // SLOT
        left -= placed
    return plan, left


def verdict(total, need):
    if total < need:
        return "🚫 無理"
    if total < need * 1.5:
        return "⚠️ タイト"
    return "✅ 可能"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("events")
    ap.add_argument("--from", dest="start", required=True)
    ap.add_argument("--due", required=True)
    ap.add_argument("--need", type=int, required=True, help="必要コマ数（30分=1コマ）")
    ap.add_argument("--horizon", default=None,
                    help="代替案を探す上限日（既定=期限+14日）")
    ap.add_argument("--now", default=None, help="当日の開始時刻 HH:MM（既定=9:00）")
    ap.add_argument("--plan", action="store_true",
                    help="作業ブロック案（日付＋時間帯）も出力する")
    ap.add_argument("--plan-json", default=None,
                    help="作業ブロック案をJSONで書き出すパス（カレンダー登録用）")
    ap.add_argument("--plan-title", default="作業",
                    help="--plan-json に入れる予定タイトル（既定=作業）")
    args = ap.parse_args()

    now_minute = None
    if args.now:
        h, m = args.now.split(":")
        now_minute = int(h) * 60 + int(m)

    horizon = args.horizon or (
        date.fromisoformat(args.due) + timedelta(days=14)).isoformat()
    days = load_days(args.events)
    rows = daily_slots(days, args.start, horizon, now_minute)

    due = date.fromisoformat(args.due)
    upto = [r for r in rows if r[0] <= due]
    total = sum(r[1] for r in upto)
    min_days = -(-args.need // MAX_SLOTS_PER_DAY)   # 切り上げ
    remaining_days = len(upto)

    for d, n, why, _free in upto:
        print("{} ({}) {}コマ  {}".format(
            d.isoformat(), "月火水木金土日"[d.weekday()], n, why))
    print("---")
    print("必要 {}コマ（{}時間・最低{}日） / 期限までの確保 {}コマ / 残り {}日".format(
        args.need, args.need / 2, min_days, total, remaining_days))

    feasible = remaining_days >= min_days and total >= args.need
    if remaining_days < min_days:
        print("判定: 🚫 無理（最低所要{}日 > 残り{}日・空き状況を見るまでもない）".format(
            min_days, remaining_days))
        v = "🚫 無理"
    else:
        v = verdict(total, args.need)
        print("判定: {}".format(v))
        if not v.startswith("🚫"):
            start_by = latest_start_day(upto, args.need)
            if start_by:
                print("着手推奨日: {}".format(start_by.isoformat()))

    if args.plan or args.plan_json:
        # 余裕がある（✅）ときは1日1セッションに抑えて散らす。逼迫時のみ1日2セッション。
        max_per_day = 2 if v.startswith("✅") else MAX_SLOTS_PER_DAY
        blocks, unplaced = plan_blocks(upto, args.need, max_per_day)
        if args.plan:
            print("--- 作業ブロック案（1ブロック最大60分・1日最大{}コマ）".format(max_per_day))
            for d, s, e in blocks:
                print("{} ({}) {}-{}".format(
                    d.isoformat(), "月火水木金土日"[d.weekday()], hhmm(s), hhmm(e)))
            if unplaced:
                print("⚠️ 未割付 {}コマ（期限までに置き切れない）".format(unplaced))
        if args.plan_json:
            with open(args.plan_json, "w", encoding="utf-8") as f:
                json.dump({
                    "title": args.plan_title,
                    "due": args.due,
                    "need_slots": args.need,
                    "verdict": v,
                    "unplaced_slots": unplaced,
                    "blocks": [{"date": d.isoformat(),
                                "start": hhmm(s), "end": hhmm(e),
                                "minutes": e - s} for d, s, e in blocks],
                }, f, ensure_ascii=False, indent=2)
            print("作業ブロック案を書き出しました: {}".format(args.plan_json))

    if not feasible:
        cum, plan_a, plan_b = 0, None, None
        for i, (d, n, _why, _free) in enumerate(rows):
            cum += n
            if plan_a is None and cum >= args.need and (i + 1) >= min_days:
                plan_a = (d, cum)
            if plan_b is None and cum >= args.need * 1.5 and (i + 1) >= min_days:
                plan_b = (d, cum)
                break
        if plan_a:
            print("代替案 a) {} （累計{}コマ）".format(plan_a[0].isoformat(), plan_a[1]))
        if plan_b:
            print("代替案 b) {} （累計{}コマ）●推奨".format(
                plan_b[0].isoformat(), plan_b[1]))


if __name__ == "__main__":
    main()
