#!/usr/bin/env python3
"""
Todoist ヘルパー（草川たくや タスク管理一本化・2026-06-14〜）
APIは必ず /api/v1/。token は ~/.config/todoist/token。

使い方:
  td.py morning            朝の3ブロック（期限超過/本日/今週中）＋監査シグナル
  td.py today              本日期限のみ
  td.py overdue            期限超過のみ
  td.py week               今週中（明日〜+7日）
  td.py nodue              期限なし（inbox的）
  td.py audit              監査シグナル件数のみ
  td.py list [PROJECT]     全アクティブ（任意でプロジェクト名フィルタ）
  td.py projects           プロジェクト一覧
  td.py add "内容" [--due "2026-07-01" or "today"/"tomorrow"/"明日"] \
                    [--project 議員活動] [--priority 1-4(4最高)] [--label 結果待ち] [--desc "メモ"]
  td.py done <task_id>     完了
  td.py rm <task_id>       削除
出力はトークン節約のため簡潔。JSONが欲しい時は末尾に --json。
"""
import sys, os, json, urllib.request, urllib.parse, datetime

API = "https://api.todoist.com/api/v1"
TOKEN = open(os.path.expanduser("~/.config/todoist/token")).read().strip()

def req(method, path, body=None, query=None):
    url = API + path
    if query:
        url += "?" + urllib.parse.urlencode(query)
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Authorization", "Bearer " + TOKEN)
    if data:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        print(f"[APIエラー {e.code}] {e.read().decode()[:200]}", file=sys.stderr)
        sys.exit(1)

def all_tasks():
    out, cursor = [], None
    while True:
        q = {"cursor": cursor} if cursor else None
        d = req("GET", "/tasks", query=q)
        out += d.get("results", [])
        cursor = d.get("next_cursor")
        if not cursor:
            break
    return out

def projects_map():
    out, cursor = {}, None
    while True:
        q = {"cursor": cursor} if cursor else None
        d = req("GET", "/projects", query=q)
        for p in d.get("results", []):
            out[p["id"]] = p["name"]
        cursor = d.get("next_cursor")
        if not cursor:
            break
    return out

def resolve_project(name):
    d = req("GET", "/projects")
    for p in d.get("results", []):
        if name in p["name"]:
            return p["id"]
    return None

def due_date(t):
    due = t.get("due")
    if not due:
        return None
    s = due.get("date", "")
    return s[:10] if s else None

WD = "月火水木金土日"


def due_label(t):
    """08/13(木) 形式。複数日にまたがる一覧で「いつの分か」を出すために使う。"""
    d = due_date(t)
    if not d:
        return "  --/--   "
    try:
        dd = datetime.date.fromisoformat(d)
    except ValueError:
        return "  --/--   "
    return f"{dd.month:02d}/{dd.day:02d}({WD[dd.weekday()]}) "


def fmt(t, pm, show_proj=True, show_due=False):
    pr = 5 - t.get("priority", 1)           # API4=P1
    flag = f"P{pr}" if pr <= 2 else ""
    labels = "".join(" @" + l for l in t.get("labels", []))
    proj = f" 〔{pm.get(t['project_id'],'?')}〕" if show_proj else ""
    # 週ビューのように複数日が混ざる一覧でだけ日付を出す（今日ビューには不要）
    day = due_label(t) if show_due else ""
    head = (flag + " ") if flag else ""
    return f"  {day}{head}{t['content'][:46]}{labels}{proj}"

# 期限が無いのが正常な置き場。ここの塩漬けを監査シグナルに数えると
# 毎朝「期限なし⚠️」が鳴り続けて本物の盲点が埋もれる（2026-08-04 棚卸しで判明）
NODUE_PARKED_PROJECTS = ("🗂 構想バックログ",)

# 実行窓ラベルごとの「その日もう間に合わない時刻」。task_windows.py の Kind と揃える。
WINDOW_END = {"役所": 17 * 60, "現地": 18 * 60, "夜電話": 20 * 60, "机上": 21 * 60}


def turn_split(sel):
    """今日の一覧を「自分の手番 / 催促する / 保留」に割る。

    Todoistの期限は1種類しかないので、@結果待ちに持たせた「催促日」と
    自分の実作業が同じ列に並ぶ。2026-08-10 の一覧は9件中6件が相手のボール、
    残り3件も前提未達か動詞なしで、実際に今日やる想定のものが無かった。
    毎朝「今日やれないこと」を見せられると一覧そのものが信用されなくなる。
    """
    own, waiting, hold = [], [], []
    for t in sel:
        labels = t.get("labels", [])
        if "結果待ち" in labels:
            waiting.append(t)
        elif "保留" in labels:
            hold.append(t)
        else:
            own.append(t)
    return own, waiting, hold


