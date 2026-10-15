#!/usr/bin/env python3
"""発信物の学習素材 供給スクリプト（2026-10-15新設）

完成した発信物（公開前の完成稿）と公開済ブログを、学習アーカイブ
~/.claude/agents/knowledge/kusagawa_archive/02_publications/ へ .txt で写す。

  drafts（既定で実行）: 3か所から各フォルダの最新版だけを拾う
    1) Obsidian vault 50_発信/
    2) Drive マイドライブ直下 *_発信一式/
    3) Drive 📱動画素材/
    ブログ本文 → blog/<日付>_<テーマ>_draft.txt
    SNS投稿文・動画台本 → sns/<日付>_<テーマ>_<SNS|台本>_<名>.txt
    最新版の決め方: 名前に final/完成 があればそれ、なければ最大の vN。
  published（--published）: go2senkyo の公開済ブログを blog/<日付>_<postid>_<題>.txt で収録
    既定は今月と先月。--since-month 2026-05 で遡り（バックフィル）。

冪等: 内容ハッシュを _sync_manifest.json に持ち、変化した時だけ書く。
削除はしない（元が消えても写しは残る）。

使い方:
  python3 publications_sync.py                 # drafts のみ
  python3 publications_sync.py --published     # drafts＋公開済ブログ（夜間はこれ）
  python3 publications_sync.py --published --since-month 2026-05
  python3 publications_sync.py --dry-run
"""
import argparse
import hashlib
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, date
from html import unescape
from pathlib import Path

HOME = Path.home()
ARCH = HOME / ".claude/agents/knowledge/kusagawa_archive/02_publications"
BLOG_DIR = ARCH / "blog"
SNS_DIR = ARCH / "sns"
MANIFEST = ARCH / "_sync_manifest.json"

VAULT = HOME / "Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVault/50_発信"
DRIVE = HOME / "Library/CloudStorage/GoogleDrive-t.higuchi125@gmail.com/マイドライブ"
VIDEO = DRIVE / "📱動画素材"

KIND_HEADER = "draft-final（公開前の完成稿）"
OPENER = "こんにちは、亀山市議会議員の草川たくやです"

# ── 除外 ──
SKIP_DIR_RE = re.compile(r"^(99_過去|_旧|_trash|\.|thumbnail$|本文画像$)")
SKIP_NAME_RE = re.compile(r"(README|gate_|辛口審査|marks|_banned|_MOVED|指示書|名簿|個人情報|後援会|連絡先|_ledger)")
SKIP_PATH_RE = re.compile(r"(00_名簿|個人情報|後援会名簿)")
TEXT_EXT = {".md", ".txt"}

SNS_RE = re.compile(r"(SNS|7PF|7種|4PF|4種|投稿文|^(threads|instagram|facebook|line|x|youtube|tiktok)(_.*)?$)", re.I)
SCRIPT_RE = re.compile(r"(台本|daihon|serifu|セリフ)")
BLOG_NAME_RE = re.compile(r"(ブログ|blog|完成)", re.I)

VER_RE = re.compile(r"[_\-\s]?v(\d+(?:\.\d+)*)", re.I)
FINAL_RE = re.compile(r"(final|完成版?(\d*))", re.I)
DATE_RE = re.compile(r"(20\d{2})[-_]?(\d{2})(?:[-_]?(\d{2}))?")


def sanitize(s: str, n: int = 30) -> str:
    s = re.sub(r"【草川たくや\s*亀山市】", "", s).strip()
    s = re.sub(r'[\s/\\:*?"<>|]+', "_", s)
    return s[:n].strip("_")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_manifest() -> dict:
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception:
        return {"files": {}}


def write_if_changed(path: Path, text: str, manifest: dict, dry: bool, key: str) -> str:
    h = sha(text)
    rel = str(path.relative_to(ARCH))
    rec = manifest["files"].get(rel)
    if rec and rec.get("hash") == h and path.exists():
        return "same"
    status = "updated" if path.exists() else "new"
    if not dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        manifest["files"][rel] = {"hash": h, "key": key, "synced_at": datetime.now().isoformat(timespec="seconds")}
    return status


# ──────────────────────────── drafts ────────────────────────────

def version_key(stem: str):
    """(final, version tuple, -len) 大きいほど新しい。"""
    is_final = 1 if FINAL_RE.search(stem) else 0
    fin_n = 0
    m = FINAL_RE.search(stem)
    if m and m.group(2):
        fin_n = int(m.group(2))
    vs = VER_RE.findall(stem)
    ver = tuple(int(x) for x in vs[-1].split(".")) if vs else (0,)
    return (is_final, fin_n, ver, -len(stem))


def group_stem(stem: str) -> str:
    s = re.sub(r"^20\d{2}-\d{2}(-\d{2})?_", "", stem)
    s = re.sub(r"^\d{2}_", "", s)  # 発信一式の 01_ 等
    s = VER_RE.split(s)[0] if VER_RE.search(s) else s
    s = FINAL_RE.sub("", s)
    s = re.sub(r"(確定前|_カット表)", "", s)
    return s.strip("_ -") or "本文"


