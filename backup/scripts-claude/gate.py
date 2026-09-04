#!/usr/bin/env python3
"""
発信物の安全ゲート実行＆記録（1コマンドに集約）

  python3 ~/.claude/scripts/gate.py <file...> [--pass]

ファイルは .md（ブログ/SNS/動画原稿）でも .html（挿入画像）でもよい。

やること:
  1. 種類に応じて機械チェックを全部回す
       .md   → check_content_limits.py
       .html → 判型（9:16 / 16:9 / 1:1）を自動判定し、その判型の規範で
               check_image_design.py / check_overflow.py を回す。
               字幕セーフ帯ゲートは 9:16(1080x1920) のときだけ。
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
import sys as _sys, os as _os; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import specs as _specs   # 規格値の正本 specs.json（2026-09-05）

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


def canvas_of(html_path):
    """画像HTMLのキャンバス実寸を (W, H) で返す。

    2026-09-04まで判型を見ず、すべて 9:16（1080x1920・ショート動画の挿入画像）として
    チェッカーを回していた。そのため 16:9 のアイキャッチに 1080幅でレンダした
    「右端はみ出し」の偽陽性と、ショート動画専用の字幕セーフ帯ゲートが当たっていた。

    判定の順序（確かな順）:
      1. 同名 .png の実寸（レンダ結果そのもの）
      2. HTML の html/body/.stage/.canvas/.frame に書かれた width/height の組
      3. どちらも取れなければ 9:16 とみなす（従来の既定）
    """
    png = os.path.splitext(html_path)[0] + ".png"
    if os.path.exists(png):
        try:
            from PIL import Image
            return Image.open(png).size
        except Exception:
            pass
    try:
        css = open(html_path, encoding="utf-8").read()
        css = css[:css.index("</style>")] if "</style>" in css else css
    except Exception:
        return _specs.dims("9:16")
    for sel in ("html, body", "html,body", "body", ".stage", ".canvas", ".frame", ".page"):
        for rule in re.findall(re.escape(sel) + r"\s*\{([^}]*)\}", css):
            w = re.search(r"\bwidth\s*:\s*(\d+)px", rule)
            h = re.search(r"\bheight\s*:\s*(\d+)px", rule)
            if w and h:
                return (int(w.group(1)), int(h.group(1)))
    return _specs.dims("9:16")


def fmt_of(w, h):
    r = w / h if h else 1
    return "16:9" if r > 1.25 else ("9:16" if r < 0.8 else "1:1")


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
        # 判型ごとにまとめて回す（2026-09-04）。混在していても取り違えない。
        groups = {}
        for h in htmls:
            w, ht = canvas_of(h)
            groups.setdefault((w, ht), []).append(h)
        for (w, ht), fs in sorted(groups.items()):
            f9 = fmt_of(w, ht)
            print(f"\n▼ 判型 {f9}（{w}x{ht}）: " + ", ".join(os.path.basename(x) for x in fs))
            for script in ("check_image_design.py", "check_overflow.py"):
                c, o = run(["python3", os.path.join(SC, script), "--canvas", f"{w}x{ht}"] + fs)
                print(o); fail += (c != 0)
            pngs = [os.path.splitext(x)[0] + ".png" for x in fs
                    if os.path.exists(os.path.splitext(x)[0] + ".png")]
            if pngs and os.path.exists(BAND):
                if (w, ht) == _specs.dims("9:16"):
                    c, o = run(["python3", BAND] + pngs)
                    print(o); fail += (c != 0)
                else:
                    print("  ・字幕セーフ帯ゲートは 9:16(1080x1920) 専用のため回していません。")

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
