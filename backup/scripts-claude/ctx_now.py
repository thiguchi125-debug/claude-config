#!/usr/bin/env python3
"""いまのセッションの文脈サイズを実測し、区切るべきかを判定する。

トークン消費は「文脈サイズ × 呼び出し回数」でほぼ決まる。文脈は減らないので、
区切る以外に効く手段はない。区切りの代償は起動時固定費（実測中央値73K）だけ。

使い方:  python3 ~/.claude/scripts/ctx_now.py
"""
import glob, json, os, sys, time

PROJ = os.path.expanduser("~/.claude/projects/-Users-kusakawatakuya")
STARTUP_COST = 73_200   # 起動時文脈の実測中央値（token_report.py より）
CUT_LINE = 300_000      # これを超えたら切ったほうが必ず得
TAIL = 400_000


def newest_transcript():
    """直近に書き込まれた jsonl ＝ いま話しているセッション。"""
    files = glob.glob(os.path.join(PROJ, "*.jsonl"))
    if not files:
        return None
    f = max(files, key=os.path.getmtime)
    # 5分以上更新が無ければ「いまのセッション」とは言えない
    if time.time() - os.path.getmtime(f) > 300:
        return None
    return f


def last_usage(path):
    """末尾から遡って最新の usage を探す。1行が巨大なことがあるので窓を広げる。"""
    size = os.path.getsize(path)
    window = TAIL
    with open(path, "rb") as f:
        while True:
            start = max(0, size - window)
            f.seek(start)
            if start:
                f.readline()
            for line in reversed(f.read().decode("utf-8", "replace").splitlines()):
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
                if ctx:
                    return ctx
            if start == 0 or window >= 8_000_000:
                return None
            window *= 4


def main():
    t = newest_transcript()
    if not t:
        print("⚠️ いまのセッションのtranscriptが特定できませんでした。")
        print("   （区切り判断は手動で。文脈が大きい実感があるなら切って損はありません）")
        return
    ctx = last_usage(t)
    if not ctx:
        print("⚠️ 文脈サイズを計測できませんでした（まだ呼び出しが少ない可能性）。")
        return

    k = ctx // 1000
    ahead = ctx * 100 // 1_000_000     # この先100回で何Mか
    saved = (ctx - STARTUP_COST) * 100 // 1_000_000  # 切った場合の100回あたり節約

    print(f"いまの文脈: {k}K トークン")
    print(f"  → 1ツール呼び出しごとに {k}K を再送している")
    print(f"  → このまま100回続けると +{ahead}M")
    print()
    if ctx >= CUT_LINE:
        print(f"⛔ 区切りどき。切れば次は 73K から始まり、"
              f"同じ100回で約 {saved}M 節約になる。")
        print("   Step 1（成果物の保存）→ Step 2（引き継ぎメモ）→ /clear へ進む。")
    elif ctx >= 200_000:
        print("🔴 そろそろ。いま一区切りつく作業なら、ここで切るのが得。")
        print("   別件を始めるなら必ず切る。")
    else:
        print("🟡 まだ切らなくてよい。区切りの代償（起動固定費73K）のほうが大きい。")
        print("   別件を始めるときだけ切る。")


if __name__ == "__main__":
    main()
