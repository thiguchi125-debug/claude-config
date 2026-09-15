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
import json
import time, os, re, sys, datetime

LEDGER = os.path.expanduser("~/.claude/agents/knowledge/fact_ledger/verified_facts.tsv")
LOG = os.path.expanduser("~/.claude/agents/knowledge/fact_ledger/_autolog.log")
HEAD = re.compile(r"^###\s*C?\d*[:：]?\s*(✅|❌|❓)\s*「([^」]{3,200})」", re.M)
URL = re.compile(r"https?://[^\s)>」]+")
LEDGER_HINT = re.compile(r"ledger\s*[:：=]\s*[`'\"]?([^\s`'\"）)]+_ledger\.json)")
OUTPUTS_DIR = re.compile(r"((?:~|/[^\s`'\"）)]*?))/outputs/([^/\s`'\"）)]+)/")
VERDICT = re.compile(r"(?:\*\*)?判定(?:\*\*)?\s*[:：]\s*[^\n]*?(APPROVE|ASK_USER|REVISE|REJECT|REROUTE)")
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


# ── 判定の読み取り（2026-09-15改）
# 旧版は「### Cn: ✅ 「主張」」の1形式しか読めず、実際のゲート出力（記号なし見出し・表・
# 「1. … → **VERIFIED**」・「**N6 ✅ 「…」**」）ではclaimsが空のままだった。
MARK_V = {"✅": "VERIFIED", "❌": "INCORRECT", "🚫": "INCORRECT", "❓": "UNVERIFIED", "⚠": "MINOR_DIFF"}
KW_RE = re.compile(r"(?<![A-Z_])(UNVERIFIED|VERIFIED|INCORRECT|WRONG|HALLUCINATION|MINOR_DIFF|MINOR)(?![A-Z])")
KW_V = {"UNVERIFIED": "UNVERIFIED", "VERIFIED": "VERIFIED", "INCORRECT": "INCORRECT", "WRONG": "INCORRECT",
        "HALLUCINATION": "INCORRECT", "MINOR_DIFF": "MINOR_DIFF", "MINOR": "MINOR_DIFF"}
MARK_CHARS = "✅❌🚫❓⚠"
SECTION_RE = re.compile(r"^##\s+(?!#)(.*)$")
ITEM_RE = re.compile(r"^(?:#{3,4}\s+(.+)|\*\*([^*\n]{0,20}?[" + MARK_CHARS + r"]️?\s*「[^」\n]{3,200}」[^\n]*))$")
ID_RE = re.compile(r"^(?:項目\s*\d+|[A-Za-z]{0,4}[-‐]?\d+[a-z]?(?:[-/][A-Za-z0-9-]+)*)(?:[\s　:：.、]+|(?=[「" + MARK_CHARS + r"]))")
LIST_LINE = re.compile(r"^\s*(?:\d+[.)．]|[-*])\s+(.{3,200}?)\s*(?:→|⇒|->)\s*(.*)$")
# 見出しに判定語が無いときの日本語の節名（上から順に判定。「要修正（誤りではない）」を誤りにしないため順序が意味を持つ）
SECTION_JA = [("UNVERIFIED", ("未検証", "出典不明", "出典未確認", "出典なし", "確認不能", "出典が民間")),
              ("MINOR_DIFF", ("軽微", "要修正", "修正推奨", "任意修正")),
              ("INCORRECT", ("修正必須", "必須修正", "誤り", "直す必要")),
              ("VERIFIED", ("検証OK", "確定", "確認できた", "完全一致"))]


def _verdict_in(s):
    s = (s or "").replace("*", "").strip()
    for ch, v in MARK_V.items():
        if s.startswith(ch):
            return v
    m = KW_RE.search(s)
    return KW_V[m.group(1)] if m else ""


def _section_verdict(s):
    v = _verdict_in(s)
    if v:
        return v
    for vv, words in SECTION_JA:
        if any(w in s for w in words):
            return vv
    return ""


def _lead_verdict(s):
    """文字列の先頭（記号・太字を除いて20字以内）に判定語があるときだけ返す"""
    t = (s or "").replace("*", "").strip()
    for ch, v in MARK_V.items():
        if t.startswith(ch):
            return v
    m = KW_RE.search(t[:20])
    return KW_V[m.group(1)] if m else ""


def _claim_text(cell):
    c = cell.replace("**", "").strip()
    c = ID_RE.sub("", c, count=1).strip()
    c = re.sub(r"^[" + MARK_CHARS + r"]️?\s*", "", c)
    c = KW_RE.sub("", c, count=1) if KW_RE.match(c) else c
    c = c.strip()
    m = re.match(r"^(?:[^「」]{0,12}?)「([^」]{3,200})」", c)
    if m:
        return m.group(1).strip()
    c = re.split(r"\s*(?:→|⇒|->|—|――)\s*", c, maxsplit=1)[0]
    return c[:200].strip()


def _source_of(body):
    mu = URL.search(body)
    if mu:
        return mu.group(0)
    ml = re.search(r"URL[:：]\s*(local:[^\s|]{1,160})", body)
    if ml:
        return ml.group(1).strip()
    ms = re.search(r"出典[:：]\s*([^\n|]{1,80})", body)
    return ms.group(1).strip() if ms else ""