def window_closed(t, now_minute):
    """その実行窓が今日はもう閉じているか（役所は17時、夜電話は20時など）。"""
    ends = [WINDOW_END[l] for l in t.get("labels", []) if l in WINDOW_END]
    return bool(ends) and now_minute > max(ends)


def print_today(pm, td_):
    now = datetime.datetime.now()
    now_minute = now.hour * 60 + now.minute
    own, waiting, hold = turn_split(td_)
    live = [t for t in own if not window_closed(t, now_minute)]
    closed = [t for t in own if window_closed(t, now_minute)]

    print(f"\n📍 今日やる・自分の手番（{len(live)}件）")
    print("\n".join(fmt(t, pm) for t in live) if live else "  なし")
    if closed:
        print(f"\n⏰ 今日は窓が閉じた（{len(closed)}件・明日以降へ）")
        print("\n".join(fmt(t, pm) for t in closed))
    if waiting:
        print(f"\n📮 催促する・相手のボール（{len(waiting)}件）")
        print("\n".join(fmt(t, pm) for t in waiting))
    if hold:
        print(f"\n⏸ 保留（{len(hold)}件）")
        print("\n".join(fmt(t, pm) for t in hold))


def print_overdue(pm, ov):
    """期限超過も手番／催促／保留に割る（2026-08-11 草川指示）。

    @結果待ちは相手が動くまで自分にできることが無いので、期限が過ぎても
    それは「サボり」ではなく「催促すべき日が来た」でしかない。同じ列に混ぜると
    超過件数が実態を指さなくなる（8/10に61→0にしたのに翌朝また9件のうち
    5件が相手待ちで埋まった）。⚠️は自分の手番だけを数える。
    """
    own, waiting, hold = turn_split(ov)
    print(f"\n⚠️ 期限超過・自分の手番（{len(own)}件）")
    print("\n".join(fmt(t, pm, show_due=True) for t in own) if own else "  なし")
    if waiting:
        print(f"\n📮 催促日が過ぎた・相手のボール（{len(waiting)}件）")
        print("\n".join(fmt(t, pm, show_due=True) for t in waiting))
    if hold:
        print(f"\n⏸ 保留のまま期限が過ぎた（{len(hold)}件）")
        print("\n".join(fmt(t, pm, show_due=True) for t in hold))


def print_week(pm, wk):
    """今週中も今日と同じ割り方で出す（2026-08-10 草川指示）。

    窓が閉じたかの判定は入れない。未来日はまだどの窓も開いているため。
    代わりに日付を出す。7日分が混ざるので、日付が無いと山の位置が読めない。
    """
    own, waiting, hold = turn_split(wk)
    print(f"\n🗓 今週中・自分の手番（{len(own)}件）")
    print("\n".join(fmt(t, pm, show_due=True) for t in own) if own else "  なし")
    if waiting:
        print(f"\n📮 今週中・催促する（{len(waiting)}件）")
        print("\n".join(fmt(t, pm, show_due=True) for t in waiting))
    if hold:
        print(f"\n⏸ 今週中・保留（{len(hold)}件）")
        print("\n".join(fmt(t, pm, show_due=True) for t in hold))


def buckets():
    today = datetime.date.today()
    tasks = all_tasks()
    pm = projects_map()
    ov, td_, wk, nod = [], [], [], []
    for t in tasks:
        d = due_date(t)
        if d is None:
            if pm.get(t["project_id"], "") not in NODUE_PARKED_PROJECTS:
                nod.append(t)
            continue
        try:
            dd = datetime.date.fromisoformat(d)
        except ValueError:
            nod.append(t); continue
        if dd < today:
            ov.append(t)
        elif dd == today:
            td_.append(t)
        elif dd <= today + datetime.timedelta(days=7):
            wk.append(t)
    for L in (ov, td_, wk):
        L.sort(key=lambda x: (due_date(x) or "", -x.get("priority", 1)))
    return pm, ov, td_, wk, nod, tasks

def cmd_morning():
    pm, ov, td_, wk, nod, tasks = buckets()
    print("✅ 今日のタスク（Todoist）")
    print_overdue(pm, ov)
    print_today(pm, td_)
    print(f"\n──── 明日〜+7日（{len(wk)}件）────")
    print_week(pm, wk)
    # 監査シグナル
    stale = [t for t in nod]
    print("\n🧹 監査シグナル")
    print(f"  ├ 期限なしタスク: {len(nod)}件 " + ("⚠️" if len(nod) > 5 else "✅"))
    waiting = [t for t in tasks if "結果待ち" in t.get("labels", [])]
    hold = [t for t in tasks if "保留" in t.get("labels", [])]
    print(f"  ├ @結果待ち: {len(waiting)}件")
    print(f"  └ @保留: {len(hold)}件")
    if len(nod) > 5:
        print('\n  👉 「タスク棚卸し」で期限なしタスクを整理推奨')

