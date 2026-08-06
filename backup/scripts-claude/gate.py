#!/usr/bin/env python3
"""
発信物の安全ゲート実行＆記録（1コマンドに集約）

  python3 ~/.claude/scripts/gate.py <file...> [--pass]

ファイルは .md（ブログ/SNS/動画原稿）でも .html（挿入画像）でもよい。

やること:
  1. 種類に応じて機械チェックを全部回す
       .md   → check_content_limits.py
       .html → check_image_design.py / check_overflow.py（+ 同名pngがあれば帯ゲート）
  2. 全通過したら、各ファイルの**本文の指紋**を _content_gate.json に記録する
     （記録があってはじめて content_safety_gate.py がNotion書き込みを通す）

重要:
  機械チェックの通過は「壊れていない」ことしか保証しない。
  **content-fact-checker と content-risk-reviewer を通したかどうかは機械では判定できない。**
  よって --pass を付けたときだけ記録する。--pass は「2つのエージェントをこのセッションで
  実際に通し、指摘を潰した」という宣言であり、それ以外の意味では付けてはいけない。

  2026-08-06、機械ゲート3本を通したことで内容検証を代替した気になり、risk-reviewerが
  必須とした一文を削って被災地への指弾だけが残る画像を作った。機械ゲートは
  fact/riskの代わりにならない。
"""
import sys, os, json, re, hashlib, subprocess, time, unicodedata

SC = os.path.expanduser("~/.claude/scripts")
BAND = os.path.expanduser(
    "~/.claude/agents/knowledge/design_system/short_video_templates/check_subtitle_band.py")
GATE = os.path.expanduser("~/.claude/hooks/_content_gate.json")


def norm(t):
    # 全角/半角ゆれ＋markdownの装飾記号を両側で同じように落とす
    t = unicodedata.normalize("NFKC", t or "")
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"[*`>#|]", "", t)
    return re.sub(r"[\s　]+", "", t)


def fp(t):
    return hashlib.sha256(norm(t).encode("utf-8")).hexdigest()[:16]


def visible_text(path):
    s = open(path, encoding="utf-8").read()
    if path.endswith(".html"):
        s = re.sub(r"<style.*?</style>", "", s, flags=re.S)
        s = re.sub(r"<script.*?</script>", "", s, flags=re.S)
        s = re.sub(r"<svg.*?</svg>", "", s, flags=re.S)
    return s


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def main(argv):
    do_pass = "--pass" in argv
    files = [a for a in argv if not a.startswith("--")]
    if not files:
        print(__doc__); return 1
    mds = [f for f in files if f.endswith(".md")]
    htmls = [f for f in files if f.endswith(".html")]
    fail = 0

    if mds:
        c, o = run(["python3", os.path.join(SC, "check_content_limits.py")] + mds)
        print(o); fail += (c != 0)
    if htmls:
        for script in ("check_image_design.py", "check_overflow.py"):
            c, o = run(["python3", os.path.join(SC, script)] + htmls)
            print(o); fail += (c != 0)
        pngs = [os.path.splitext(h)[0] + ".png" for h in htmls
                if os.path.exists(os.path.splitext(h)[0] + ".png")]
        if pngs and os.path.exists(BAND):
            c, o = run(["python3", BAND] + pngs)
            print(o); fail += (c != 0)

    if fail:
        print("🚨 機械チェックに違反があります。直してから再実行してください。")
        return 1
    print("✅ 機械チェックは全通過。")

    if not do_pass:
        print("""
記録していません。記録するには --pass を付けてください。
--pass は「content-fact-checker と content-risk-reviewer をこのセッションで
実際に通し、指摘を潰した」という宣言です。機械チェックの通過は
fact/riskの代わりにはなりません。""")
        return 0

    rec = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "ttl_minutes": 120, "approved": []}
    for f in files:
        t = visible_text(f)
        rec["approved"].append({"file": os.path.basename(f), "fp": fp(t),
                                "text": norm(t)})
    json.dump(rec, open(GATE, "w"), ensure_ascii=False, indent=1)
    print(f"\n📝 {len(files)}件の本文指紋を記録しました（有効2時間）→ {GATE}")
    print("   本文を1文字でも変えたら指紋が変わり、Notion書き込みは再びdenyされます。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
