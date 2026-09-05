#!/usr/bin/env python3
"""SubagentStop: ファクトチェック系サブエージェントの最終報告から
「### Cn: ✅ 「主張」」「### Cn: ❌ 「主張」」ブロックを拾い、検証済み台帳
~/.claude/agents/knowledge/fact_ledger/verified_facts.tsv へ自動追記する。

2026-09-05 新設。agent が「検証後に台帳へ書く」指示を守るかどうかに依存させず、
成果物（報告）から機械的に学習を回収する。失敗しても絶対にエラーで止めない（exit 0）。
対象: content-fact-checker / content-gate-lite の出力形式。他agentの報告は形式が
合わなければ何も拾わないので副作用なし。
"""
import json, os, re, sys, datetime

LEDGER = os.path.expanduser("~/.claude/agents/knowledge/fact_ledger/verified_facts.tsv")
LOG = os.path.expanduser("~/.claude/agents/knowledge/fact_ledger/_autolog.log")
HEAD = re.compile(r"^###\s*C?\d*[:：]?\s*(✅|❌)\s*「([^」]{3,200})」", re.M)
URL = re.compile(r"https?://[^\s)>」]+")


def last_assistant_text(path):
    text = ""
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                try:
                    o = json.loads(line)
                except ValueError:
                    continue
                if o.get("type") != "assistant":
                    continue
                m = o.get("message") or {}
                parts = [b.get("text", "") for b in (m.get("content") or [])
                         if isinstance(b, dict) and b.get("type") == "text"]
                if parts:
                    text = "\n".join(parts)
    except OSError:
        return ""
    return text


def existing_claims():
    s = set()
    try:
        with open(LEDGER, encoding="utf-8") as f:
            next(f, None)
            for line in f:
                c = line.split("\t")
                if len(c) >= 3:
                    s.add(c[2].strip())
    except OSError:
        pass
    return s


def main():
    try:
        inp = json.load(sys.stdin)
    except ValueError:
        return
    tpath = inp.get("transcript_path") or ""
    if not tpath or not os.path.exists(tpath):
        return
    text = last_assistant_text(tpath)
    if "✅" not in text and "❌" not in text:
        return
    heads = list(HEAD.finditer(text))
    if not heads:
        return
    theme = ""
    mt = re.search(r"(?:テーマ|theme)[:：]\s*([^\n]{1,40})", text)
    if mt:
        theme = mt.group(1).strip()
    known = existing_claims()
    today = datetime.date.today().isoformat()
    rows = []
    for i, h in enumerate(heads):
        mark, claim = h.group(1), h.group(2).strip()
        body = text[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        url = ""
        mu = URL.search(body)
        if mu:
            url = mu.group(0)
        else:
            ms = re.search(r"出典[:：]\s*([^\n]{1,80})", body)
            if ms:
                url = ms.group(1).strip()
        correct = ""
        if mark == "❌":
            mc = re.search(r"(?:正|正しく|正確に)[:：は]\s*([^\n]{1,80})", body)
            if mc:
                correct = mc.group(1).strip()
        if claim in known or (mark == "✅" and not url):
            continue  # 既知、または出典の無いVERIFIEDは台帳に入れない
        rows.append([today, "VERIFIED" if mark == "✅" else "INCORRECT",
                     claim.replace("\t", " "), correct.replace("\t", " "),
                     url.replace("\t", " "), theme.replace("\t", " ")])
        known.add(claim)
    if not rows:
        return
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    if not os.path.exists(LEDGER):
        with open(LEDGER, "w", encoding="utf-8") as f:
            f.write("日付\t判定\t主張\t正しい値\t出典URL\tテーマ\n")
    with open(LEDGER, "a", encoding="utf-8") as f:
        for r in rows:
            f.write("\t".join(r) + "\n")
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M} +{len(rows)}行 from {os.path.basename(tpath)}\n")
    except OSError:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception:  # 台帳の副作用でセッションを止めない
        pass
    sys.exit(0)
