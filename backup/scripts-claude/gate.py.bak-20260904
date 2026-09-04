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
import sys, os, json, re, glob, hashlib, subprocess, time, unicodedata

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
    # .txt も対象（SNS成果物は ~/outputs/sns/<日付>_<テーマ>/threads.txt 等の .txt で保存される。
    # 2026-09-02、.md しか見ていなかったため7本とも機械チェック0件のまま --pass で指紋記録された）
    mds = [f for f in files if f.endswith((".md", ".txt"))]
    htmls = [f for f in files if f.endswith(".html")]
    unchecked = [f for f in files if not f.endswith((".md", ".txt", ".html"))]
    if unchecked:
        print("⚠ 機械チェック未対応の拡張子（--pass を付けても中身は検査されていない）:")
        for f in unchecked:
            print("   - " + os.path.basename(f))
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

    # --- 禁止語スイープ ---
    # 「削除を決めた語が別ファイル・画像HTMLに残る」事故（2026-08-06 card_timeline）対策。
    # 対象mdと同じディレクトリの *_banned.txt を台帳とし、対象ファイル＋
    # md本文が参照する ~/outputs/ 配下のアセットディレクトリをまとめて掃く。
    banned = set()
    for f in files:
        d = os.path.dirname(os.path.abspath(f)) or "."
        for b in glob.glob(os.path.join(d, "*_banned.txt")):
            prefix = os.path.basename(b)[:-len("_banned.txt")]
            if any(os.path.basename(x).startswith(prefix) for x in files):
                banned.add(b)
    if banned:
        sweep = list(files)
        for f in mds:
            for m in re.findall(r"~/outputs/[^\s`）)」]+", open(f, encoding="utf-8").read()):
                p = os.path.expanduser(m.rstrip("/（。、"))
                d = p if os.path.isdir(p) else os.path.dirname(p)
                if os.path.isdir(d):
                    sweep.append(d)
        for b in sorted(banned):
            c, o = run(["python3", os.path.join(SC, "check_banned_terms.py"), b]
                       + sorted(set(sweep)))
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

    # 2026-09-03: 全書き換え→マージに変更。
    # 旧実装は json.dump(..., open(GATE,"w")) で丸ごと上書きしていたため、
    # 並行セッションが互いの承認記録を消し合っていた（本日、実際に別セッションの
    # 記録を消して deny を誘発。詳細 memory/feedback_gate_json_concurrent_overwrite.md）。
    # 以後：期限切れだけを落とし、同じファイルの古い記録だけを置き換え、他は残す。
    now = time.time()
    stamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    TTL_MIN = 120

    def _born(e, d):
        for v in (e.get("at"), d.get("generated_at")):
            try:
                return time.mktime(time.strptime(str(v)[:19], "%Y-%m-%dT%H:%M:%S"))
            except Exception:
                continue
        return 0.0

    lock = open(GATE + ".lock", "w")
    try:
        import fcntl
        fcntl.flock(lock, fcntl.LOCK_EX)
    except Exception:
        pass
    try:
        try:
            old = json.load(open(GATE))
        except Exception:
            old = {}
        kept = []
        names = {os.path.basename(f) for f in files}
        for e in old.get("approved", []):
            if e.get("file") in names:
                continue                      # 同じファイルは新しい記録で置き換える
            ttl = e.get("ttl_minutes", old.get("ttl_minutes", TTL_MIN)) * 60
            if now - _born(e, old) <= ttl:
                kept.append(e)                # 他セッションの生きた記録は残す
        fresh = []
        for f in files:
            t = visible_text(f)
            fresh.append({"file": os.path.basename(f), "fp": fp(t), "text": norm(t),
                          "at": stamp, "ttl_minutes": TTL_MIN,
                          "session": os.environ.get("CLAUDE_SESSION_ID", "")})
        rec = {"generated_at": stamp, "ttl_minutes": TTL_MIN, "approved": kept + fresh}
        tmp = GATE + ".tmp"
        json.dump(rec, open(tmp, "w"), ensure_ascii=False, indent=1)
        os.replace(tmp, GATE)
    finally:
        try:
            lock.close()
        except Exception:
            pass
    print(f"\n📝 {len(files)}件の本文指紋を記録しました（有効2時間）→ {GATE}")
    if kept:
        print(f"   併存：他に生きている承認記録 {len(kept)}件は消さずに残しました。")
    print("   本文を1文字でも変えたら指紋が変わり、Notion書き込みは再びdenyされます。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
