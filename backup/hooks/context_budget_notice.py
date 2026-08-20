#!/usr/bin/env python3
"""PostToolUse: セッションの文脈サイズを実測し、閾値を跨いだ時だけ1回警告する。

トークン消費はほぼ「文脈サイズ × ツール呼び出し回数」で決まる（2026-08実測で
月4,859Mトークンのうち約30%が起動時74.5Kの再送、残りは会話の積み上がり）。
文脈は減らないので、唯一効くのは「区切って /clear する」こと。
このフックは切り時を機械的に知らせるだけで、動作をブロックしない。
"""
import json, os, sys

THRESHOLDS = [120_000, 200_000, 300_000]
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
    if level >= 300_000:
        msg = (f"\u26d4 \u6587\u8108 {k}K \u30c8\u30fc\u30af\u30f3\u3002\u3053\u3053\u304b\u3089\u5148\u306f1\u30c4\u30fc\u30eb\u547c\u3073\u51fa\u3057\u3054\u3068\u306b {k}K \u3092\u518d\u9001\u3057\u3066\u3044\u308b\u3002\n"
               f"   \u3053\u306e\u5148100\u56de\u306e\u547c\u3073\u51fa\u3057\u3067 +{k*100//1000}M \u30c8\u30fc\u30af\u30f3\u3002\n"
               "   \u4eca\u3059\u3050\u533a\u5207\u308b\u3053\u3068\uff1a\u2460 \u4f5c\u308a\u304b\u3051\u306e\u6210\u679c\u7269\u3092 ~/outputs/ \u304b drafts/ \u306b\u4fdd\u5b58 "
               "\u2461 /clear \u2462 \u518d\u958b\u306f\u300c\u3044\u307e\u4f55\u3092\u3057\u3066\u3069\u3053\u307e\u3067\u9032\u3093\u3060\u304b\u300d1-2\u6587\u3067\u8ffd\u5f93\u3067\u304d\u308b\u3002")
    elif level >= 200_000:
        msg = (f"\U0001f534 \u6587\u8108 {k}K \u30c8\u30fc\u30af\u30f3\u3002\u547c\u3073\u51fa\u30571\u56de\u3042\u305f\u308a {k}K \u3092\u6255\u3063\u3066\u3044\u308b\u3002\n"
               f"   \u3053\u306e\u5148100\u56de\u306e\u547c\u3073\u51fa\u3057\u3067 +{k*100//1000}M \u30c8\u30fc\u30af\u30f3\u3002\n"
               "   \u533a\u5207\u308b\u524d\u306b\uff1a\u2460 \u6210\u679c\u7269\u3092 ~/outputs/ \u304b drafts/ \u306b\u4fdd\u5b58 \u2461 /clear "
               "\u2462 \u518d\u958b\u306f\u300c\u3044\u307e\u4f55\u3092\u3057\u3066\u3069\u3053\u307e\u3067\u9032\u3093\u3060\u304b\u300d1-2\u6587\u3002")
    else:
        msg = (f"\U0001f7e1 \u6587\u8108 {k}K \u30c8\u30fc\u30af\u30f3\u3002\u4ee5\u964d\u3053\u306e\u30bb\u30c3\u30b7\u30e7\u30f3\u306e\u30b3\u30b9\u30c8\u306f\u547c\u3073\u51fa\u3057\u56de\u6570\u306b\u6bd4\u4f8b\u3057\u3066\u5897\u3048\u308b\u3002\n"
               "   \u5225\u4ef6\u3092\u59cb\u3081\u308b\u306a\u3089\u65b0\u30bb\u30c3\u30b7\u30e7\u30f3\u3078\u3002\u753b\u50cf\u3092\u4f34\u3046\u4f5c\u696d\u30fb\u5e83\u3044\u63a2\u7d22\u304c\u3053\u306e\u5148\u306b\u63a7\u3048\u3066\u3044\u308b\u306a\u3089"
               "\u30b5\u30d6\u30a8\u30fc\u30b8\u30a7\u30f3\u30c8\u3078\u9694\u96e2\u3059\u308b\u3002")

    json.dump({"hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "[トークン監視] " + msg,
    }}, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
