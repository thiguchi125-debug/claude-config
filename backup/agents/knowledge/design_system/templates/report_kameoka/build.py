#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Embed data URIs, render PDF + 816x1145 preview PNG. side = omote|ura."""
import os, base64, subprocess, sys

BASE = "/Users/kusakawatakuya/.claude/projects/-Users-kusakawatakuya/drafts/2026-07-07_市政報告レポート試作"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def uri(name):
    p = os.path.join(BASE, name)
    ext = os.path.splitext(p)[1].lstrip(".").lower()
    mime = "image/jpeg" if ext in ("jpg","jpeg") else "image/png"
    with open(p,"rb") as f:
        return f"data:{mime};base64,"+base64.b64encode(f.read()).decode()

REPL = {
    "__HERO__":   lambda: uri("kameoka_hero.jpg"),
    "__DOOR__":   lambda: uri("kameoka_door.jpg"),
    "__ACCENT__": lambda: uri("kameoka_accent.jpg"),
    "__QR_IKEN__":lambda: uri("qr_iken.png"),
    "__QR_LINE__":lambda: uri("qr_line.png"),
}

def build(side):
    src = os.path.join(BASE, f"kameoka_{side}.html")
    with open(src, encoding="utf-8") as f: html = f.read()
    for k,v in REPL.items():
        if k in html: html = html.replace(k, v())
    out = os.path.join(BASE, f"kameoka_{side}_final.html")
    with open(out,"w",encoding="utf-8") as f: f.write(html)
    return out

def render(side, fh, scale="1"):
    pdf = os.path.join(BASE, f"kameoka_{side}.pdf")
    subprocess.run([CHROME,"--headless","--disable-gpu","--no-pdf-header-footer",
        f"--print-to-pdf={pdf}","--print-to-pdf-no-header",f"file://{fh}"],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    png = os.path.join(BASE, f"kameoka-{side}.png")
    subprocess.run([CHROME,"--headless","--disable-gpu",
        f"--force-device-scale-factor={scale}","--window-size=816,1145",
        f"--screenshot={png}","--hide-scrollbars",f"file://{fh}"],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return pdf, png

def overflow(fh):
    js = os.path.join(BASE,"_ovf.html")
    out = subprocess.run([CHROME,"--headless","--disable-gpu","--window-size=816,1145",
        "--dump-dom",f"file://{fh}"], capture_output=True, text=True).stdout
    return None  # placeholder; measured separately

if __name__=="__main__":
    sides = [a for a in sys.argv[1:] if not a.startswith("-")] or ["omote","ura"]
    scale = "1"
    if "--scale" in sys.argv: scale = sys.argv[sys.argv.index("--scale")+1]
    for s in sides:
        fh = build(s); pdf,png = render(s,fh,scale)
        print(f"{s}: pdf={os.path.basename(pdf)} png={os.path.basename(png)} scale={scale}")
