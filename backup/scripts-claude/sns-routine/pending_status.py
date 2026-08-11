#!/usr/bin/env python3
"""
_pending_tasks.jsonl の未決・退避行を毎朝あぶり出す。

なぜ要るか（2026-08-11に発覚した事故）:
  夜間triageはタスクを登録せず提案だけしてDiscordへ投げ、「①OK」の返信を待つ。
  返信が2晩無いと retire_no_reply で📥未分類インテークへ退避する。
  この導線は緊急度を一切見ないので、最重要案件ほど静かに消える。
  実際、育休退園の市民相談（相談者は8/7から返信待ち・9月復園が懸かる）が
  8/10・8/11の無応答だけを理由に退避キューへ入り、
  さらに content_safety_gate に阻まれて退避先にも書けず宙に浮いていた。
  同じ経路で「みずきが丘の信号の注意喚起」（交通安全）も8/5に消えている。

  📮投げ込み台帳の「保存先」欄に "Todoist提案中" と書いてはいたが、
  それを毎朝読む者がいなかった。＝締めが人間の記憶に依存していた。
  このスクリプトが読む係になる。

使い方:
  python3 ~/.claude/scripts/sns-routine/pending_status.py          # 人が読む形で出力
  python3 ~/.claude/scripts/sns-routine/pending_status.py --json   # _pending_status.json も更新

ohayo §1 から呼ばれる。出力が空（滞留ゼロ）なら "clean" とだけ返す。
"""
import json
import os
import sys
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PENDING = os.path.join(HERE, "_pending_tasks.jsonl")
QUEUE = os.path.join(HERE, "_notion_queue.jsonl")
OUT = os.path.join(HERE, "_pending_status.json")

# 決着済み＝もう朝に出さなくてよい状態
SETTLED = {
    "registered",
    "registered_no_due",
    "resolved_already_registered",
    "dropped_by_user",
}
# 「返事が無いから捨てた」系。捨てた事実そのものを朝に出す（復活の機会を作る）
RETIRED = {"retired_no_reply", "retire_queued"}


def _age(d):
    try:
        return (date.today() - datetime.strptime(d, "%Y-%m-%d").date()).days
    except Exception:
        return None


def _rows(path):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def collect():
    waiting, retired = [], []
    for r in _rows(PENDING):
        st = r.get("status", "proposed")
        if st in SETTLED:
            continue
        item = {
            "id": r.get("id"),
            "label": r.get("label", ""),
            "content": r.get("content", ""),
            "project": r.get("project", ""),
            "due_proposed": r.get("due"),
            "priority": r.get("priority", ""),
            "age_days": _age(r.get("proposed_date", "")),
            "status": st,
        }
        (retired if st in RETIRED else waiting).append(item)

    # Notion書込に失敗して宙に浮いている分（退避先にすら書けなかったもの）
    stuck = []
    for r in _rows(QUEUE):
        stuck.append({"dest": r.get("dest") or r.get("type", "?"),
                      "title": (r.get("title") or r.get("content") or "")[:60]})

    waiting.sort(key=lambda x: -(x["age_days"] or 0))
    retired.sort(key=lambda x: -(x["age_days"] or 0))
    return waiting, retired, stuck


def render(waiting, retired, stuck):
    lines = []
    if waiting:
        lines.append(f"📋 Todoist提案の滞留 {len(waiting)}件（返信待ち＝まだ誰の手番でもない）")
        for w in waiting:
            age = w["age_days"]
            mark = "🚨" if (age is not None and age >= 2) else "・"
            age_s = f"{age}日経過" if age is not None else "経過日数不明"
            due = f"・期限案{w['due_proposed']}" if w.get("due_proposed") else ""
            lines.append(f"  {mark} {age_s} {w['label']}{w['content'][:52]}"
                         f"（{w['project']}{due}）")
    if retired:
        lines.append(f"🗑 無応答で退避された分 {len(retired)}件（内容を見て復活させるか判断）")
        for r in retired:
            age = r["age_days"]
            age_s = f"{age}日前の提案" if age is not None else ""
            lines.append(f"  ・{age_s} {r['content'][:52]}（{r['project']}）")
    if stuck:
        lines.append(f"📦 Notion書込待ちキュー {len(stuck)}件（_notion_queue.jsonl・flush要）")
        for s in stuck[:5]:
            lines.append(f"  ・{s['dest']}: {s['title']}")
    if not lines:
        return "clean"
    lines.append("→ 「①OK」「①は期限来週で」「②不要」で処理。"
                 "期限を付けるものは task-add（カレンダー突合）を通します。")
    return "\n".join(lines)


def main():
    waiting, retired, stuck = collect()
    text = render(waiting, retired, stuck)
    if "--json" in sys.argv:
        json.dump({
            "updated": datetime.now().isoformat(timespec="seconds"),
            "waiting": waiting,
            "retired": retired,
            "queue_stuck": stuck,
            "text": text,
        }, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
