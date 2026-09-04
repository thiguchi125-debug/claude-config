#!/usr/bin/env python3
"""
はみ出し検出ゲート（Chrome headless に実測させる）

「文字サイズと枠幅を、実際の描画幅を測らずに決める」ことによる版ズレを潰す。
目視やピクセル勘に頼らず、ブラウザのレイアウト結果（getBoundingClientRect /
scrollWidth）を直接読む。

検出するもの:
  1. キャンバス外への飛び出し（left<0 / right>1080 / bottom>1920）
  2. 親要素からの水平はみ出し（scrollWidth > clientWidth）
  3. 兄弟要素どうしの重なり（絶対配置カード同士の衝突）
  4. 折り返しで1〜2文字だけ残る孤立行（確定仕様「孤立文字ゼロ」）

使い方:
  python3 check_overflow.py <page.html> [...]
終了コード: 全PASSなら0、1件でもFAILなら1

2026-08-06 追加の理由:
  a4a の値列を196pxに固定したが「90.5%」は66pxで約330px必要で右端が欠けた。
  a4b の kicker は48px×21字＋余白で1090px＝画面幅超過。いずれも描画前に
  数値を決め、レンダ後に測らなかったことが原因。
"""
import sys, os, json, re, subprocess, tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# 既定は9:16のショート動画挿入画像。横型サムネ（1600x900・1200x630）等は
# --canvas 1600x900 で上書きする。2026-09-04まで1080x1920固定だったため、
# 横型ページを1080幅でレンダして「右端超過」を全要素に出す偽陽性が起きていた。
W, H = 1080, 1920
for _i, _a in enumerate(sys.argv):
    if _a == "--canvas" and _i + 1 < len(sys.argv):
        try:
            W, H = (int(x) for x in sys.argv[_i + 1].lower().split("x"))
        except ValueError:
            sys.exit("--canvas は 1600x900 の形式で指定してください")
        del sys.argv[_i:_i + 2]
        break

PROBE = """
<script>
window.addEventListener('load', function(){
  var out = [], W=%d, H=%d;
  var els = Array.from(document.querySelectorAll('body *'))
    .filter(function(e){ return e.tagName!=='SCRIPT' && e.tagName!=='STYLE'
                         && !(e.tagName==='svg'||e.closest('svg')); });
  els.forEach(function(e){
    var r = e.getBoundingClientRect();
    if (r.width===0 || r.height===0) return;
    var tag = e.className ? (e.tagName.toLowerCase()+'.'+String(e.className).trim().split(/\\s+/).join('.'))
                          : e.tagName.toLowerCase();
    var txt = (e.textContent||'').trim().slice(0,24);
    if (r.left < -1 || r.right > W+1)
      out.push({t:'canvas-x', el:tag, txt:txt, left:Math.round(r.left), right:Math.round(r.right)});
    if (r.bottom > H+1)
      out.push({t:'canvas-y', el:tag, txt:txt, bottom:Math.round(r.bottom)});
    if (e.scrollWidth > e.clientWidth + 1 && e.clientWidth > 0)
      out.push({t:'overflow-x', el:tag, txt:txt, need:e.scrollWidth, have:e.clientWidth});
  });
  // 絶対配置ブロック同士の重なり
  var abs = els.filter(function(e){ return getComputedStyle(e).position==='absolute'; });
  for (var i=0;i<abs.length;i++) for (var j=i+1;j<abs.length;j++){
    if (abs[i].contains(abs[j]) || abs[j].contains(abs[i])) continue;
    var a=abs[i].getBoundingClientRect(), b=abs[j].getBoundingClientRect();
    var ox=Math.min(a.right,b.right)-Math.max(a.left,b.left);
    var oy=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);
    if (ox>4 && oy>4) out.push({t:'overlap',
      el:(abs[i].className||abs[i].tagName)+' × '+(abs[j].className||abs[j].tagName),
      txt:'', h:Math.round(oy)});
  }
  // 孤立行（最終行が1〜2文字）
  els.forEach(function(e){
    var kids=Array.from(e.children);
    if (kids.some(function(k){return !['BR','SPAN','B','I','EM','STRONG'].includes(k.tagName);})) return;
    var s=(e.textContent||'').trim(); if (s.length<6) return;
    var r=e.getBoundingClientRect();
    var lh=parseFloat(getComputedStyle(e).lineHeight)||parseFloat(getComputedStyle(e).fontSize)*1.2;
    var lines=Math.round(r.height/lh); if (lines<2) return;
    var rng=document.createRange(); rng.selectNodeContents(e);
    var rects=Array.from(rng.getClientRects());
    // インラインspanがあると1行が複数rectに割れるので、top座標で行にまとめる
    var byLine={};
    rects.forEach(function(r){ var k=Math.round(r.top/4);
      byLine[k]=(byLine[k]||0)+r.width; });
    var keys=Object.keys(byLine).map(Number).sort(function(a,b){return a-b;});
    if (keys.length>=2){
      var lastw=byLine[keys[keys.length-1]];
      var fs=parseFloat(getComputedStyle(e).fontSize);
      if (lastw < fs*2.5)
        out.push({t:'orphan', el:(e.className||e.tagName), txt:s.slice(-10),
                  lastw:Math.round(lastw), fs:Math.round(fs)});
    }
  });
  var d=document.createElement('div'); d.id='__probe__';
  d.textContent = JSON.stringify(out);
  document.body.appendChild(d);
});
</script>
""" % (W, H)

LABEL = {
    "canvas-x": "画面の左右にはみ出し",
    "canvas-y": "画面の下にはみ出し",
    "overflow-x": "枠より文字が広い",
    "overlap": "要素どうしが重なっている",
    "orphan": "孤立行（最終行が短すぎる）",
}

def probe(path):
    src = open(path, encoding="utf-8").read()
    if "</body>" in src:
        src = src.replace("</body>", PROBE + "</body>")
    else:
        src += PROBE
    d = tempfile.mkdtemp()
    tmp = os.path.join(d, os.path.basename(path))
    open(tmp, "w", encoding="utf-8").write(src)
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--window-size={W},{H}", "--virtual-time-budget=3000",
                        "--dump-dom", "file://" + tmp],
                       capture_output=True, text=True, timeout=90)
    m = re.search(r'id="__probe__">(.*?)</div>', r.stdout, re.S)
    if not m:
        return None
    return json.loads(m.group(1) or "[]")

def main(argv):
    if not argv:
        print("usage: check_overflow.py <page.html> ..."); return 1
    fail = 0
    for f in argv:
        print(f"\n== {os.path.basename(f)} ==")
        res = probe(f)
        if res is None:
            print("  ⚠ 計測できませんでした"); continue
        if not res:
            print("  ✅ はみ出し・重なり・孤立行なし"); continue
        for x in res:
            fail += 1
            detail = " ".join(f"{k}={v}" for k, v in x.items() if k not in ("t", "el", "txt"))
            print(f"  🚨 {LABEL.get(x['t'], x['t'])}: {x['el']}"
                  + (f" 「{x['txt']}」" if x.get('txt') else "") + f"  {detail}")
    print(f"\n-- 違反 {fail}件 --")
    return 1 if fail else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
