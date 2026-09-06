#!/usr/bin/env python3
"""md → A4縦PDF（Chrome headless）。使い方: md_to_pdf.py <in.md> [out.pdf]。`<div style="page-break-after:always">` で改ページ。"""
import sys, subprocess, pathlib, markdown, tempfile
src = pathlib.Path(sys.argv[1]).expanduser().resolve()
out = pathlib.Path(sys.argv[2]).expanduser().resolve() if len(sys.argv) > 2 else src.with_suffix('.pdf')
body = markdown.markdown(src.read_text(encoding='utf-8'), extensions=['tables', 'fenced_code'])
css = """@page{size:A4;margin:14mm 14mm}body{font-family:"Hiragino Sans","Hiragino Kaku Gothic ProN",sans-serif;font-size:10.5pt;line-height:1.55;color:#111}
h1{font-size:15pt;border-bottom:2px solid #333;padding-bottom:2px;margin:0 0 6px}h2{font-size:12pt;background:#eee;padding:2px 6px;margin:10px 0 4px}
blockquote{margin:4px 0 4px 8px;padding:2px 8px;border-left:4px solid #2a7;font-size:11pt}table{border-collapse:collapse;font-size:9.5pt}td,th{border:1px solid #999;padding:2px 5px;vertical-align:top}
li{margin:1px 0}p{margin:3px 0}strong{color:#900}"""
html = f'<!doctype html><meta charset="utf-8"><style>{css}</style><body>{body}</body>'
tmp = pathlib.Path(tempfile.mkdtemp()) / 'doc.html'; tmp.write_text(html, encoding='utf-8')
subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--no-pdf-header-footer',f'--print-to-pdf={out}',f'file://{tmp}'],check=True,capture_output=True)
print(out)
