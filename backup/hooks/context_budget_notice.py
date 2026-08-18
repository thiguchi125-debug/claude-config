#!/usr/bin/env python3
"""PostToolUse: セッションの文脈サイズを実測し、閾値を跨いだ時だけ1回警告する。

トークン消費はほぼ「文脈サイズ × ツール呼び出し回数」で決まる（2026-08実測で
月4,859Mトークンのうち31%が起動時75Kの再送、残りは会話の積み上がり）。
文脈は減らないので、唯一効くのは「区切って /clear する」こと。
このフックは切り時を機械的に知らせるだけで、動作をブロックしない。
"""
import json, os, sys

THRESHOLDS = [200_000, 350_000, 500_000, 700_000]
STATE_DIR = os.path.expanduser("~/.claude/hooks/state")
TAIL_BYTES = 300_000
MAX_SCAN = 6_000_000  # usage が見つかるまで末尾から遡る上限


def last_context(path):
    """transcript の末尾から遡って最新の usage を探し、文脈サイズを返す。

    1行が数百KBになることがある（画像base64を含む行）ため、固定幅の tail では
    usage 行を跨いで取りこぼす。見つかるまで窓を広げて遡る。
    """
    try:
        size = os.path.getsize(path)
        f = open(path, "rb")
    except OSError:
        return None
    with f:
        window = TAIL_BYTES
        while True:
            start = max(0, size - window)
            f.seek(start)
            if start:
                f.readline()  # 途中で切れた行を捨てる
            lines = f.read().decode("utf-8", "replace").splitlines()
            for line in reversed(lines):
                try:
                    o = json.loads(line)
                except ValueError:
                    continue
                m = o.get("message")
                u = m.get("usage") if isinstance(m, dict) else None
                if not u:
                    continue
                ctx = ((u.get("input_tokens") or 0)
                       + (u.get("cache_creation_input_tokens") or 0)
                       + (u.get("cache_read_input_tokens") or 0))
                if ctx:  # 合計0の空 usage 行は本物の計測値ではないので読み飛ばす
                    return ctx
            if start == 0 or window >= MAX_SCAN:
                return None
            window *= 4


def main():
    try:
        inp = json.load(sys.stdin)
    except ValueError:
        return
    sid = inp.get("session_id") or "unknown"
    tpath = inp.get("transcript_path")
    if not tpath:
        return

    sf = os.path.join(STATE_DIR, f"{sid}.ctx")
    try:
        prev = int(open(sf).read().strip())
    except (OSError, ValueError):
        prev = 0
    if prev >= THRESHOLDS[-1]:
        return  # 全閾値を通知済み。以降は transcript を読まずに即抜ける

    ctx = last_context(tpath)
    if not ctx:
        return

    crossed = [t for t in THRESHOLDS if ctx >= t]
    if not crossed:
        return
    level = max(crossed)
    if level <= prev:
        return  # この閾値は通知済み

    os.makedirs(STATE_DIR, exist_ok=True)
    try:
        with open(sf, "w") as f:
            f.write(str(level))
    except OSError:
        return

    k = ctx // 1000
    if level >= 700_000:
        msg = (f"⛔ 文脈 {k}K トークン。ここから先は1ツール呼び出しごとに {k}K を再送している。"
               "今の用件を成果物として保存し、直ちに /clear してから続きを始めること。")
    elif level >= 500_000:
        msg = (f"🔴 文脈 {k}K トークン。区切り時。作業中の内容をファイル/Notionに落として /clear。"
               "続きは「いま何をしていてどこまで進んだか」を1-2文で伝えれば追従できる。")
    elif level >= 350_000:
        msg = (f"🟠 文脈 {k}K トークン。次の区切りで /clear を検討。"
               "画像を扱う作業・広い探索がこの先に控えているならサブエージェントへ隔離する。")
    else:
        msg = (f"🟡 文脈 {k}K トークン。以降このセッションのコストは呼び出し回数に比例して増える。"
               "独立した別件を始めるなら新セッションに分けること。")

    json.dump({"hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "[トークン監視] " + msg,
    }}, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
