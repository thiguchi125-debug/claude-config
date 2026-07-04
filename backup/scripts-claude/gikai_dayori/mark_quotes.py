#!/usr/bin/env python3
"""議会だより 引用参照マーク生成スクリプト（汎用版）

会議録docxに対し、議会だより原稿で引用した箇所を色付けした「引用参照マーク」docxを生成する。
- 赤（C00000）= 草川発言からの引用元
- 青（0033CC）= 執行部答弁からの引用元
編集委員会が「原稿が会議録のどこに基づくか」を照合するための成果物。

使い方:
    python3 mark_quotes.py config.json

config.json の形式:
{
  "src": "/Users/.../【会議録】一般質問◯月◯日.docx",
  "out": "/Users/.../【会議録】一般質問◯月◯日_引用参照マーク.docx",
  "red_quotes":  ["原稿のQ1本文", "原稿のQ2本文", ...],   // 草川発言由来（要約後の文言でOK・fuzzyマッチ）
  "blue_quotes": ["原稿のA1本文", "原稿のA2本文", ...],   // 執行部答弁由来
  "region_start": "対象範囲の開始を示す会議録内の一意な文字列（省略時=文書全体）",
  "region_end":   "対象範囲の終了を示す一意な文字列（省略可）",
  "questioner_name": "草川卓也"   // 省略時デフォルト
}

アルゴリズム（2026-07-02 R7.6月議会で実証済みのパラメータ）:
  A. SequenceMatcher整列（MIN_BLOCK=4字以上の一致）＋BRIDGE=5字以内の言い換え橋渡し
  B. 語順入替に強いgreedy完全一致（GREEDY_TH=6字以上）
  仕上げ: 句読点trim・実質MIN_RUN=5字未満の断片除去・STRONG=5字以上の核を含む連続のみ残す
"""
import sys, json, zipfile, copy
from lxml import etree
from difflib import SequenceMatcher

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML = "http://www.w3.org/XML/1998/namespace"
def w(tag): return "{%s}%s" % (W, tag)

# 全角ASCII/数字/空白を半角へ（厳密1:1・indexずれなし）
TBL = {0xFF01 + i: 0x21 + i for i in range(0x5E)}
TBL[0x3000] = 0x20
def norm(s): return s.translate(TBL)

PUNCT = set("。、，．・「」『』（）()：；　 ー―…　")
RED = "C00000"
BLUE = "0033CC"
MIN_BLOCK = 4      # SequenceMatcher最小一致
BRIDGE = 5         # 一致同士の間の言い換えを橋渡しする最大字数
GREEDY_TH = 6      # 語順入替の完全一致を拾う
MIN_RUN = 5        # 最終的な色付け連続の最小実質字数
STRONG = 5         # この長さ以上の確一致を「核」とし、核を含む連続だけ残す

# 執行部側の登壇者を示す肩書き
EXEC_TITLES = ["市長", "部長", "参事", "教育長", "副市長", "理事", "統括官", "署長"]


def greedy(Pn, ref, th):
    m = [False]*len(Pn); i = 0
    while i < len(Pn):
        best = 0; L = 1
        while i+L <= len(Pn) and Pn[i:i+L] in ref:
            best = L; L += 1
        if best >= th:
            for k in range(i, i+best): m[k] = True
            i += best
        else:
            i += 1
    return m


def bridge(m, maxgap):
    n = len(m); i = 0; prev_end = None
    while i < n:
        if m[i]:
            j = i
            while j < n and m[j]:
                j += 1
            if prev_end is not None and (i - prev_end) <= maxgap:
                for k in range(prev_end, i):
                    m[k] = True
            prev_end = j; i = j
        else:
            i += 1
    return m


def build_mask(P, ref):
    Pn = norm(P)
    # A: SequenceMatcher整列＋橋渡し
    mA = [False]*len(P)
    strong = [False]*len(P)
    sm = SequenceMatcher(None, Pn, ref, autojunk=False)
    for b in sm.get_matching_blocks():
        if b.size >= MIN_BLOCK:
            for k in range(b.a, b.a + b.size):
                mA[k] = True
        if b.size >= STRONG:
            for k in range(b.a, b.a + b.size):
                strong[k] = True
    bridge(mA, BRIDGE)
    # B: 語順入替の完全一致（これも核とみなす）
    mB = greedy(Pn, ref, GREEDY_TH)
    for k, v in enumerate(mB):
        if v: strong[k] = True
    m = [a or b for a, b in zip(mA, mB)]
    # 前後句読点trim＋実質MIN_RUN未満は落とす
    n = len(P); j = 0
    while j < n:
        if not m[j]:
            j += 1; continue
        k = j
        while k < n and m[k]:
            k += 1
        a, b = j, k
        while a < b and P[a] in PUNCT:
            a += 1
        while b > a and P[b-1] in PUNCT:
            b -= 1
        core = sum(1 for x in range(a, b) if P[x] not in PUNCT)
        has_strong = any(strong[x] for x in range(j, k))
        if core < MIN_RUN or not has_strong:
            for x in range(j, k): m[x] = False
        else:
            for x in range(j, a): m[x] = False
            for x in range(b, k): m[x] = False
        j = k
    return m


