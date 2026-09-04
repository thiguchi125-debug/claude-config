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
  パスに agent-memory を含むのに ~/.claude/agent-memory/ 配下でないもの。

素通しする:
  読み取り系（find / grep / ls / cat / diff など書き込みを伴わない Bash）。
  正規パス配下への書き込み。
失敗時はすべて素通し（hookのバグで作業を止めない）。
"""
import sys, os, json, re

CANON = os.path.realpath(os.path.expanduser("~/.claude/agent-memory"))
WRITE_CMDS = ("mkdir", "mv", "cp", "touch", "tee", "install", "rsync", "sed -i", "python", "ruby", "perl")
REDIRECT = re.compile(r">>?\s*[^\s;|&]*agent-memory")


def is_stray(path: str) -> bool:
    if not path or "agent-memory" not in path:
        return False
    p = os.path.realpath(os.path.expanduser(path.strip().strip("'\"")))
    return not (p == CANON or p.startswith(CANON + os.sep))


def reason_for(paths):
    shown = "\n".join(f"  ✗ {p}" for p in paths[:5])
    return (
        "[agent-memory 置き場ゲート] 学びの書き込み先が作業フォルダになっています。\n"
        f"{shown}\n"
        f"正規の置き場は 1つだけです → {CANON}/<agent名>/<ファイル名>.md\n"
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
            if "agent-memory" in cmd:
                writeish = any(c in cmd for c in WRITE_CMDS) or REDIRECT.search(cmd)
                if writeish:
                    for tok in re.findall(r"[^\s;|&<>()\"']*agent-memory[^\s;|&<>()\"']*", cmd):
                        if is_stray(tok):
                            hits.append(tok)

        if hits:
            seen, uniq = set(), []
            for h in hits:
                if h not in seen:
                    seen.add(h); uniq.append(h)
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
