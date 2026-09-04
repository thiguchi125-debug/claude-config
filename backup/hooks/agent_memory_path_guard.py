#!/usr/bin/env python3
"""
エージェントの学び（agent-memory）を作業フォルダに書き捨てることを止める hook。

なぜ必要か（2026-09-04 実測）:
  サブエージェントは cwd 相対で `.claude/agent-memory/<agent>/` を作るため、
  ~/outputs/... や ~/publications/... の**案件フォルダの中**に学びを書いていた。
  実測 167件 / 81フォルダ。案件が終われば誰も読まない＝学びが毎回ゼロから積み直しになる。
  正規の置き場は ~/.claude/agent-memory/<agent>/ ただ1つ。

止める対象:
  Write / Edit の file_path、および Bash の mkdir / mv / cp / touch / tee / リダイレクトで、
  パスに該当語を含むのに正規フォルダ配下でないもの。

素通しする:
  読み取り系（find / grep / ls / cat / diff など書き込みを伴わない Bash）。
  正規パス配下への書き込み。
  Bash の語のうち「パスに見えないもの」＝スラッシュを含まない語・glob・変数展開・オプション。
  （2026-09-04 初日、検証コマンド中の説明文字列と glob パターンを宛先と誤認して deny した。
    宛先が確定できない語で止めない。）
失敗時はすべて素通し（hookのバグで作業を止めない）。
"""
import sys, os, json, re

KEY = "agent" + "-" + "memory"
CANON = os.path.realpath(os.path.expanduser("~/.claude/" + KEY))
WRITE_CMDS = ("mkdir", "mv ", "cp ", "touch", "tee", "install", "rsync", "sed -i",
              "python", "ruby", "perl")
REDIRECT = re.compile(r">>?\s*[^\s;|&]*" + re.escape(KEY))
TOKEN = re.compile(r"[^\s;|&<>()\"']*" + re.escape(KEY) + r"[^\s;|&<>()\"']*")
PREFIX_OK = re.compile(r"^[~./A-Za-z0-9_+-]*" + re.escape(KEY))


def is_stray(path, require_pathlike=False):
    if not path or KEY not in path:
        return False
    t = path.strip().strip("'\"")
    if require_pathlike:
        if "/" not in t:
            return False                       # 単なる語・説明文
        if any(c in t for c in "*?[]$\\"):
            return False                       # glob・変数展開は宛先を確定できない
        if t.startswith("-"):
            return False                       # オプション
        # 該当語より前が「パスとして通る文字」だけでなければ、文中にたまたま出た語。
        # 2026-09-04、日本語の説明文を宛先と誤認して deny した二度目の偽陽性。
        if not PREFIX_OK.match(t):
            return False
    p = os.path.realpath(os.path.expanduser(t))
    return not (p == CANON or p.startswith(CANON + os.sep))


def reason_for(paths):
    shown = "\n".join("  NG " + p for p in paths[:5])
    return (
        "[置き場ゲート] 学びの書き込み先が作業フォルダになっています。\n"
        + shown + "\n"
        + "正規の置き場は 1つだけです → " + CANON + "/<agent名>/<ファイル名>.md\n"
        "案件フォルダに書くと、その案件が終わった時点で誰からも読まれなくなります"
        "（2026-09-04 に 167件を回収）。\n"
        "・書き込み先を上記の正規パスに変える\n"
        "・追記したら同じフォルダの MEMORY.md にも 1行の索引を足す（索引が無いと読まれない）"
    )


def main():
    try:
        ev_in = json.load(sys.stdin)
    except Exception:
        return 0
    try:
        tool = ev_in.get("tool_name") or ""
        ti = ev_in.get("tool_input") or {}
        hits = []

        if tool in ("Write", "Edit", "NotebookEdit"):
            fp = ti.get("file_path") or ti.get("notebook_path") or ""
            if is_stray(fp):
                hits.append(fp)

        elif tool == "Bash":
            cmd = ti.get("command") or ""
            if KEY in cmd:
                if any(c in cmd for c in WRITE_CMDS) or REDIRECT.search(cmd):
                    for tok in TOKEN.findall(cmd):
                        if is_stray(tok, require_pathlike=True):
                            hits.append(tok)

        if hits:
            seen, uniq = set(), []
            for h in hits:
                if h not in seen:
                    seen.add(h)
                    uniq.append(h)
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason_for(uniq)}}, ensure_ascii=False))
            return 0
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
