#!/usr/bin/env python3
"""
発信物フォーマットゲート（機械可読・記憶依存をやめるための実装）

ブログ／SNS7種／ショート動画原稿が、各agent・SKILLの規定に収まっているかを自動判定する。
check_subtitle_band.py（ショート動画の字幕帯ゲート）と同じ思想で、
「ルールをmarkdownに書いておく」から「機械が落とす」へ移す。

正本:
  ブログ  = ~/.claude/agents/blog-writer.md（1500-2500字・5段構成厳守）
  SNS     = ~/.claude/agents/sns-content-creator.md（PF別字数）
  動画    = ~/.claude/skills/short-video-create/SKILL.md（35-45秒・憲法5構成）
            ~/.claude/agents/short-video-virality-architect.md

使い方:
  python3 check_content_limits.py <file.md> [<file.md> ...]
  種別はファイル名から自動判定（SNS7種 / ショート動画原稿 / それ以外=ブログ）

終了コード: 全PASSなら0、1件でもFAILなら1（フック・CIに載せられる）
"""
import sys, re, os

SNS_LIMITS = {  # 表示名の接頭辞 -> (下限, 上限)  ※Noneは規定なし
    "X（":            (None, 140),
    "Threads":        (300, 500),
    "Instagram":      (600, 1000),
    "Facebook":       (500, 800),
    "LINE":           (200, 400),
}
BLOG_MIN, BLOG_MAX = 1500, 2500
BLOG_STAGES = ["現場の声", "全国", "制度", "亀山", "締め"]  # 5段構成の手がかり
VIDEO_MIN_SEC, VIDEO_MAX_SEC = 35, 45
VIDEO_CHARS_PER_SEC = 7.0        # 日本語ナレの上限目安
VIDEO_MAX_SENTENCE = 30          # 一文30字超はanti-pattern

def n_chars(t):
    return len(re.sub(r"\s", "", t))

def kind_of(path):
    b = os.path.basename(path)
    if "SNS" in b:  return "sns"
    if "動画" in b: return "video"
    return "blog"

def check_sns(text):
    out = []
    for sec in re.split(r"\n## ", text)[1:]:
        name = sec.split("\n")[0].strip()
        body = "\n".join(sec.split("\n")[1:])
        body = re.sub(r"^\s*\*\*\d/\d\*\*\s*$", "", body, flags=re.M)  # スレッド番号除去
        n = n_chars(body)
        key = next((k for k in SNS_LIMITS if name.startswith(k)), None)
        if key is None:
            continue
        lo, hi = SNS_LIMITS[key]
        if hi and n > hi:
            out.append((False, f"{name}: {n}字 > 上限{hi}字"))
        elif lo and n < lo:
            out.append((False, f"{name}: {n}字 < 下限{lo}字"))
        else:
            out.append((True, f"{name}: {n}字"))
        # ハッシュタグ規定
        has_tag = "#" in body
        if key == "Threads" and has_tag:
            out.append((False, f"{name}: Threadsにハッシュタグ（規定=なし）"))
        if key == "LINE" and has_tag:
            out.append((False, f"{name}: LINEにハッシュタグ（規定=なし）"))
        if key == "X（" and not has_tag:
            out.append((False, f"{name}: Xにハッシュタグなし（規定=必須）"))
    if "<BLOG_URL>" in text:
        out.append((False, "プレースホルダ <BLOG_URL> が残っている（投稿前に実URLへ）"))
    return out

def check_blog(text):
    out = []
    body = re.split(r"\n【出典】|\n### 出典|\n## 出典", text)[0]
    body = re.split(r"◆亀山市政や", body)[0]
    n = n_chars(re.sub(r"^#.*$", "", body, flags=re.M))
    if n > BLOG_MAX:
        out.append((False, f"本文 {n}字 > 上限{BLOG_MAX}字（深掘りモード規定）"))
    elif n < BLOG_MIN:
        out.append((False, f"本文 {n}字 < 下限{BLOG_MIN}字"))
    else:
        out.append((True, f"本文 {n}字"))
    heads = re.findall(r"^(?:##\s*|■\s*)(.+)$", body, flags=re.M)
    out.append((len(heads) >= 4, f"見出し {len(heads)}本（5段構成の骨格が要る）"))
    first = body.strip().split("\n")
    named = any("草川たくやです" in l for l in first[:4])
    out.append((named, "冒頭の名乗り"))
    if "【ご意見箱】" not in text or "AIインタビュー" not in text:
        out.append((False, "定型フッター欠落（ご意見箱／LINE／Threads／AIインタビュー）"))
    else:
        out.append((True, "定型フッター"))
    return out

def check_video(text):
    out = []
    # 憲法5構成
    body = text
    cold = re.search(r"（0:00[^）]*）\s*\n([^\n]+)", body)
    if cold and "草川たくやです" in cold.group(1):
        out.append((False, "冒頭が名乗り＝コールドオープン逸脱（憲法・出荷拒否）"))
    else:
        out.append((True, "コールドオープン"))
    out.append((("多いんです" in body or "撮って" in body or "ご意見が" in body),
                "「撮っている理由」（憲法・出荷拒否）"))
    out.append((("必ず実現" in body or "あきらめません" in body),
                "結びの決意（憲法・出荷拒否）"))
    out.append((("コメントで教えてください" in body), "コメント誘発CTA"))
    # 尺
    secs = [int(m) for m in re.findall(r"0:(\d\d)-0:(\d\d)", body) for m in [m[1]]]
    if secs:
        total = max(secs)
        ok = VIDEO_MIN_SEC <= total <= VIDEO_MAX_SEC
        out.append((ok, f"尺 {total}秒（規定 {VIDEO_MIN_SEC}〜{VIDEO_MAX_SEC}秒）"))
    # 一文30字超
    lines = [l.strip() for l in body.split("\n")
             if l.strip() and not l.startswith(("#", "|", "-", "※", "（", ">"))]
    longs = [x for l in lines for x in re.split(r"(?<=。)", l) if 0 < len(x.strip()) and n_chars(x) > VIDEO_MAX_SENTENCE]
    out.append((not longs, f"一文30字超 {len(longs)}件" + (f" 例:「{longs[0][:34]}…」" if longs else "")))
    return out

def main(argv):
    files = argv
    if not files:
        print("usage: check_content_limits.py <file.md> ..."); return 1
    fail = 0
    for f in files:
        text = open(f, encoding="utf-8").read()
        k = kind_of(f)
        print(f"\n== {os.path.basename(f)}  [{k}] ==")
        res = {"sns": check_sns, "blog": check_blog, "video": check_video}[k](text)
        for ok, msg in res:
            print(("  ✅ " if ok else "  🚨 ") + msg)
            if not ok: fail += 1
    print(f"\n-- 違反 {fail}件 --")
    return 1 if fail else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
