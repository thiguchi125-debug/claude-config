#!/usr/bin/env python3
"""トークン消費の実測レポート。対策の効果を同じ物差しで測り直すために使う。

  python3 ~/.claude/scripts/token_report.py            # 直近14日
  python3 ~/.claude/scripts/token_report.py 30         # 直近30日
  python3 ~/.claude/scripts/token_report.py 14 08-19   # 起動時文脈を指定日で前後比較

コストは「文脈サイズ × ツール呼び出し回数」でほぼ決まる。見るべきは
①1日あたりの総トークン ②上位セッションへの集中度 ③画像の2度読み率
④起動時文脈（＝毎回払う固定費）の4つ。
"""
import json, glob, os, sys, statistics, collections, datetime

D = os.path.expanduser("~/.claude/projects/-Users-kusakawatakuya")
IMGEXT = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".pdf", ".heic", ".bmp", ".tiff")


def scan(path):
    """1セッション分を1回のパスで読む。"""
    day = ""
    first = last = 0
    calls = 0
    total = 0
    imgreads = []
    started = None
    for line in open(path, errors="replace"):
        try:
            o = json.loads(line)
        except ValueError:
            continue
        ts = o.get("timestamp") or ""
        if ts:
            if not started:
                started = ts
            if ts[:10] > day:
                day = ts[:10]
        m = o.get("message")
        if not isinstance(m, dict):
            continue
        if m.get("role") == "assistant":
            for c in m.get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == "Read":
                    p = (c.get("input") or {}).get("file_path") or ""
                    if p.lower().endswith(IMGEXT):
                        imgreads.append(p)
        u = m.get("usage")
        if u:
            ctx = ((u.get("input_tokens") or 0)
                   + (u.get("cache_creation_input_tokens") or 0)
                   + (u.get("cache_read_input_tokens") or 0))
            if ctx:
                if not first:
                    first = ctx
                last = ctx
                calls += 1
                total += ctx
    return dict(day=day, started=started, first=first, last=last,
                calls=calls, total=total, imgreads=imgreads)


def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    split = sys.argv[2] if len(sys.argv) > 2 else None  # "MM-DD"
    since = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()

    sess = []
    for f in glob.glob(D + "/*.jsonl"):
        s = scan(f)
        if s["calls"] and s["day"] >= since:
            s["id"] = os.path.basename(f)[:8]
            sess.append(s)
    if not sess:
        print("対象セッションなし")
        return

    byday = collections.defaultdict(lambda: [0, 0, 0])  # tokens, calls, sessions
    for s in sess:
        b = byday[s["day"]]
        b[0] += s["total"]; b[1] += s["calls"]; b[2] += 1

    print(f"=== 日別（直近{days}日）")
    print("日付        セッション 呼出   総トークン  平均文脈")
    for d in sorted(byday):
        t, c, n = byday[d]
        print(f"{d}  {n:6d} {c:6d} {t/1e6:9.1f}M  {t/c/1000:7.0f}K")

    TOT = sum(s["total"] for s in sess)
    TC = sum(s["calls"] for s in sess)
    print(f"\n合計 {TOT/1e6:.0f}M トークン / {TC} 呼び出し / {len(sess)} セッション")

    sess.sort(key=lambda s: -s["total"])
    print("\n=== 集中度（ここが偏るほど「区切り」が効く）")
    for k in (5, 10):
        if len(sess) >= k:
            sub = sess[:k]
            print(f"  上位{k:2d}セッション = 全トークンの {sum(x['total'] for x in sub)/TOT*100:4.1f}%"
                  f"（呼び出しでは {sum(x['calls'] for x in sub)/TC*100:4.1f}%）")
    print("\n=== 重いセッション上位5")
    print("  日付        ID       呼出  総トークン  到達文脈")
    for s in sess[:5]:
        print(f"  {s['day']} {s['id']} {s['calls']:5d} {s['total']/1e6:8.1f}M  {s['last']/1000:7.0f}K")

    allimg = [p for s in sess for p in s["imgreads"]]
    dup = sum(v - 1 for s in sess for v in collections.Counter(s["imgreads"]).values() if v > 1)
    print(f"\n=== 画像Read {len(allimg)}件 / うち同一ファイルの2度読み {dup}件"
          f"（{dup/len(allimg)*100:.0f}%）" if allimg else "\n=== 画像Read なし")
    print("    ※ image_reread_guard.py 導入後はここが0%に近づくのが正常")

    print("\n=== 起動時文脈（毎回払う固定費）")
    if split:
        cut = f"2026-{split}"
        pre = [s["first"] for s in sess if s["started"] and s["started"][:10] < cut]
        post = [s["first"] for s in sess if s["started"] and s["started"][:10] >= cut]
        for lbl, v in (("前", pre), ("後", post)):
            if v:
                print(f"  {cut}{lbl}: n={len(v):3d} 中央値={statistics.median(v)/1000:5.1f}K"
                      f"  幅={min(v)/1000:.1f}〜{max(v)/1000:.1f}K")
        if pre and post and len(post) < 10:
            print(f"  ※ 後n={len(post)}は少なすぎ。ばらつき幅より小さい差は判定できない")
    else:
        v = [s["first"] for s in sess]
        print(f"  n={len(v)} 中央値={statistics.median(v)/1000:.1f}K"
              f"  幅={min(v)/1000:.1f}〜{max(v)/1000:.1f}K")


if __name__ == "__main__":
    main()
