#!/usr/bin/env python3
"""質問シート md → A4縦PDF（議場の机上用）。使い方: sheet_to_pdf.py <in.md> [out.pdf]
 - ==…== を <mark> に（答弁を求める質問文＝黄色ハイライト）
 - ### 🗣 / 📊 / 💬 / ⚠️ / 🎤 の見出しごとにブロックを div で包み、役割別に見え方を変える
 - # パート見出しと ## 問見出しで改ページ（1問＝1ページで繰れる）
"""
import sys, re, subprocess, pathlib, tempfile, markdown, html as _html

src = pathlib.Path(sys.argv[1]).expanduser().resolve()
out = pathlib.Path(sys.argv[2]).expanduser().resolve() if len(sys.argv) > 2 else src.with_suffix('.pdf')
text = src.read_text(encoding='utf-8')

# ==…== → <mark>（行内・複数行はまたがせない）
text = re.sub(r'==(.+?)==', lambda m: '<mark>' + m.group(1) + '</mark>', text, flags=re.S)

body = markdown.markdown(text, extensions=['tables', 'fenced_code', 'sane_lists'])

# ### 見出しの絵文字で後続ブロックを包む
ROLE = {'🗣': 'say', '📊': 'data', '💬': 'reply', '⚠️': 'warn', '🎤': 'aim', '🔒': 'hidden'}
parts = re.split(r'(<h[1-3][^>]*>.*?</h[1-3]>)', body, flags=re.S)
buf, open_div = [], False
just_h1 = False  # 直前がパート見出しで、間に中身が無い＝ここで改ページしない
for p in parts:
    m = re.match(r'<h([1-3])[^>]*>(.*?)</h\1>', p, flags=re.S)
    if m:
        if open_div:
            buf.append('</div>'); open_div = False
        level, title = m.group(1), re.sub(r'<[^>]+>', '', m.group(2))
        cls = next((v for k, v in ROLE.items() if k in title), None)
        # パート見出し直後の最初の問は、パート見出しと同じページに載せる
        is_q = (level == '2' and ('問' in title or '伏せ札' in title))
        brk = ' class="brk"' if (is_q and not just_h1) else ''
        buf.append(f'<h{level}{brk}>{m.group(2)}</h{level}>')
        if level == '1':
            just_h1 = True
        elif is_q:
            just_h1 = False
        if cls:
            buf.append(f'<div class="blk {cls}">'); open_div = True
    else:
        buf.append(p)
if open_div:
    buf.append('</div>')
body = ''.join(buf)

css = """
@page{size:A4;margin:12mm 12mm 14mm}
body{font-family:"Hiragino Sans","Hiragino Kaku Gothic ProN",sans-serif;font-size:11pt;line-height:1.7;color:#111}
h1{font-size:15pt;background:#123;color:#fff;padding:4px 8px;margin:0 0 8px;border-radius:2px}
h1.brk,h2.brk{page-break-before:always}
h1:first-of-type{page-break-before:avoid}
h2{font-size:13.5pt;border-left:7px solid #123;padding:2px 0 2px 8px;margin:14px 0 6px}
h3{font-size:11.5pt;margin:10px 0 3px;color:#333}
p{margin:4px 0}li{margin:2px 0}
mark{background:#ffe95c;padding:1px 2px;font-weight:700;box-shadow:0 1px 0 #caa400}
blockquote{margin:5px 0 5px 4px;padding:4px 10px;border-left:4px solid #bbb}
table{border-collapse:collapse;font-size:9.5pt;margin:4px 0}
td,th{border:1px solid #999;padding:2px 5px;vertical-align:top}
th{background:#eee}
strong{color:#8a0000}
/* 役割別 */
.blk{page-break-inside:auto}
.say{font-size:13pt;line-height:1.85;background:#fffdf2;border:1.5px solid #e2c94a;border-radius:3px;padding:6px 10px}
.say blockquote{border-left:4px solid #e2c94a;margin-left:0}
.aim{font-size:12.5pt;background:#f2f7ff;border:1.5px solid #9bb8e0;border-radius:3px;padding:5px 10px}
.aim blockquote{border-left:4px solid #9bb8e0;margin-left:0}
.reply{font-size:11pt;background:#f7f7f7;border-left:4px solid #888;padding:5px 10px}
.data{font-size:9.5pt;color:#222}
.warn{font-size:10pt;background:#fff4f4;border-left:4px solid #c33;padding:4px 10px}
.hidden{font-size:10pt;background:#f4f4ef;border:1px dashed #999;padding:5px 10px}
"""
html = ('<!doctype html><meta charset="utf-8"><style>' + css + '</style><body>' + body + '</body>')
tmp = pathlib.Path(tempfile.mkdtemp()) / 'sheet.html'
tmp.write_text(html, encoding='utf-8')
subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--headless=new',
                '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={out}', f'file://{tmp}'],
               check=True, capture_output=True)
print(out)
