#!/usr/bin/env python3
"""SessionStart: /kugiri が書いた引き継ぎメモを新セッションの冒頭に流し込む。

2026-09-05 改訂: LAST.md（1枠）をやめ、archive/ 直読みにした。
  同日08:19〜08:24に3セッションがほぼ同時に区切り、LAST.md を上書きし合った結果、
  ブログの再開セッション2本が別案件（発信フロー改善A-1）を二重に走らせた。
  1枠の上書き競合を構造から消すため、24時間以内のメモを全部（最大 MAX_FILES）
  案件名付きで注入し、複数あれば草川に1問で選ばせる。

なぜ「パスの案内」ではなく「中身そのもの」を入れるか:
  中身は1本あたり最大でも約800トークン。起動直後の文脈73Kで cat を1回走らせると
  その呼び出しだけで73Kを払う。中身を直接入れるほうが100倍以上安い。

テストは KUGIRI_HANDOFF_DIR にダミーディレクトリを渡して行う（本物の handoff/ を触らない）。
"""
import glob, json, os, re, sys, time

DIR = os.environ.get("KUGIRI_HANDOFF_DIR") or os.path.expanduser("~/.claude/handoff/archive")
MAX_AGE_H = 24        # これより古い引き継ぎは出さない
MAX_FILES = 3         # 並行案件はこの数まで注入（多いほど固定費が増える）
MAX_CHARS = 2000      # 1本あたりの保険


def title_of(path):
    """archive/<YYYY-MM-DD_HHMM>_<案件名>.md → 案件名"""
    base = os.path.basename(path)[:-3]
    return re.sub(r"^\d{4}-\d{2}-\d{2}_\d{4}_", "", base)


def when(h):
    return "約%d分前" % (h * 60) if h < 1 else "約%.1f時間前" % h


def main():
    now = time.time()
    items = []
    for p in glob.glob(os.path.join(DIR, "*.md")):
        try:
            age_h = (now - os.path.getmtime(p)) / 3600
            if age_h > MAX_AGE_H:
                continue
            body = open(p, encoding="utf-8").read().strip()
        except OSError:
            continue
        if not body:
            continue
        if len(body) > MAX_CHARS:
            body = body[:MAX_CHARS] + "\n…（以下省略。全文は " + p + "）"
        items.append((age_h, p, body))
    if not items:
        return
    items.sort()
    items = items[:MAX_FILES]

    if len(items) == 1:
        age_h, p, body = items[0]
        msg = (
            "[引き継ぎあり] 直前のセッションを " + when(age_h) + " に /kugiri で区切っています"
            "（案件: " + title_of(p) + "）。\n"
            "草川が「再開」「続きから」「さっきの続き」等と言ったら、"
            "下の『次の一手』から着手すること。\n"
            "前セッションの経緯を掘り返さない（掘り返すと区切った意味が消える）。"
            "過去ログが要るときだけ必要箇所を sed -n で抜く。\n"
            "草川が別の用件を始めた場合は、この引き継ぎには触れない。\n"
            "--- " + p + " ---\n" + body
        )
    else:
        heads = "\n".join("  %d. %s（%s）" % (i + 1, title_of(p), when(h))
                          for i, (h, p, _) in enumerate(items))
        msg = (
            "[引き継ぎが%d件] 24時間以内に並行セッションが別々の案件で区切っています。\n" % len(items)
            + heads + "\n"
            "草川が「再開」とだけ言ったら、どの案件かを AskUserQuestion 1問（上の番号を選択肢に）で"
            "確認してから、その『次の一手』に着手すること。案件名を言われたら聞かずにそれを選ぶ。\n"
            "選ばなかった案件のメモには触れない。経緯を掘り返さない。"
            "草川が別の用件を始めた場合は、この引き継ぎには触れない。\n"
        )
        for i, (h, p, body) in enumerate(items):
            msg += "\n=== %d. %s --- %s ===\n%s\n" % (i + 1, title_of(p), p, body)

    json.dump({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": msg,
    }}, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