def cmd_simple(which):
    pm, ov, td_, wk, nod, tasks = buckets()
    if which == "today":          # 今日・今週は手番・催促・保留に分けて出す
        print(f"本日期限（{len(td_)}件）")
        print_today(pm, td_)
        return
    if which == "week":
        print(f"今週中（{len(wk)}件）")
        print_week(pm, wk)
        return
    if which == "overdue":
        print(f"期限超過（{len(ov)}件）")
        print_overdue(pm, ov)
        return
    print(f"期限なし（{len(nod)}件）")
    print("\n".join(fmt(t, pm) for t in nod) if nod else "  なし")

def cmd_audit():
    pm, ov, td_, wk, nod, tasks = buckets()
    waiting = [t for t in tasks if "結果待ち" in t.get("labels", [])]
    hold = [t for t in tasks if "保留" in t.get("labels", [])]
    ov_own, ov_wait, _ = turn_split(ov)
    # 滞留日数は added_at 基準。60日超は「登録して以来一度も判断していない」の意。
    today = datetime.date.today()
    def age(t):
        try: return (today - datetime.date.fromisoformat(t.get("added_at","")[:10])).days
        except ValueError: return 0
    stale_wait = [t for t in waiting if age(t) >= 60]
    print("🧹 タスク監査シグナル（Todoist）")
    print(f"  ├ 期限超過（自分の手番）: {len(ov_own)}件")
    print(f"  ├ 催促日超過（相手のボール）: {len(ov_wait)}件")
    print(f"  ├ 期限なし: {len(nod)}件 " + ("⚠️" if len(nod) > 5 else "✅"))
    print(f"  ├ @結果待ち: {len(waiting)}件（うち滞留60日超 {len(stale_wait)}件"
          + ("⚠️" if stale_wait else "") + "）")
    print(f"  └ @保留: {len(hold)}件")
    if stale_wait:
        print('\n  👉 「タスク棚卸し」で滞留@結果待ちの撤退ライン確認を推奨')

def cmd_list(args):
    pm = projects_map()
    tasks = all_tasks()
    if args:
        tasks = [t for t in tasks if args[0] in pm.get(t["project_id"], "")]
    tasks.sort(key=lambda x: (due_date(x) or "9999", -x.get("priority",1)))
    print(f"アクティブ {len(tasks)}件")
    print("\n".join(fmt(t, pm) + f"  #{t['id']}" for t in tasks) if tasks else "  なし")

def cmd_projects():
    d = req("GET", "/projects")
    for p in d.get("results", []):
        print(f"  {p['name']}  #{p['id']}")

def cmd_add(args):
    # parse
    content = args[0]
    opts = {"content": content}
    desc = None; proj = None
    i = 1
    while i < len(args):
        a = args[i]
        if a == "--due": opts["due_string"] = args[i+1]; i += 2
        elif a == "--priority": opts["priority"] = int(args[i+1]); i += 2
        elif a == "--label": opts.setdefault("labels", []).append(args[i+1]); i += 2
        elif a == "--desc": opts["description"] = args[i+1]; i += 2
        elif a == "--project": proj = args[i+1]; i += 2
        else: i += 1
    if proj:
        pid = resolve_project(proj)
        if pid: opts["project_id"] = pid
        else: print(f"[警告] プロジェクト '{proj}' 不明→Inboxへ", file=sys.stderr)
    d = req("POST", "/tasks", body=opts)
    print(f"✅ 追加: {d.get('content','?')[:46]} | 期限{(d.get('due') or {}).get('date','—')} | #{d.get('id')}")

def cmd_done(tid):
    req("POST", f"/tasks/{tid}/close")
    print(f"✅ 完了: #{tid}")

def cmd_rm(tid):
    req("DELETE", f"/tasks/{tid}")
    print(f"🗑 削除: #{tid}")

def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return
    c = a[0]
    if c == "morning": cmd_morning()
    elif c in ("today","overdue","week","nodue"): cmd_simple(c)
    elif c == "audit": cmd_audit()
    elif c == "list": cmd_list(a[1:])
    elif c == "projects": cmd_projects()
    elif c == "add": cmd_add(a[1:])
    elif c == "done": cmd_done(a[1])
    elif c == "rm": cmd_rm(a[1])
    else: print(__doc__)

if __name__ == "__main__":
    main()
