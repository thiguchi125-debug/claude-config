#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""地区版市政報告レポートの機械ゲート（chiku-report G6/G7-1）。

使い方:
  python3 check_report.py --dir <02_reportのパス> --prefix <hokuto など>
      紙面の実測（オーバーフロー・横幅・列バランス）＋QR判定を行う
  python3 check_report.py --text <_proof.txt>
      禁止表現・約束型表現のスイープ
  python3 check_report.py --map <地図PNG> --map-mm 56
      地図ラベルの紙面実寸pt判定（make_map.py の出力値と突合する補助）

目視で「収まっている」と判断しない。ここを通ってから安全ゲートへ。
"""
import argparse, os, re, subprocess, sys, json

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# ---------------------------------------------------------------- 紙面実測
MEASURE_JS = """
<script>
window.addEventListener('load',function(){
 var page=document.querySelector('.page');
 if(!page){var d=document.createElement('div');d.id='_M_';d.textContent='ERR:.pageなし';document.body.appendChild(d);return;}
 var pr=page.getBoundingClientRect(), mm=pr.height/303, pl=pr.left;
 var foot=document.querySelector('.foot');
 var footTop=foot?((foot.getBoundingClientRect().top-pr.top)/mm):null;
 var prof=document.querySelector('.prof');
 var profTop=prof?((prof.getBoundingClientRect().top-pr.top)/mm):null;
 var profBottom=prof?((prof.getBoundingClientRect().bottom-pr.top)/mm):null;
 var last=null, lastB=0;
 document.querySelectorAll('.page > div').forEach(function(el){
   if(el.classList.contains('foot')||el.classList.contains('prof')||el.classList.contains('echo'))return;
   var b=(el.getBoundingClientRect().bottom-pr.top)/mm;
   if(b>lastB){lastB=b;last=el.className;}
 });
 var edges=[];
 document.querySelectorAll('.page > div, .leftcol, .side').forEach(function(el){
   var r=el.getBoundingClientRect();
   edges.push({cls:(el.className||'?').split(' ')[0],
               l:+(((r.left-pl)/mm).toFixed(1)), r:+(((r.right-pl)/mm).toFixed(1)),
               h:+((r.height/mm).toFixed(1))});
 });
 var d=document.createElement('div'); d.id='_M_';
 d.textContent=JSON.stringify({lastBlock:last,lastBottom:+lastB.toFixed(1),
   footTop:footTop!==null?+footTop.toFixed(1):null,
   profTop:profTop!==null?+profTop.toFixed(1):null,
   profBottom:profBottom!==null?+profBottom.toFixed(1):null, edges:edges});
 document.body.appendChild(d);
});
</script>
"""

def measure(path):
    path = os.path.abspath(path)
    html = open(path, encoding="utf-8").read().replace("</body>", MEASURE_JS + "</body>")
    tmp = path + ".measure.html"
    open(tmp, "w", encoding="utf-8").write(html)
    dom = subprocess.run([CHROME, "--headless", "--disable-gpu", "--virtual-time-budget=6000",
                          "--window-size=816,1145", "--dump-dom", f"file://{tmp}"],
                         capture_output=True, text=True).stdout
    os.remove(tmp)
    m = re.search(r'id="_M_">(.*?)</div>', dom, re.S)
    if not m:
        return None
    import html as H
    return json.loads(H.unescape(m.group(1)))

def gate_layout(d, prefix):
    ng = []
    for side in ("omote", "ura"):
        f = os.path.abspath(os.path.join(d, f"{prefix}_{side}_final.html"))
        if not os.path.exists(f):
            print(f"  [{side}] final HTML なし（build.py を先に流す）"); ng.append(side); continue
        r = measure(f)
        if not r:
            print(f"  [{side}] 測定失敗"); ng.append(side); continue
        # 1) 下端の余裕
        limit = min(x for x in (r["footTop"], r["profTop"]) if x is not None)
        slack = limit - r["lastBottom"]
        ok1 = slack >= 3.0
        print(f"  [{side}] 下端余裕 {slack:.1f}mm （最終={r['lastBlock']} {r['lastBottom']}mm ／ 下限={limit}mm） {'OK' if ok1 else 'NG(3mm以上必要)'}")
        # 1-b) プロフィール帯とフッターの干渉
        if r.get("profBottom") is not None and r["footTop"] is not None:
            gap = r["footTop"] - r["profBottom"]
            okp = gap >= 1.5
            print(f"  [{side}] プロフィール下端→フッター {gap:.1f}mm {'OK' if okp else 'NG(1.5mm以上必要)'}")
            if not okp:
                ng.append(side)
        # 2) 右端の一致
        rights = [e["r"] for e in r["edges"] if e["cls"] not in ("leftcol",)]
        ref = max(set(rights), key=rights.count)
        # 内側に収まっているのは問題なし。右へ超過したものだけをNGにする
        outliers = [e for e in r["edges"] if e["cls"] not in ("leftcol",) and (e["r"] - ref) > 0.6]
        ok2 = not outliers
        print(f"  [{side}] 右端 基準{ref}mm / はみ出し {len(outliers)}件 {'OK' if ok2 else 'NG'}")
        for e in outliers:
            print(f"        - .{e['cls']} 右端 {e['r']}mm（基準を {e['r']-ref:.1f}mm 超過）")
        # 3) 2段組バランス
        cols = {e["cls"]: e["h"] for e in r["edges"] if e["cls"] in ("leftcol", "side")}
        ok3 = True
        if len(cols) == 2:
            diff = abs(cols["leftcol"] - cols["side"])
            ok3 = diff <= 10.0
            print(f"  [{side}] 段バランス 左{cols['leftcol']}mm / 右{cols['side']}mm 差{diff:.1f}mm {'OK' if ok3 else 'NG(10mm以内)'}")
        if not (ok1 and ok2 and ok3):
            ng.append(side)
    return ng

# ---------------------------------------------------------------- QR
def gate_qr(d, prefix):
    try:
        from pyzbar.pyzbar import decode as zdecode
        from PIL import Image
    except ImportError:
        print("  pyzbar/PIL 未導入。pip install pyzbar pillow"); return ["qr"]
    ng = []
    for side in ("omote", "ura"):
        f = os.path.abspath(os.path.join(d, f"{prefix}_{side}_final.html"))
        if not os.path.exists(f):
            continue
        png = os.path.abspath(os.path.join(d, f"_qrchk_{side}.png"))
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--force-device-scale-factor=3",
                        "--window-size=816,1145", f"--screenshot={png}", "--hide-scrollbars",
                        f"file://{f}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        im = Image.open(png)
        w200 = int(216 / 25.4 * 200)          # 200dpi相当まで落として判定する
        small = im.resize((w200, int(im.size[1] * w200 / im.size[0])), Image.LANCZOS)
        urls = sorted({r.data.decode() for r in zdecode(small)})
        print(f"  [{side}] 200dpi相当デコード {len(urls)}件")
        for u in urls:
            print(f"        -> {u}")
        if len(urls) < 3:
            print(f"        NG: 3種そろっていない。URLを短縮するか寸法を上げる")
            ng.append(side)
        os.remove(png)
    return ng

# ---------------------------------------------------------------- 禁止表現
PROMISE = [
    (r"(報告会で|会場で|議会で)[^。]{0,20}(お伝えします|報告します|お話しします)", "約束型（履行が保証されない）"),
    (r"(議会で|本会議で|委員会で)[^。]{0,15}(取り上げます|質問します|問います|確かめます|求めます)", "約束型（議会での行動の言い切り）"),
    (r"求め(続けます|てまいります|ていきます)", "約束型（継続の言い切り）"),
    (r"(実現|整備|導入|設置)し(ます|てまいります|ていきます)", "約束型（実現の言い切り）"),
    (r"(必ず|きっと|絶対に)[^。]{0,20}します", "約束型（強い断定）"),
    (r"私が[^。]{0,20}(変えます|動かします|止めます)", "約束型（一人称の断定）"),
]
BANNED = [
    (r"[\U0001F300-\U0001FAFF☀-➿]", "絵文字"),
    (r"届かないを終わらせる", "禁止フレーズ"),
    (r"届かなくても届く", "禁止フレーズ"),
    (r"次の議会で(追及|問いただ)", "対決動詞（禁止）"),
    (r"生物多様性・獣害対策室", "所管名の誤り（正＝環境課 生物多様性・獣害対策グループ）"),
    (r"令和12年度.*開庁", "新庁舎の旧計画（正＝令和18年度）"),
]

def gate_text(path):
    txt = open(path, encoding="utf-8").read()
    lines = txt.split("\n")
    hits = []
    for i, l in enumerate(lines, 1):
        s = l.strip()
        if not s:
            continue
        for pat, why in BANNED:
            if re.search(pat, s):
                hits.append(("BANNED", i, why, s))
        for pat, why in PROMISE:
            if re.search(pat, s):
                hits.append(("PROMISE", i, why, s))
    if not hits:
        print("  禁止表現・約束型表現: 検出なし OK")
        return []
    for kind, i, why, s in hits:
        mark = "🚫" if kind == "BANNED" else "⚠️"
        print(f"  {mark} L{i} [{why}] {s[:70]}")
    print("\n  ※ PROMISE は文脈次第。草川の将来の行動を言い切っていれば「〜したい」へ、"
          "事実・数字の断定なら残してよい（[[feedback_sns_no_action_promise_assertions]]）")
    return [h for h in hits if h[0] == "BANNED"]

# ---------------------------------------------------------------- 地図
def gate_map(png, mm):
    from PIL import Image
    im = Image.open(png)
    print(f"  地図 {im.size[0]}x{im.size[1]}px を {mm}mm 幅で配置 → {im.size[0]/mm*25.4:.0f}dpi")
    print(f"  主ラベル7pt = {7*25.4/72:.2f}mm = 画素で {7*25.4/72*im.size[0]/mm:.0f}px 以上必要")
    print(f"  副ラベル6pt = {6*25.4/72:.2f}mm = 画素で {6*25.4/72*im.size[0]/mm:.0f}px 以上必要")
    print("  → make_map.py の出力値と突合すること")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir"); ap.add_argument("--prefix")
    ap.add_argument("--text"); ap.add_argument("--map"); ap.add_argument("--map-mm", type=float, default=56.0)
    a = ap.parse_args()
    ng = []
    if a.dir and a.prefix:
        print("■ 紙面実測（G6）"); ng += gate_layout(a.dir, a.prefix)
        print("\n■ QR（G6）");     ng += gate_qr(a.dir, a.prefix)
    if a.text:
        print("\n■ 禁止・約束型表現（G7-1）"); ng += gate_text(a.text)
    if a.map:
        print("\n■ 地図ラベル（G6）"); gate_map(a.map, a.map_mm)
    print("\n判定:", "NG（要修正）" if ng else "OK")
    sys.exit(1 if ng else 0)

if __name__ == "__main__":
    main()
