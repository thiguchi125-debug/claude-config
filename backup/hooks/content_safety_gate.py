#!/usr/bin/env python3
"""
発信物のNotion書き込みを、安全ゲート未通過なら deny する PreToolUse hook。

todoist_calendar_guard.py と同じ思想：ルールをmarkdownに書いておくのをやめ、
出口で機械的に止める。

止める対象:
  notion-create-pages / notion-update-page のうち、**本文（content / new_str /
  content_updates）を伴う呼び出し**だけ。プロパティだけの更新は素通しする。
  本文＝市民が読む文章なので、ここが発信の境界。

通す条件:
  ~/.claude/hooks/_content_gate.json に、**その本文と一致する指紋**が
  記録されていること。記録は `python3 ~/.claude/scripts/gate.py <files...>` が作る。
  本文を1文字でも変えたら指紋が変わり、再度ゲートを通すまで書き込めない。

なぜ必要か（2026-08-05〜06 の実例）:
  1. 「Notionに保存するだけ」を発信ではなくファイリングと解釈し、fact/riskを飛ばした。
  2. 画像を「仕様に合わせて作り直すだけ」＝デザイン作業と解釈し、また飛ばした。
     このとき risk-reviewer が必須とした一文（「亀山市も、0%です。」＝被災地への
     指弾を自分事化する装置）をレイアウト都合で削り、指摘前より悪化させた。
  どちらも「本文が変わったのに、本文の変更だと認識しなかった」ことが原因。
  人間の注意力ではなく指紋で検出する。
"""
import sys, os, json, re, hashlib, time

GATE = os.path.expanduser("~/.claude/hooks/_content_gate.json")
GUARDED = {
    "mcp__claude_ai_Notion__notion-create-pages",
    "mcp__claude_ai_Notion__notion-update-page",
}
DENY = """安全ゲート未通過のため、この本文はNotionへ書き込めません。

本文（市民が読む文章）を書き込む前に、必ず次を済ませてください。
  1. content-fact-checker を通す（数値・固有名詞・制度を一次情報まで遡る）
  2. content-risk-reviewer を通す（公選法・個人情報・名誉毀損・差別・利益相反・品位・物議）
  3. python3 ~/.claude/scripts/gate.py <対象ファイル...> で通過を記録

未登録の本文: {heads}

※本文を1文字でも変えたら指紋が変わります。「レイアウト都合で一文削る」も本文の変更です。
　risk-reviewerが必須とした文を落として指摘前より悪化させた実例があります（2026-08-06 a2）。
※プロパティだけの更新は止めません。"""


def norm(t):
    return re.sub(r"[\s　]+", "", re.sub(r"<[^>]+>", "", t or ""))


def fp(t):
    return hashlib.sha256(norm(t).encode("utf-8")).hexdigest()[:16]


def bodies(tool_input):
    """本文を伴う部分だけ取り出す。プロパティのみなら空。"""
    out = []
    for p in tool_input.get("pages", []) or []:
        if p.get("content"):
            out.append(p["content"])
    if tool_input.get("new_str"):
        out.append(tool_input["new_str"])
    if tool_input.get("content"):
        out.append(tool_input["content"])
    for u in tool_input.get("content_updates", []) or []:
        if u.get("new_str"):
            out.append(u["new_str"])
    return [b for b in out if norm(b)]


def approved():
    try:
        d = json.load(open(GATE))
    except Exception:
        return set()
    ttl = d.get("ttl_minutes", 120) * 60
    try:
        born = time.mktime(time.strptime(d["generated_at"][:19], "%Y-%m-%dT%H:%M:%S"))
    except Exception:
        return set()
    if time.time() - born > ttl:
        return set()
    return {e.get("fp") for e in d.get("approved", []) if e.get("fp")}


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if payload.get("tool_name") not in GUARDED:
        return 0
    bs = bodies(payload.get("tool_input", {}) or {})
    if not bs:
        return 0  # プロパティのみ＝素通し
    ok = approved()
    bad = [b for b in bs if fp(b) not in ok]
    if not bad:
        return 0
    heads = "\n".join("  ・" + norm(b)[:44] + "…" for b in bad[:4])
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": DENY.format(heads=heads),
        }
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