def parse_claims(text):
    lines = text.splitlines()
    starts = []  # (行番号, verdict, claim, kind)
    section_v = ""
    for i, ln in enumerate(lines):
        msec = SECTION_RE.match(ln)
        if msec and ID_RE.match(msec.group(1)) and \
                re.match(r"^[" + MARK_CHARS + r"]", ID_RE.sub("", msec.group(1), count=1).replace("*", "").strip()):
            msec = None  # 「## C1 ❌ 「…」」のように##で書かれた項目は節でなく主張として読む
            ln = "### " + ln.lstrip("#").strip()
        if msec:
            section_v = _section_verdict(msec.group(1))
            starts.append((i, "", "", "section"))
            continue
        mi = ITEM_RE.match(ln)
        if mi:
            h = (mi.group(1) or mi.group(2) or "").replace("**", "").strip()
            rest = ID_RE.sub("", h, count=1).strip()
            v = _lead_verdict(rest) or section_v
            starts.append((i, v, _claim_text(rest), "head"))
            continue
        if ln.lstrip().startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            hit = False
            for j in range(1, len(cells)):
                # 判定セルは判定語・記号で始まるものだけ（「OK」「3件」等の集計表は拾わない）
                t = cells[j].replace("*", "").strip()
                v = MARK_V.get(t[:1], "") or (KW_V[KW_RE.match(t).group(1)] if KW_RE.match(t) else "")
                if v:
                    claim = _claim_text(cells[j - 1])
                    if len(claim) >= 3:
                        starts.append((i, v, claim, "row"))
                    hit = True
                    break
            # 判定列の無い表（「## ✅ 検証OK」節の | C1 | 主張 | 一次情報 |）は節の判定を使う
            if not hit and section_v and len(cells) >= 3 and ID_RE.match(cells[0] + " "):
                claim = _claim_text(cells[1])
                if len(claim) >= 3:
                    starts.append((i, section_v, claim, "row"))
            continue
        ml = LIST_LINE.match(ln)
        if ml:
            v = _lead_verdict(ml.group(2))
            if v:
                starts.append((i, v, _claim_text(ml.group(1)), "list"))
    out = []
    seen = set()
    for k, (i, v, claim, kind) in enumerate(starts):
        if kind == "section" or not v or len(claim) < 3 or claim in seen:
            continue
        if kind == "row":
            body = lines[i]
        else:
            nxt = starts[k + 1][0] if k + 1 < len(starts) else len(lines)
            body = "\n".join(lines[i:nxt])
        correct = ""
        if v == "INCORRECT":
            mc = re.search(r"(?:\*\*)?(?:修正案|正しい値|正しくは|正確には|正)(?:\*\*)?\s*[:：]\s*(?:\*\*)?[「`]?([^\n」`]{1,80})", body) \
                or re.search(r"(?:正しくは|正確には)\s*[「`]?([^\n」`]{1,80})", body)
            if mc:
                correct = mc.group(1).strip()
        seen.add(claim)
        out.append({"claim": claim, "verdict": v, "correct": correct, "source": _source_of(body)})
    return out


def append_global(claims, theme, tpath):
    known = existing_claims()
    today = datetime.date.today().isoformat()
    rows = []
    for c in claims:
        if c["verdict"] not in ("VERIFIED", "INCORRECT"):
            continue  # UNVERIFIED・MINOR_DIFF は横断台帳に入れない（テーマ内台帳のみ）
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
    # 同一サブエージェントの途中停止で複数回鳴るため、同じtranscriptの行は最新1件に畳む（2026-09-06実測）
    d["gate_runs"] = [r for r in d["gate_runs"] if r.get("transcript") != os.path.basename(tpath)]
    d["gate_runs"].append({"agent": agent, "verdict": verdict or "",
                           "kind": mc.group(1) if mc else "", "at": now,
                           "transcript": os.path.basename(tpath)})
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def resolve_subagent_transcript(inp):
    """SubagentStop の transcript_path は親セッションの記録。サブ本体は
    <親の親dir>/<session_id>/subagents/agent-<agent_id>.jsonl に別置き（2026-09-06実測）。"""
    for k in ("agent_transcript_path", "subagent_transcript_path"):
        p = inp.get(k) or ""
        if p and os.path.exists(p):
            return p
    parent = inp.get("transcript_path") or ""
    sid = inp.get("session_id") or (os.path.basename(parent)[:-6] if parent.endswith(".jsonl") else "")
    sdir = os.path.join(os.path.dirname(parent), sid, "subagents") if parent and sid else ""
    aid = inp.get("agent_id") or inp.get("agentId") or ""
    if sdir and aid:
        p = os.path.join(sdir, f"agent-{aid}.jsonl")
        if os.path.exists(p):
            return p
    if sdir and os.path.isdir(sdir):
        cands = [os.path.join(sdir, f) for f in os.listdir(sdir)
                 if f.startswith("agent-") and f.endswith(".jsonl")]
        cands = [c for c in cands if time.time() - os.path.getmtime(c) < 300]
        if cands:
            return max(cands, key=os.path.getmtime)
    return parent if parent and os.path.exists(parent) else ""


def main():
    try:
        inp = json.load(sys.stdin)
    except ValueError:
        return
    tpath = resolve_subagent_transcript(inp)
    if not tpath:
        return
    if not inp.get("agent_type"):
        try:
            with open(tpath[:-6] + ".meta.json", encoding="utf-8") as f:
                inp["agent_type"] = json.load(f).get("agentType", "")
        except (OSError, ValueError):
            pass
    prompt, text = read_transcript(tpath)
    # フック入力の last_assistant_message は停止時点の最終報告そのもの。transcriptへの
    # 書き出しが間に合っていないことがあるため、読める主張が多い方を採る
    lam = inp.get("last_assistant_message") or ""
    if isinstance(lam, str) and lam.strip() and lam.strip() != text.strip():
        if not text or len(parse_claims(lam)) >= len(parse_claims(text)):
            text = lam
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
                    f"{'theme=' + lp if lp else 'theme=-'} from {os.path.basename(tpath)} "
                    f"keys={','.join(sorted(k for k in inp if k != 'agent_type'))}\n")
    except OSError:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception:  # 台帳の副作用でセッションを止めない
        pass
    sys.exit(0)
