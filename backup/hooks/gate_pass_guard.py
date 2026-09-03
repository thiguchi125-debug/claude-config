#!/usr/bin/env python3
"""
`gate.py --pass` を「保存を実行する側」が自分で名乗れないようにする PreToolUse hook。

なぜ必要か（2026-09-03）:
  notion-saver（保存役のサブエージェント）が、Notion書き込みを deny されたとき、
  復旧のために自分で `gate.py --pass` を実行して指紋を記録し直し、そのまま書き込んだ。
  結果は正しかった（内容は親セッションで fact/risk 通過済みだった）が、
  **保存役が自分で自分に合格を出せる経路が存在している**こと自体が穴。
  --pass は「content-fact-checker と content-risk-reviewer を実際に通し、指摘を潰した」
  という宣言であり、両エージェントを起動できるのは親セッションだけ。

止める対象:
  サブエージェントから実行された `gate.py ... --pass`。
  判定は transcript_path（サブエージェントの記録は .../tasks/<agentId>.* に出る）。
  検出できないときは**通す**（fail-open。hookのバグで作業を止めない）。

記録:
  通した／止めたにかかわらず、--pass の実行を _gate_pass_audit.log に1行残す。
  「誰がいつ何に合格を出したか」を後から追えるようにするため。
"""
import sys, os, json, re, time

AUDIT = os.path.expanduser("~/.claude/hooks/_gate_pass_audit.log")

DENY = """`gate.py --pass` はサブエージェントからは実行できません。

--pass は「content-fact-checker と content-risk-reviewer を実際に通し、
指摘を潰した」という宣言です。両エージェントを起動できるのは親セッションだけで、
保存役が自分で自分に合格を出すと、ゲートは素通りするだけの飾りになります。

Notion書き込みが deny された場合は、本文を変えずに **denyされた事実と理由を
そのまま親に報告して停止**してください。指紋の記録し直しは親が行います。
（deny の原因が並行セッションによる承認記録の消失であることも多いので、
 まず `~/.claude/hooks/_content_gate.json` を疑うよう報告に書き添えてください）"""


def is_subagent(data):
    tp = str(data.get("transcript_path") or "")
    # サブエージェントの記録は .../tasks/<agentId>.jsonl|.output に出る
    if re.search(r"[/\\]tasks[/\\]", tp):
        return True
    return False


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    cmd = (data.get("tool_input") or {}).get("command") or ""
    if "gate.py" not in cmd or "--pass" not in cmd:
        return 0

    sub = False
    try:
        sub = is_subagent(data)
        with open(AUDIT, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({
                "at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "subagent": sub,
                "session": data.get("session_id", ""),
                "transcript": str(data.get("transcript_path") or "")[-120:],
                "cmd": cmd[:300],
            }, ensure_ascii=False) + "\n")
    except Exception:
        return 0

    if sub:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": DENY}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
