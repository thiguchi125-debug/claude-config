#!/usr/bin/env python3
"""市民要望管理台帳（Googleスプレッドシート）CLI。市役所対応の市民要望はTodoistでなくここへ。
使い方:
  yobo.py list [--status 受付|照会中|回答済・報告前|保留|完了] [--alert] [--q キーワード] [--json]
  yobo.py add --t "件名" [--k 地区] [--r 経路] [--d 詳細] [--s 相談者] [--c 連絡手段] [--b 分類] [--a 相手先] [--l TEL] [--na 次アクション] [--due YYYY-MM-DD] [--link URL]
  yobo.py update KY-012 [--st ステータス] [--memo "回答・進捗メモ"] [--ans YYYY-MM-DD(回答日)] [--asked YYYY-MM-DD(照会日)] [--reported YYYY-MM-DD(相談者へ報告日)] [--na 次アクション] [--due 期限] [--a 相手先] [--l TEL] [--d 詳細]
  yobo.py done KY-012 [--reported today]   # ステータス=完了
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
def main():
    ap = argparse.ArgumentParser(add_help=False); ap.add_argument("cmd"); ap.add_argument("no", nargs="?")
    for k in F: ap.add_argument("--"+k)
    ap.add_argument("--status"); ap.add_argument("--alert", action="store_true"); ap.add_argument("--q"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.cmd == "list":
        res = call({"action":"list","status":a.status or "","only_alert":a.alert,"q":a.q or ""})
        rows = res.get("rows", [])
        if a.json: print(json.dumps(rows, ensure_ascii=False, indent=1)); return
        print(f"{len(rows)}件")
        for o in rows:
            print(f"  {o['No']} {o.get('要対応','')} [{o['ステータス']}] {o['要望内容（件名）'][:40]} → {o.get('相手先（担当課など）','')} / 次:{o.get('次アクション','')[:30]} {('期限'+o['次アクション期限']) if o.get('次アクション期限') else ''} 滞留{o.get('滞留日数','')}日")
        return
    fields = {F[k]: norm_date(v) if k in ("due","ans","asked","reported") else v for k, v in vars(a).items() if k in F and v}
    if a.cmd == "add":
        if "要望内容（件名）" not in fields: sys.exit("--t 件名 は必須")
        res = call({"action":"add","fields":fields})
    elif a.cmd in ("update","done"):
        if not a.no: sys.exit("No（KY-xxx）を指定")
        if a.cmd == "done": fields["ステータス"] = "完了"
        res = call({"action":"update","no":a.no,"fields":fields})
    else: sys.exit(__doc__)
    print(json.dumps(res, ensure_ascii=False))
if __name__ == "__main__": main()
