#!/usr/bin/env python3
"""
禁止語スイープ — 「文章からは削ったのに、画像や別ファイルに残っていた」事故を機械で潰す。

2026-08-06の実例:
  草川判断で「被災自治体の実名（宇城市・氷川町）は全媒体から削除」と決めた。
  テキスト3本は直したが、ブログ用図表 card_timeline.png には
  「震度7の宇城市 0.0%・氷川町 0.0%」が赤字で焼き込まれたまま残り、
  risk-reviewerの再確認でCRITICAL判定。人間の記憶で全アセットを追うのは不可能なので、
  削除を決めた語は台帳（*_banned.txt）に書き、機械が全ファイルを掃く。

使い方:
  python3 check_banned_terms.py <banned.txt> <file-or-dir ...>

banned.txt の書式（1行1語・タブ区切りで例外指定可）:
  宇城市
  熊本	allow:v5_FINAL|v7_FINAL     ← パスがこのパターンにマッチするファイルでは許可

掃く対象: 引数のファイル＋ディレクトリ配下の .md/.html/.txt
スキップ: パスに _backup/_removed/banned を含むもの、
          行に「【不使用」「削除」「欠番」を含む行（削除の記録自体は残してよい）

終了コード: ヒット0なら0、1件でもあれば1
"""
import sys, os, re, glob

SKIP_PATH = ("_backup", "_removed", "banned")
SKIP_LINE = ("【不使用", "削除", "欠番")
EXTS = (".md", ".html", ".txt")


def load_terms(path):
    terms = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "\t" in line:
            term, opt = line.split("\t", 1)
            m = re.search(r"allow:(\S+)", opt)
            terms.append((term.strip(), m.group(1) if m else None))
        else:
            terms.append((line, None))
    return terms


def collect(paths):
    out = []
    for p in paths:
        p = os.path.expanduser(p)
        if os.path.isdir(p):
            for f in glob.glob(os.path.join(p, "**", "*"), recursive=True):
                if f.endswith(EXTS):
                    out.append(f)
        elif os.path.isfile(p):
            out.append(p)
    return [f for f in dict.fromkeys(out)
            if not any(s in f for s in SKIP_PATH)]


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    terms = load_terms(argv[0])
    files = collect(argv[1:])
    hits = []
    for f in files:
        try:
            lines = open(f, encoding="utf-8").read().split("\n")
        except (UnicodeDecodeError, OSError):
            continue
        for term, allow in terms:
            if allow and re.search(allow, f):
                continue
            for i, line in enumerate(lines, 1):
                if term in line and not any(s in line for s in SKIP_LINE):
                    hits.append((f, i, term, line.strip()[:60]))
    print(f"== 禁止語スイープ（{len(terms)}語 × {len(files)}ファイル） ==")
    if hits:
        for f, i, term, ctx in hits:
            print(f"  🚨 {os.path.basename(f)}:{i} 「{term}」 … {ctx}")
        print(f"\n-- 違反 {len(hits)}件 — 削除を決めた語が残っています。"
              "PNGの元HTMLに残っていれば画像側も再レンダが必要 --")
        return 1
    print("  ✅ 残存なし")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