def strip_frontmatter(t: str) -> str:
    if t.startswith("---\n"):
        end = t.find("\n---", 4)
        if end != -1:
            return t[end + 4:].lstrip("\n")
    return t


def classify(name: str, text: str):
    stem = Path(name).stem
    if SCRIPT_RE.search(stem):
        return "script"
    if SNS_RE.search(stem):
        return "sns"
    if OPENER in text[:1500]:
        return "blog"
    if BLOG_NAME_RE.search(stem):
        return "blog" if OPENER in text else None
    return None


def theme_parts(rel: Path):
    """テーマフォルダ名から日付とテーマを決める。"""
    parts = [p for p in rel.parent.parts if not re.match(r"^\d{2}_(完成|SNS|ショート|ブログ)", p)]
    top = parts[0] if parts else rel.stem
    m = DATE_RE.search(top)
    d = ""
    if m:
        d = f"{m.group(1)}-{m.group(2)}" + (f"-{m.group(3)}" if m.group(3) else "")
    theme = re.sub(r"^20\d{2}-?\d{2}(-?\d{2})?_?", "", top)
    theme = re.sub(r"_発信一式$", "", theme)
    sub = [re.sub(r"^20\d{2}-\d{2}(-\d{2})?_", "", p) for p in parts[1:] if not p.startswith("_")]
    if sub:
        theme = theme + "_" + "_".join(sub)
    return d, theme


def collect_candidates():
    """(source_label, base, path) を列挙。"""
    out = []
    srcs = [("vault", VAULT)]
    if DRIVE.exists():
        srcs += [("drive発信一式", p) for p in sorted(DRIVE.glob("*_発信一式")) if p.is_dir()]
    srcs.append(("drive動画素材", VIDEO))
    for label, base in srcs:
        if not base.exists():
            print(f"  [skip] 見つからない: {base}", file=sys.stderr)
            continue
        root_for_rel = base.parent if label == "drive発信一式" else base
        for p in base.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in TEXT_EXT:
                continue
            rel = p.relative_to(root_for_rel)
            if any(SKIP_DIR_RE.search(x) for x in rel.parts[:-1]):
                continue
            if p.name.startswith("_") or p.name.startswith(".") or SKIP_NAME_RE.search(p.name) or SKIP_PATH_RE.search(str(rel)):
                continue
            out.append((label, root_for_rel, rel, p))
    return out


def load_published_index():
    """既存の公開版blog（postid付き）を (file, date, shingles) で返す。"""
    idx = []
    for f in BLOG_DIR.glob("*.txt"):
        if f.stem.endswith("_draft"):
            continue
        m = re.match(r"(\d{4}-\d{2}-\d{2})_(\d+)_", f.name)
        if not m:
            continue
        body = f.read_text(encoding="utf-8", errors="replace").split("\n---\n", 1)[-1]
        idx.append((f.name, date.fromisoformat(m.group(1)), shingles(body)))
    return idx


def shingles(t: str, n: int = 8):
    t = re.sub(r"\s+", "", t)
    t = re.sub(r"[#*>`\-|【】\[\]（）()]", "", t)
    return {t[i:i + n] for i in range(0, max(0, len(t) - n), 3)}


def match_published(body: str, d: str, pub_idx):
    sh = shingles(body)
    if not sh:
        return None
    best, score = None, 0.0
    for fname, pdate, psh in pub_idx:
        if d:
            try:
                dd = date.fromisoformat(d if len(d) == 10 else d + "-15")
                if abs((pdate - dd).days) > 45:
                    continue
            except ValueError:
                pass
        c = len(sh & psh) / len(sh)
        if c > score:
            best, score = fname, c
    return best if score >= 0.25 else None


