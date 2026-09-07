#!/usr/bin/env python3
"""市民要望管理台帳 → Todoist 一方向ミラー（2026-09-07）
台帳の未完了案件のうち「次アクション期限」があるものを、Todoist 🏛議員活動 / 🗂台帳フォロー（自動）
セクションに 1案件=1タスク で写す。Todoistの「今日」ビューを唯一の入口にするため。
- 正本は台帳。Todoist側の完了は台帳に書き戻さない（草川が yobo.py update/done で更新）
- 相談者名は写さない（名簿・個人情報は台帳にだけ）
- 台帳の件名/次アクション/期限が変わったら旧タスクを閉じて作り直す。台帳で完了・期限消去なら閉じる
- Todoist側で完了済みなら、台帳が変わるまで再生成しない（同じ写しを何度も蘇らせない）
使い方: python3 yobo_mirror.py [--dry]
"""
import sys, os, json, hashlib, subprocess, datetime
WINDOW_DAYS = 3   # 期限が今日+3日以内（＋期限超過・「相談者に報告」）だけ写す。全件写すとTodoistが台帳の複製になる
sys.path.insert(0, os.path.expanduser("~/.claude/scripts/todoist"))
import td

PROJECT = "6grRHfFfc2WQF46C"          # 🏛 議員活動
SECTION_NAME = "🗂 台帳フォロー（自動）"
STATE = os.path.expanduser("~/.config/yobo/mirror_state.json")
DRY = "--dry" in sys.argv

def ledger():
    out = subprocess.run([sys.executable, os.path.expanduser("~/.claude/scripts/yobo/yobo.py"), "list", "--json"],
                         capture_output=True, text=True).stdout
    rows = json.loads(out[out.index("["):])
    lim = (datetime.date.today()+datetime.timedelta(days=WINDOW_DAYS)).isoformat()
    out=[]
    for r in rows:
        due = str(r.get("次アクション期限","")).strip()[:10]
        if r.get("ステータス")=="完了" or not due: continue
        if due <= lim or r.get("ステータス")=="相談者に報告": out.append(r)
    return out

def section_id():
    cursor=None
    while True:
        d=td.req("GET","/sections",query={"project_id":PROJECT, **({"cursor":cursor} if cursor else {})})
        for s in d.get("results",[]):
            if s["name"]==SECTION_NAME: return s["id"]
        cursor=d.get("next_cursor")
        if not cursor: break
    if DRY: return "DRY"
    return td.req("POST","/sections",body={"name":SECTION_NAME,"project_id":PROJECT})["id"]

def active_mirror_tasks():
    return {t["id"]:t for t in td.all_tasks() if t["project_id"]==PROJECT and t["content"].startswith("KY-")}

def sig(r):
    key = "|".join(str(r.get(k,"")).strip() for k in ("要望内容（件名）","次アクション","次アクション期限","ステータス"))
    return hashlib.md5(key.encode()).hexdigest()[:8]

def build(r):
    no = r["No"]; title = str(r.get("要望内容（件名）","")).strip()
    na = str(r.get("次アクション","")).strip().replace("\n"," ")
    content = f"{no} {title[:28]} ｜ {na[:60]}"
    desc = f"台帳ミラー（正本は市民要望管理台帳）。更新は yobo.py update {no}\n相手先: {r.get('相手先（担当課など）','')} TEL: {r.get('TEL','')}\nステータス: {r.get('ステータス','')}\n次アクション全文: {na}"
    return content, desc, str(r.get("次アクション期限")).strip()[:10]

state = json.load(open(STATE)) if os.path.exists(STATE) else {}
rows = ledger(); sec = section_id(); active = active_mirror_tasks()
seen=set(); made=closed=kept=0
for r in rows:
    no=r["No"]; seen.add(no); h=sig(r); st=state.get(no)
    if st and st["sig"]==h:
        kept+=1; continue                       # 変化なし（Todoist側で完了済みでも蘇らせない）
    if st and st.get("task_id") in active:      # 内容が変わった→旧を閉じる
        if not DRY: td.req("POST", f"/tasks/{st['task_id']}/close")
        closed+=1
    content, desc, due = build(r)
    if DRY: print("  + ", content, due); tid="DRY"
    else: tid = td.req("POST","/tasks",body={"content":content,"description":desc,"project_id":PROJECT,"section_id":sec,"due_date":due})["id"]
    state[no]={"sig":h,"task_id":tid}; made+=1
for no, st in list(state.items()):              # 台帳で完了・期限消去 → 閉じる
    if no not in seen:
        if st.get("task_id") in active:
            if not DRY: td.req("POST", f"/tasks/{st['task_id']}/close")
            closed+=1
        del state[no]
if not DRY: json.dump(state, open(STATE,"w"), ensure_ascii=False, indent=1)
print(f"🗂 台帳ミラー: 対象{len(rows)}件 → 新規{made} / 閉じ{closed} / 据え置き{kept}")
