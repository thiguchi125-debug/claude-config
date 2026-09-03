#!/usr/bin/env python3
"""PreToolUse: サブエージェントの中からさらにAgentを生やすのを止める。

2026-09-03 実測：サブエージェント83本・4,258呼び出し・440M のうち、サブの中から
呼ばれた Agent が227回あった。孫は本体の文脈にも `token_report.py` の集計にも
現れにくく、深さの歯止めが無いまま増える。深さ1（本体→サブ）までに固定する。

サブエージェントかどうかは transcript_path で判定する。サブは
`<projects>/<session_id>/subagents/agent-*.jsonl` に置かれる。
"""
import json, os, sys

DEEP = os.sep + "subagents" + os.sep


def main():
    try:
        inp = json.load(sys.stdin)
    except ValueError:
        return
    tpath = inp.get("transcript_path") or ""
    if DEEP not in tpath:
        return  # 本体からの呼び出しは通す
    tool = inp.get("tool_name") or "Agent"
    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": (
            f"サブエージェントの中から {tool} を呼ぶことは禁止（深さは1段まで）。"
            "孫エージェントは親の文脈にも実測にも現れないまま増え、2026-09-03 には"
            "227回発生して440Mの一因になった。"
            "いま持っているツール（WebSearch/WebFetch/Bash/Read）で自分で調べ切るか、"
            "調べ切れない範囲は『未確認』と明記して親に返すこと。"
            "分担が要るなら、その旨を報告に書いて親に判断させる。"
        ),
    }}, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
