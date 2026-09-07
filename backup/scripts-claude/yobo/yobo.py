#!/usr/bin/env python3
"""市民要望管理台帳（Googleスプレッドシート）CLI。市役所対応の市民要望はTodoistでなくここへ。
使い方:
  yobo.py list [--status これから聞く|返事待ち|相談者に報告|様子見|完了] [--alert] [--q キーワード] [--json]
  yobo.py add --t "件名" [--k 地区] [--r 経路] [--d 詳細] [--s 相談者] [--c 連絡手段] [--b 分類] [--a 相手先] [--l TEL] [--na 次アクション] [--due YYYY-MM-DD] [--link URL]
  yobo.py update KY-012 [--st ステータス] [--memo "回答・進捗メモ"] [--ans YYYY-MM-DD(回答日)] [--asked YYYY-MM-DD(照会日)] [--reported YYYY-MM-DD(相談者へ報告日)] [--na 次アクション] [--due 期限] [--a 相手先] [--l TEL] [--d 詳細]
  yobo.py done KY-012 [--reported today]   # ステータス=完了
  yobo.py alert                            # ohayo用：⚠要対応だけをステータス別に圧縮表示（0件なら1行）
  yobo.py flush                            # _pending.jsonl に退避した add を再投入
設定: ~/.config/yobo/config.json = {"url": "<Apps Script exec URL>", "token": "<合言葉>"}（手順書 ~/outputs/yobo-sheet/SETUP_AppsScript.md）
"""
import sys, os, json, argparse, urllib.request, datetime
CFG = os.path.expanduser("~/.config/yobo/config.json")
def cfg():
    if not os.path.exists(CFG):
        sys.exit("未設定: Apps Script が未デプロイです。手順書 ~/outputs/yobo-sheet/SETUP_AppsScript.md を草川に案内し、URLと合言葉を受け取って ~/.config/yobo/config.json に保存してください。")
    return json.load(open(CFG))
PENDING = os.path.expanduser("~/outputs/yobo-sheet/_pending.jsonl")
def call(body):
    c = cfg(); body["token"] = c["token"]
    if not c.get("url"):
        if body.get("action") == "add":
            body["queued_at"] = datetime.datetime.now().isoformat(timespec="seconds")
            with open(PENDING, "a") as f: f.write(json.dumps({k:v for k,v in body.items() if k!="token"}, ensure_ascii=False)+"\n")
            print(f"未設定: Apps Script のURLが空です。この案件は {PENDING} に退避しました（デプロイ後に再投入）。")
        sys.exit("手順書 ~/outputs/yobo-sheet/SETUP_AppsScript.md に従い、URLと合言葉を ~/.config/yobo/config.json に保存してください。")
    req = urllib.request.Request(c["url"], data=json.dumps(body, ensure_ascii=False).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read().decode())
F = {"t":"要望内容（件名）","k":"地区","r":"経路","d":"詳細・経緯","s":"相談者","c":"連絡手段","b":"分類","a":"相手先（担当課など）","l":"TEL",
     "na":"次アクション","due":"次アクション期限","link":"関連リンク","st":"ステータス","memo":"回答・進捗メモ","ans":"回答日","asked":"照会日","reported":"相談者へ報告日"}
def norm_date(v): return datetime.date.today().isoformat() if v=="today" else v
def _d(v):
    try: return datetime.date.fromisoformat(str(v)[:10])
    except Exception: return None
def stay_days(o):
    """滞留日数＝今日−直近の動き（受付日・照会日・回答日・最終更新の最大）。シートT列が日付書式で返る不具合の回避（完了は空）。"""
    v = str(o.get("滞留日数",""))
    if v.isdigit(): return int(v)
    if o.get("ステータス")=="完了": return ""
    ds = [d for d in (_d(o.get(k)) for k in ("受付日","照会日","回答日","最終更新")) if d]
    return (datetime.date.today()-max(ds)).days if ds else ""
