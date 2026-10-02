"""会議録PDFに議会だよりの引用元をハイライト注釈する（赤=質問者／青=執行部）。
mark_quotes.py（docx版）のfuzzy照合をそのまま使う。会議録がPDFしか無いとき用（2026-10-02 R8.9で実証）。
usage: python3 mark_quotes_pdf.py <config.json>
config: src(会議録PDF) / out / sections[{q,a}]（提出docxと同一テキスト）/
        regions[[開始の一意文言, 終了の一意文言, ラベル], ...]（sectionsと同順）/
        extra{ラベル:[5字未満で拾われない草川側の語句]}（任意）/ questioner_name（既定 草川卓也）
"""
import fitz, json, sys, os, importlib.util
spec=importlib.util.spec_from_file_location("mq",os.path.join(os.path.dirname(os.path.abspath(__file__)),"mark_quotes.py"))
mq=importlib.util.module_from_spec(spec); spec.loader.exec_module(mq)
cfg=json.load(open(sys.argv[1]))
SRC=cfg['src']; OUT=cfg['out']
d=cfg
RED=mq.norm("".join(x['q'] for x in d['sections']))
BLUE=mq.norm("".join(x['a'] for x in d['sections']))
REGIONS=[tuple(r) for r in cfg['regions']]
doc=fitz.open(SRC)
PAGES=[doc[i] for i in range(len(doc))]
# build global line list: (page, text, chars[(c,bbox)])
lines=[]
for pno in range(len(doc)):
    rd=doc[pno].get_text("rawdict")
    for b in rd["blocks"]:
        for l in b.get("lines",[]):
            chars=[(c["c"],fitz.Rect(c["bbox"])) for s in l["spans"] for c in s["chars"]]
            if chars: lines.append((pno,"".join(c for c,_ in chars),chars))
full="".join(t for _,t,_ in lines)
# char stream
stream=[]  # (char, page, rect, lineidx)
for li,(p,t,ch) in enumerate(lines):
    for c,r in ch: stream.append((c,p,r,li))
text="".join(s[0] for s in stream)
qname=cfg.get("questioner_name","草川卓也")
EXTRA={(k,"K"):v for k,v in cfg.get("extra",{}).items()}
results={}
annots=0
for ri,(rs,re_,label) in enumerate(REGIONS):
    RED=mq.norm(d["sections"][ri]["q"]); BLUE=mq.norm(d["sections"][ri]["a"])
    a=text.find(rs); assert a>=0,rs
    b=text.find(re_,a); assert b>=0,re_; b+=len(re_)
    # speaker of region start: find last ○ line before a
    # split into turns by lines starting with ○
    turns=[]; cur=None; spk=None
    # determine initial speaker
    prev=text.rfind("○",0,a); hdr=text[prev:text.find("\n",prev) if False else prev+30]
    spk="K" if qname+"君登壇" in hdr.replace(" ","").replace("　","") else ("E" if "登壇" in hdr else None)
    i=a; seg_start=a
    li_prev=None
    # iterate line by line within region
    idx=a
    turn_chars=[]
    def flush():
        if turn_chars and spk:
            P="".join(stream[k][0] for k in turn_chars)
            m=mq.build_mask(P, RED if spk=="K" else BLUE)
            # 短い数字・固有名詞（5字未満でfuzzyの足切りに掛かるもの）を完全一致で補う
            for ph in EXTRA.get((label,spk),[]):
                st=P.find(ph)
                if st>=0:
                    for j in range(st,st+len(ph)): m[j]=True
            sel=[turn_chars[j] for j,v in enumerate(m) if v]
            segs=[];curs="";last=None
            for j,v in enumerate(m):
                if v: curs+=P[j]
                elif curs: segs.append(curs);curs=""
            if curs: segs.append(curs)
            results.setdefault((label,spk),[]).extend(segs)
            return sel
        return []
    marks={"K":[], "E":[]}
    k=a
    while k<b:
        li=stream[k][3]
        lt=lines[li][1].strip()
        if lt.startswith("○"):
            marks.setdefault(spk,[]) if spk else None
            if spk: marks[spk]+=flush()
            turn_chars=[]
            h=lt.replace(" ","").replace("　","")
            if qname+"君登壇" in h: spk="K"
            elif "登壇" in h and any(x in h for x in mq.EXEC_TITLES): spk="E"
            else: spk=None
            # skip this line
            while k<b and stream[k][3]==li: k+=1
            continue
        if lt.startswith("－") and lt.endswith("－"):
            while k<b and stream[k][3]==li: k+=1
            continue
        turn_chars.append(k); k+=1
    if spk: marks[spk]+=flush()
    for s,col in (("K",(1,0.55,0.55)),("E",(0.55,0.7,1))):
        # group consecutive marked chars by line into rects
        bylinerun=[]
        for kk in sorted(marks[s]):
            p,r,li=stream[kk][1],stream[kk][2],stream[kk][3]
            if bylinerun and bylinerun[-1][0]==li and bylinerun[-1][3]==kk-1:
                bylinerun[-1][2]|=r; bylinerun[-1][3]=kk
            else: bylinerun.append([li,p,fitz.Rect(r),kk])
        for li,p,r,_ in bylinerun:
            an=PAGES[p].add_highlight_annot(r); an.set_colors(stroke=col); an.set_info(title="草川卓也 議会だより引用", content=("赤=草川発言" if s=="K" else "青=執行部答弁")); an.update(); annots+=1
        results[(label,s,"rects")]=len(bylinerun)
doc.save(OUT,garbage=3,deflate=True)
for key,v in results.items():
    if len(key)==2:
        print("==",key[0],"赤(草川)" if key[1]=="K" else "青(答弁)", "連続", len(v), "件 / 実字数", sum(len(x) for x in v))
        for x in v: print("   ",x)
    else: print("==",key,"行矩形",v)
print("annots",annots,"saved",OUT)
