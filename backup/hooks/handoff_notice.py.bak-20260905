#!/usr/bin/env python3
"""SessionStart: 直前に /kugiri で書いた引き継ぎメモを、新セッションの冒頭に流し込む。

これが無いと「再開」と言われても何を再開するのか分からず、草川に説明させることに
なる（＝区切りの心理的コストが残り、結局セッションが切られない）。

なぜ「パスの案内」ではなく「中身そのもの」を入れるか:
  中身は最大でも約500トークン。対して、起動直後の文脈73Kで cat を1回走らせると
  その呼び出しだけで73Kを払う。中身を直接入れるほうが100倍以上安い。

古い引き継ぎを延々と貼り続けないよう、MAX_AGE_H を過ぎたものは黙って無視する。
"""
import os, time

PATH = os.path.expanduser("~/.claude/handoff/LAST.md")
MAX_AGE_H = 24        # これより古い引き継ぎは出さない（別件を始めている可能性が高い）
MAX_CHARS = 2000      # 万一メモが長すぎた場合の保険


def main():
    try:
        age_h = (time.time() - os.path.getmtime(PATH)) / 3600
        body = open(PATH, encoding="utf-8").read().strip()
    except OSError:
        return
    if not body or age_h > MAX_AGE_H:
        return

    if len(body) > MAX_CHARS:
        body = body[:MAX_CHARS] + "\n…（以下省略。全文は " + PATH + "）"

    when = ("約%d分前" % (age_h * 60) if age_h < 1 else "約%.1f時間前" % age_h)

    msg = (
        "[引き継ぎあり] 直前のセッションを " + when + " に /kugiri で区切っています。\n"
        "草川が「再開」「続きから」「さっきの続き」等と言ったら、"
        "下の『次の一手』から着手すること。\n"
        "前セッションの経緯を掘り返さない（掘り返すと区切った意味が消える）。"
        "過去ログが要るときだけ必要箇所を sed -n で抜く。\n"
        "草川が別の用件を始めた場合は、この引き継ぎには触れない。\n"
        "--- " + PATH + " ---\n" + body
    )

    import json, sys
    json.dump({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": msg,
    }}, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
