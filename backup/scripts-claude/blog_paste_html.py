#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ブログ原稿(.md) → ブログ貼り付け用HTML（蛍光マーカー付き）

Notionからコピペすると `**` が生のまま入る／緑マーカーが落ちる。
ブラウザでこのHTMLを開き、指示バーの下から選択してコピーすれば、
太字・緑マーカー・見出し・リンクが書式ごとブログ編集画面に入る。

usage:
  python3 blog_paste_html.py <draft.md> --marks <marks.txt> [-o <out.html>] [--label "テーマ名 v3"]

  marks.txt = 蛍光マーカーを引く一文を1行1本（原稿の markdown 表記のまま・完全一致）。
              規則＝明るい緑1色・1章1本・全7本・「判断が変わる一文」だけ。
"""
import argparse, html, io, os, re, sys

GREEN = "#c6f8c2"          # 蛍光マーカー（明るい緑・1色のみ）
RULE_GREEN = "#7fbf8a"     # 見出し左のライムバー
URL_RE = re.compile(r'(?<![\("])(https?://[^\s<>"）」]+)')


def inline(s: str) -> str:
    """1行分のインライン変換（エスケープ → 太字 → 素のURLをリンク化）"""
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = URL_RE.sub(lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', s)
    return s


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--marks", help="蛍光マーカー対象の一文を並べたテキスト（1行1本）")
    ap.add_argument("-o", "--out")
    ap.add_argument("--label", default="", help="指示バーに出す案件名（例: 学校体育館の空調 v3）")
    a = ap.parse_args()

    md = io.open(a.draft, encoding="utf-8").read()

    marks = []
    if a.marks:
        marks = [l.rstrip("\n") for l in io.open(a.marks, encoding="utf-8") if l.strip()]

    title, body, img_slots, n_head = "", [], 0, 0
    for block in re.split(r"\n\s*\n", md.strip()):
        block = block.strip()
        if not block:
            continue
        if block.startswith("# "):
            title = block[2:].strip()
            continue
        if block.startswith("## "):
            n_head += 1
            body.append(f'<h3>■ {inline(block[3:].strip())}</h3>')
            continue
        if re.fullmatch(r"-{3,}", block):
            body.append("<hr>")
            continue
        if block.startswith("【画像"):
            # 画像行＋直後のキャプションは、差し替え位置が一目で分かる枠にする
            lines = block.split("\n")
            img_slots += 1
            cap = "<br>".join(inline(x) for x in lines[1:]) if len(lines) > 1 else ""
            body.append(
                '<div style="border:2px dashed #c0392b;border-radius:6px;padding:14px 16px;'
                'margin:1.6em 0;background:#fff8f7">'
                f'<p style="margin:0 0 .5em;color:#c0392b;font-weight:700">{inline(lines[0])}'
                '　← ここにブログ編集画面で画像をアップロードして差し替える</p>'
                f'<p style="margin:0;font-size:.94em">{cap}</p></div>'
            )
            continue
        body.append("<p>" + "<br>".join(inline(l) for l in block.split("\n")) + "</p>")

    doc = "\n".join(body)

    # 蛍光マーカー（インライン変換後の文字列で突き合わせる）
    hit = 0
    for m in marks:
        conv = inline(m)
        if conv in doc:
            doc = doc.replace(conv, f'<span style="background-color:{GREEN};">{conv}</span>', 1)
            hit += 1
        else:
            print(f"  ⚠️ マーカー未一致（本文に見つからない）: {m[:40]}…", file=sys.stderr)

    label = a.label or os.path.basename(a.draft)
    out = a.out or os.path.join(
        os.path.expanduser("~/outputs/blog-marking"),
        os.path.basename(a.draft).rsplit(".", 1)[0] + "_blog_paste.html",
    )
    os.makedirs(os.path.dirname(out), exist_ok=True)

    img_note = (
        f'<br>本文中に<b style="color:#c0392b">赤い破線の枠が{img_slots}か所</b>あります。'
        "そこはブログ編集画面で画像に差し替えてください（枠ごと消す）。" if img_slots else ""
    )
    io.open(out, "w", encoding="utf-8").write(f"""<meta charset="utf-8"><title>{html.escape(title)}｜ブログ貼り付け用</title>
<style>
body{{font-family:"Hiragino Sans","Yu Gothic",sans-serif;line-height:1.9;max-width:760px;
 margin:0 auto;padding:28px 22px 80px;color:#1c1a17;background:#fff}}
h3{{font-size:1.12em;margin:2.1em 0 .7em;padding-left:.55em;border-left:5px solid {RULE_GREEN}}}
p{{margin:0 0 1.15em}} hr{{margin:2.4em 0;border:0;border-top:1px solid #ddd}}
a{{word-break:break-all}}
#bar{{position:sticky;top:0;background:#f4f2ed;border:1px solid #ddd8cd;border-radius:6px;
 padding:10px 14px;margin-bottom:26px;font-size:12.5px;line-height:1.7}}
</style>
<div id="bar"><b>ブログ貼り付け用（{html.escape(label)}）</b>：この枠の<b>下</b>から最後までを選択してコピーし、ブログの編集画面に貼り付けてください。<b>Notionからはコピーしないでください</b>（緑マーカーが落ち、<code>**</code>が生のまま入ります）。<br>タイトル欄には別途これを入れます → <b>{html.escape(title)}</b><br>見出し {n_head}／緑マーカー {hit}本{img_note}</div>
{doc}
""")
    print(f"✅ {out}")
    print(f"   見出し {n_head}／緑マーカー {hit}/{len(marks)}本／画像枠 {img_slots}")
    return 0 if hit == len(marks) else 1


if __name__ == "__main__":
    sys.exit(main())
