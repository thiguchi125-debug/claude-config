#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SubagentStop: 安全ゲート系サブエージェント（content-fact-checker / content-gate-lite /
content-risk-reviewer）の最終報告から検証結果を拾い、2つの台帳へ自動追記する。

1. 横断台帳 ~/.claude/agents/knowledge/fact_ledger/verified_facts.tsv
   「### Cn: ✅ 「主張」」「### Cn: ❌ 「主張」」ブロック → 1主張1行（従来どおり）
2. テーマ内台帳 ~/outputs/<日付>_<テーマ>/_ledger.json（2026-09-05 設計書§3-E）
   claims（✅❌❓すべて）／approved_texts（risk側の APPROVE）／gate_runs（起動ログ）
   置き場は親の指示文に書かれた `ledger: <path>` を最優先、無ければ指示文中の
   最初の ~/outputs/<フォルダ>/ を採用。どちらも無ければテーマ内台帳は書かない。

親（スキル）は派生版のゲート時に _ledger.json のパスを渡すだけでよい。
"""
import json, os, re, sys, datetime

LEDGER = os.path.expanduser("~/.claude/agents/knowledge/fact_ledger/verified_facts.tsv")
LOG = os.path.expanduser("~/.claude/agents/knowledge/fact_ledger/_autolog.log")
HEAD = re.compile(r"^###\s*C?\d*[:：]?\s*(✅|❌|❓)\s*「([^」]{3,200})」", re.M)
URL = re.compile(r"https?://[^\s)>」]+")
LEDGER_HINT = re.compile(r"ledger\s*[:：=]\s*[`'\"]?([^\s`'\"）)]+_ledger\.json)")
OUTPUTS_DIR = re.compile(r"((?:~|/[^\s`'\"）)]*?))/outputs/([^/\s`'\"）)]+)/")
VERDICT = re.compile(r"\*\*判定\*\*\s*[:：]\s*[^\n]*?(APPROVE|ASK_USER|REVISE|REJECT|REROUTE)")
CTYPE = re.compile(r"content_type\s*[:：=]\s*[`'\"]?([A-Za-z0-9_-]+)")
DRAFT_PATH = re.compile(r"((?:~|/Users/[^/\s]+)/[^\s`'\"）)]+\.(?:md|txt|html))")


def read_transcript(path):
    """(最初のuser本文, 最後のassistant本文) を返す"""
    first_user, last_assistant = "", ""
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                try:
                    o = json.loads(line)
                except ValueError:
                    continue
                t = o.get("type")
                if t not in ("user", "assistant"):
                    continue
                m = o.get("message") or {}
                c = m.get("content")
                if isinstance(c, str):
                    parts = [c]
                else:
                    parts = [b.get("text", "") for b in (c or [])
                             if isinstance(b, dict) and b.get("type") == "text"]
                if not parts:
                    continue
                text = "\n".join(parts)
                if t == "user" and not first_user:
                    first_user = text
                elif t == "assistant":
                    last_assistant = text
    except OSError:
        pass
    return first_user, last_assistant


def detect_agent(inp, text):
    a = inp.get("agent_type") or inp.get("agent_name") or ""
    if a:
        return a
    if "短文ゲート結果" in text:
        return "content-gate-lite"
    if "リスクレビュー結果" in text:
        return "content-risk-reviewer"
    if "ファクトチェック" in text or HEAD.search(text):
        return "content-fact-checker"
    return ""


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


def parse_claims(text):
    heads = list(HEAD.finditer(text))
    out = []
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
        verdict = {"✅": "VERIFIED", "❌": "INCORRECT", "❓": "UNVERIFIED"}[mark]
        out.append({"claim": claim, "verdict": verdict, "correct": correct, "source": url})
    return out


def append_global(claims, theme, tpath):
    known = existing_claims()
    today = datetime.date.today().isoformat()
    rows = []
    for c in claims:
        if c["verdict"] == "UNVERIFIED":
            continue
        if c["claim"] in known or (c["verdict"] == "VERIFIED" and not c["source"]):
            continue  # 既知、または出典の無いVERIFIEDは台帳に入れない
        rows.append([today, c["verdict"], c["claim"].replace("\t", " "),
                     c["correct"].replace("\t", " "), c["source"].replace("\t", " "),
                     theme.replace("\t", " ")])
        known.add(c["claim"])
    if not rows:
        return 0
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    if not os.path.exists(LEDGER):
        with open(LEDGER, "w", encoding="utf-8") as f:
            f.write("日付\t判定\t主張\t正しい値\t出典URL\tテーマ\n")
    with open(LEDGER, "a", encoding="utf-8") as f:
        for r in rows:
            f.write("\t".join(r) + "\n")
    return len(rows)


def theme_ledger_path(prompt):
    m = LEDGER_HINT.search(prompt)
    if m:
        return os.path.expanduser(m.group(1))
    m = OUTPUTS_DIR.search(prompt)
    if m:
        return os.path.expanduser(f"{m.group(1)}/outputs/{m.group(2)}/_ledger.json")
    return ""


def update_theme_ledger(path, agent, claims, verdict, prompt, theme, tpath):
    d = {"theme": "", "claims": [], "approved_texts": [], "gate_runs": []}
    try:
        with open(path, encoding="utf-8") as f:
            d.update(json.load(f))
    except (OSError, ValueError):
        pass
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    today = now[:10]
    if theme and not d.get("theme"):
        d["theme"] = theme
    known = {c.get("claim") for c in d["claims"]}
    for c in claims:
        if c["claim"] in known:
            continue
        d["claims"].append({**c, "checked": today, "by": agent})
        known.add(c["claim"])
    mc = CTYPE.search(prompt)
    md = DRAFT_PATH.search(prompt)
    if verdict == "APPROVE" and agent in ("content-risk-reviewer", "content-gate-lite"):
        d["approved_texts"].append({
            "kind": mc.group(1) if mc else "",
            "path": md.group(1) if md else "",
            "by": agent, "at": now})
    d["gate_runs"].append({"agent": agent, "verdict": verdict or "",
                           "kind": mc.group(1) if mc else "", "at": now,
                           "transcript": os.path.basename(tpath)})
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def main():
    try:
        inp = json.load(sys.stdin)
    except ValueError:
        return
    tpath = inp.get("transcript_path") or ""
    if not tpath or not os.path.exists(tpath):
        return
    prompt, text = read_transcript(tpath)
    agent = detect_agent(inp, text)
    if agent not in ("content-fact-checker", "content-gate-lite", "content-risk-reviewer"):
        return
    claims = parse_claims(text)
    mv = VERDICT.search(text)
    verdict = mv.group(1) if mv else ""
    theme = ""
    mt = re.search(r"(?:テーマ|theme)[:：]\s*([^\n]{1,40})", text) or \
        re.search(r"(?:テーマ|theme)[:：]\s*([^\n]{1,40})", prompt)
    if mt:
        theme = mt.group(1).strip()
    n = append_global(claims, theme, tpath) if claims else 0
    lp = theme_ledger_path(prompt)
    if lp:
        update_theme_ledger(lp, agent, claims, verdict, prompt, theme, tpath)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M} {agent} +{n}行 "
                    f"{'theme=' + lp if lp else 'theme=-'} from {os.path.basename(tpath)}\n")
    except OSError:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception:  # 台帳の副作用でセッションを止めない
        pass
    sys.exit(0)