def sync_drafts(manifest: dict, dry: bool):
    cands = collect_candidates()
    groups = {}
    for label, root, rel, p in cands:
        try:
            raw = p.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"  [read-err] {p}: {e}", file=sys.stderr)
            continue
        kind = classify(str(rel), raw)
        if not kind:
            continue
        key = (label, str(rel.parent), kind, group_stem(p.stem))
        groups.setdefault(key, []).append((version_key(p.stem), p.stat().st_mtime, rel, p, raw))

    pub_idx = load_published_index()
    seen_hash = set()
    stats = {"new": 0, "updated": 0, "same": 0, "dup": 0, "groups": len(groups)}
    used_names = {}
    for key in sorted(groups):
        label, parent, kind, gstem = key
        best = max(groups[key], key=lambda x: (x[0], x[1]))
        _, mtime, rel, p, raw = best
        body = strip_frontmatter(raw).strip() + "\n"
        h = sha(body)
        if h in seen_hash:
            stats["dup"] += 1
            continue
        seen_hash.add(h)
        d, theme = theme_parts(rel)
        if not d:
            m = DATE_RE.search(p.stem)
            d = f"{m.group(1)}-{m.group(2)}" + (f"-{m.group(3)}" if m and m.group(3) else "") if m else datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        header = [f"source: {p}", f"kind: {KIND_HEADER}", f"type: {kind}",
                  f"version_file: {p.name}", f"source_label: {label}"]
        if kind == "blog":
            pub = match_published(body, d, pub_idx)
            if pub:
                header.append(f"published_version: blog/{pub}（公開版あり＝学習は公開版を優先）")
            fname = f"{d}_{sanitize(theme, 40)}" + (f"_{sanitize(gstem, 15)}" if gstem not in ("本文", "ブログ", "blog", "完成") else "") + "_draft.txt"
            out = BLOG_DIR / fname
        else:
            tag = "台本" if kind == "script" else "SNS"
            fname = f"{d}_{sanitize(theme, 40)}_{tag}_{sanitize(gstem, 20)}.txt"
            out = SNS_DIR / fname
        # 同名衝突（別グループ）は source のハッシュで区別
        gk = "|".join(key)
        if out.name in used_names and used_names[out.name] != gk:
            out = out.with_name(out.stem + "_" + sha(gk)[:6] + out.suffix)
        used_names[out.name] = gk
        text = "---\n" + "\n".join(header) + "\n---\n\n" + body
        st = write_if_changed(out, text, manifest, dry, gk)
        stats[st] += 1
        if st != "same":
            print(f"  [{st}] {out.relative_to(ARCH)}  ← {label}:{rel}")
    return stats


# ──────────────────────────── published ────────────────────────────

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
API = "https://api.go2senkyo.com/api/posts/168135/year/{y}/month/{m}?num=50&p={p}"


def http_get(url, retries=3):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ja"})
    for a in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read().decode("utf-8", errors="replace")
        except Exception:
            if a == retries - 1:
                raise
            time.sleep(3 * (a + 1))


def months_from(since: str):
    y, m = map(int, since.split("-"))
    today = date.today()
    while (y, m) <= (today.year, today.month):
        yield y, m
        m += 1
        if m > 12:
            y, m = y + 1, 1


def sync_published(manifest: dict, dry: bool, since_month: str):
    sys.path.insert(0, str(HOME / ".claude/scripts/published-archive"))
    from scrape_full_blog import extract_post  # 既存の本文抽出ロジックを流用（形式を揃える）

    existing = {re.match(r"\d{4}-\d{2}-\d{2}_(\d+)_", f.name).group(1)
                for f in BLOG_DIR.glob("*.txt") if re.match(r"\d{4}-\d{2}-\d{2}_(\d+)_", f.name)}
    stats = {"listed": 0, "new": 0, "exists": 0, "err": 0}
    for y, m in months_from(since_month):
        p = 1
        while True:
            arr = json.loads(http_get(API.format(y=y, m=m, p=p)))
            for x in arr:
                stats["listed"] += 1
                pid = str(x["id"])
                if pid in existing:
                    stats["exists"] += 1
                    continue
                try:
                    html = http_get(f"https://go2senkyo.com/seijika/168135/posts/{pid}")
                    it = extract_post(html, pid)
                    if not it["body"]:
                        raise ValueError("body empty")
                    pub = it["published"]
                    if not pub:
                        dm = re.match(r"(\d{4})/(\d{1,2})/(\d{1,2})", x.get("published_at", ""))
                        pub = f"{int(dm.group(1)):04d}-{int(dm.group(2)):02d}-{int(dm.group(3)):02d}T00:00:00+00:00"
                    title = it["title"] or x["title"]
                    fname = f"{pub[:10]}_{pid}_{sanitize(title)}.txt"
                    text = (f"---\npost_id: {pid}\ntitle: {title}\npublished: {pub}\n"
                            f"url: https://go2senkyo.com/seijika/168135/posts/{pid}\n"
                            f"char_count: {it['char_count']}\nmedia: ブログ\n---\n\n{it['body']}\n")
                    write_if_changed(BLOG_DIR / fname, text, manifest, dry, f"go2senkyo|{pid}")
                    existing.add(pid)
                    stats["new"] += 1
                    print(f"  [published] blog/{fname}")
                    time.sleep(0.5)
                except Exception as e:
                    stats["err"] += 1
                    print(f"  [published-err] {pid}: {e}", file=sys.stderr)
            if len(arr) < 50:
                break
            p += 1
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--published", action="store_true", help="go2senkyoの公開済ブログも収録")
    ap.add_argument("--since-month", default=None, help="公開済の遡り開始 YYYY-MM（既定=先月）")
    ap.add_argument("--no-drafts", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    manifest = load_manifest()
    print(f"publications_sync {datetime.now().isoformat(timespec='seconds')}")
    if a.published:
        if a.since_month:
            since = a.since_month
        else:
            t = date.today()
            since = f"{t.year - (t.month == 1)}-{(t.month - 2) % 12 + 1:02d}"
        try:
            print("published:", sync_published(manifest, a.dry_run, since))
        except Exception as e:
            print(f"published: ERROR {e}", file=sys.stderr)
    if not a.no_drafts:
        print("drafts:", sync_drafts(manifest, a.dry_run))
    if not a.dry_run:
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