def para_text(p): return "".join(t.text or "" for t in p.iter(w("t")))


def first_rpr(p):
    r = p.find(w("r"))
    if r is not None:
        rpr = r.find(w("rPr"))
        if rpr is not None:
            return copy.deepcopy(rpr)
    return None


def recolor(p, mask, hexcolor):
    text = para_text(p)
    base = first_rpr(p)
    for r in p.findall(w("r")):
        p.remove(r)
    ppr = p.find(w("pPr"))
    idx = (list(p).index(ppr) + 1) if ppr is not None else 0
    segs = []; cur = ""; flag = None
    for ch, f in zip(text, mask):
        if flag is None:
            cur, flag = ch, f
        elif f == flag:
            cur += ch
        else:
            segs.append((cur, flag)); cur, flag = ch, f
    if cur:
        segs.append((cur, flag))
    for s, f in segs:
        r = etree.Element(w("r"))
        rpr = copy.deepcopy(base) if base is not None else etree.Element(w("rPr"))
        r.append(rpr)
        if f:
            for old in rpr.findall(w("color")):
                rpr.remove(old)
            col = etree.SubElement(rpr, w("color")); col.set(w("val"), hexcolor)
            if rpr.find(w("b")) is None:
                etree.SubElement(rpr, w("b"))
        t = etree.SubElement(r, w("t")); t.set("{%s}space" % XML, "preserve"); t.text = s
        p.insert(idx, r); idx += 1


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        cfg = json.load(f)

    SRC = cfg["src"]
    OUT = cfg["out"]
    RED_REF = norm("".join(cfg["red_quotes"]))
    BLUE_REF = norm("".join(cfg["blue_quotes"]))
    region_start = cfg.get("region_start")
    region_end = cfg.get("region_end")
    qname = cfg.get("questioner_name", "草川卓也")

    with zipfile.ZipFile(SRC) as z:
        names = z.namelist()
        data = {n: z.read(n) for n in names}
    DOCKEY = next(n for n in names if n.replace("\\", "/").endswith("word/document.xml"))
    root = etree.fromstring(data[DOCKEY])

    kus = False; exe = False
    region = region_start is None  # region_start省略時は全体対象
    red_hits = []; blue_hits = []
    for p in list(root.iter(w("p"))):
        t = para_text(p); ts = t.strip()
        # ○◯◯君登壇 の話者切替行
        if ts.startswith("○"):
            if (qname + "君登壇") in ts.replace("　", "").replace(" ", ""):
                kus, exe = True, False
            elif ("登壇" in ts) and any(x in ts for x in EXEC_TITLES):
                kus, exe = False, True
            continue
        # 「◯◯部長。」等の指名だけの短い行はスキップ
        if ts.endswith("。") and len(ts) < 12 and any(x in ts for x in EXEC_TITLES + ["議員"]):
            continue
        if (not region) and region_start and (region_start in t):
            region = True
        if region:
            spk = "K" if kus else ("E" if exe else None)
            if spk:
                ref = RED_REF if spk == "K" else BLUE_REF
                m = build_mask(t, ref)
                if any(m):
                    segs = []; cur = ""
                    for ch, f in zip(t, m):
                        if f: cur += ch
                        elif cur: segs.append(cur); cur = ""
                    if cur: segs.append(cur)
                    (red_hits if spk == "K" else blue_hits).append(segs)
                    recolor(p, m, RED if spk == "K" else BLUE)
            if region_end and (region_end in t):
                region = False

    data[DOCKEY] = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            z.writestr(n, data[n])

    print("=== 赤（%s発言） ===" % qname)
    for h in red_hits:
        print("  ", " ／ ".join(h))
    print("=== 青（執行部答弁） ===")
    for h in blue_hits:
        print("  ", " ／ ".join(h))
    print("saved:", OUT)
    if not red_hits or not blue_hits:
        print("⚠️ 赤または青のマークが0件。region_start/quotesを確認してください。")


if __name__ == "__main__":
    main()
