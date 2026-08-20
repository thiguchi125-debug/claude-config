#!/usr/bin/env python3
"""PreToolUse(Read): 親セッションに画像を積み上げすぎるのを止める。

2026-08の実測で、重いセッションの正体は印刷物のデザインループだった:
  ed309187 = 画像147枚 / 446.8Mトークン, 619d05d7 = 110枚 / 229.8M。
画像1枚は約1,500トークンを「セッション終了まで」占有し、以降の全呼び出しで
再送される。147枚 ≒ 220K が757回の呼び出しに毎回乗っていた計算になる。

レンダ→目視→修正のループは print-layout-architect / natural-design-reviewer
の中で回せば、スクショは親に残らない。このフックはその誘導を機械的にかける。

閾値を超えたら deny するが、詰まったときの解除方法をメッセージに必ず書く。
"""
import json, os, sys

WARN1, WARN2, DENY = 10, 18, 25
STATE_DIR = os.path.expanduser("~/.claude/hooks/state")
EXTS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic", ".bmp", ".tiff")


def main():
    try:
        inp = json.load(sys.stdin)
    except ValueError:
        return
    if inp.get("tool_name") != "Read":
        return
    path = (inp.get("tool_input") or {}).get("file_path") or ""
    if not path.lower().endswith(EXTS):
        return

    sid = inp.get("session_id") or "unknown"
    sf = os.path.join(STATE_DIR, f"{sid}.imgcount")
    try:
        n = int(open(sf).read().strip())
    except (OSError, ValueError):
        n = 0
    n += 1

    os.makedirs(STATE_DIR, exist_ok=True)
    try:
        with open(sf, "w") as f:
            f.write(str(n))
    except OSError:
        return

    reset = f"rm {sf}"

    if n >= DENY:
        json.dump({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"このセッションで画像を {n} 枚読んでいる（約 {n*3//2}K トークンが以降の"
                "全呼び出しに乗り続ける）。レンダ確認の繰り返しは親セッションで抱えないこと。\n"
                "  ・実装と目視のループ → Agent(print-layout-architect) の中で完結させる\n"
                "  ・破綻チェックだけ   → Agent(natural-design-reviewer) に PNG のパスを渡す\n"
                "  ・区切ってよい段階なら成果物を保存して /clear\n"
                f"どうしても親で見る必要がある場合はカウンタを消す: {reset}"
            ),
        }}, sys.stdout, ensure_ascii=False)
        return

    msg = None
    if n == WARN2:
        msg = (f"画像 {n} 枚（約 {n*3//2}K トークン）。ここから先の呼び出しは毎回この分を再送する。"
               f"{DENY} 枚で打ち止めになる。レンダ確認のループは print-layout-architect / "
               "natural-design-reviewer に移すこと。")
    elif n == WARN1:
        msg = (f"画像 {n} 枚（約 {n*3//2}K トークン）がこのセッションに乗った。"
               "同じPNGを何度も見直す作業になっているなら、サブエージェント側で回せば親に残らない。")
    if msg:
        json.dump({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "additionalContext": "[画像バジェット] " + msg,
        }}, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