def print_rows(rows):
    for o in rows:
        print(f"  {o['No']} {o.get('要対応','')} [{o['ステータス']}] {o['要望内容（件名）'][:40]} → {o.get('相手先（担当課など）','')} / 次:{o.get('次アクション','')[:30]} {('期限'+o['次アクション期限']) if o.get('次アクション期限') else ''} 滞留{stay_days(o)}日")
def main():
    ap = argparse.ArgumentParser(add_help=False); ap.add_argument("cmd"); ap.add_argument("no", nargs="?")
    for k in F: ap.add_argument("--"+k)
    ap.add_argument("--status"); ap.add_argument("--alert", action="store_true"); ap.add_argument("--q"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.cmd == "list":
        res = call({"action":"list","status":a.status or "","only_alert":a.alert,"q":a.q or ""})
        rows = res.get("rows", [])
        if a.json: print(json.dumps(rows, ensure_ascii=False, indent=1)); return
        print(f"{len(rows)}件"); print_rows(rows); return
    if a.cmd == "alert":
        rows = call({"action":"list","only_alert":True})["rows"]
        if not rows: print("🗂 市民要望台帳: ⚠要対応なし"); return
        today = datetime.date.today()
        def over(o):
            d=_d(o.get("次アクション期限")); return d and d<today
        buckets = [("相談者に報告（答えは来ている）", [o for o in rows if o["ステータス"]=="相談者に報告"]),
                   ("期限超過", [o for o in rows if o["ステータス"]!="相談者に報告" and over(o)]),
                   ("滞留14日以上（期限内）", [o for o in rows if o["ステータス"]!="相談者に報告" and not over(o)])]
        print(f"🗂 市民要望台帳: ⚠要対応 {len(rows)}件（" + "／".join(f"{n}{len(b)}" for n,b in buckets if b) + "）")
        for n,b in buckets:
            if not b: continue
            print(f"  ■{n}")
            for o in sorted(b, key=lambda o:(o.get("次アクション期限") or "9999", o["No"])):
                due = f" 期限{o['次アクション期限'][5:]}" if o.get("次アクション期限") else ""
                print(f"    {o['No']} {o['要望内容（件名）'][:28]} → {o.get('相手先（担当課など）','')[:14]} / {o.get('次アクション','')[:24]}{due} 滞留{stay_days(o)}日")
        print("  → 進捗があれば `yobo.py update KY-xxx --st 返事待ち --asked today` ／相談者へ報告したら `--reported today`")
        return
    if a.cmd == "flush":
        if not os.path.exists(PENDING): print("退避キューなし"); return
        lines=[l for l in open(PENDING).read().splitlines() if l.strip()]
        if not lines: print("退避キューなし"); return
        done=[]
        for l in lines:
            body=json.loads(l); res=call({"action":"add","fields":body["fields"]})
            print(json.dumps(res, ensure_ascii=False)); 
            if res.get("ok"): done.append(l)
        rest=[l for l in lines if l not in done]
        open(PENDING,"w").write("\n".join(rest)+("\n" if rest else ""))
        print(f"再投入 {len(done)}件／残 {len(rest)}件"); return
    fields = {F[k]: norm_date(v) if k in ("due","ans","asked","reported") else v for k, v in vars(a).items() if k in F and v}
    if a.cmd == "add":
        if "要望内容（件名）" not in fields: sys.exit("--t 件名 は必須")
        fields.setdefault("ステータス", "これから聞く")
        res = call({"action":"add","fields":fields})
    elif a.cmd in ("update","done"):
        if not a.no: sys.exit("No（KY-xxx）を指定")
        if a.cmd == "done": fields["ステータス"] = "完了"
        res = call({"action":"update","no":a.no,"fields":fields})
    else: sys.exit(__doc__)
    print(json.dumps(res, ensure_ascii=False))
    # 2026-09-07: 台帳→Todoistミラー（Todoist「今日」を唯一の入口にする）。失敗しても台帳の書込は成立済み
    try:
        if os.environ.get("YOBO_NO_MIRROR"): return
        import subprocess; subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "yobo_mirror.py")], timeout=60)
    except Exception as e: print("（ミラー未実行: %s）" % e)
if __name__ == "__main__": main()
