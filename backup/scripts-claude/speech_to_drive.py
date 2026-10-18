#!/usr/bin/env python3
"""speech_to_drive.py — vaultの演説原稿md → スマホで読むGoogleドキュメント（2026選挙用）

なぜ2段か: このMacにはPythonから使えるGoogle API認証が無い（yoboはApps Script経由・Sheet専用）。
Drive MCP の create_file は text/html を渡すとGoogleドキュメントに変換してくれるので、
  ① build  … このスクリプトがmdをスマホ用HTMLにし、タイトル・置き場・旧版の移動先をJSONで出す
  ② Claude … Drive MCP create_file(title, textContent=HTML, contentMimeType=text/html, parentId=FOLDER_ID)
             → 旧版があれば update_file(fileId=旧id, parentId=OLD_FOLDER_ID) で「旧版」へ移す（削除・上書きはしない）
  ③ record … 新しいfileIdを台帳に記録し、URLを出力する
という分担にしている。呼び方＝草川「〇〇をスマホに送って」。

使い方:
  python3 ~/.claude/scripts/speech_to_drive.py build  <vaultのmd>  [--all]
  python3 ~/.claude/scripts/speech_to_drive.py record <vaultのmd>  --id <DriveのfileId>
  python3 ~/.claude/scripts/speech_to_drive.py list
--all … 出典表・切り出し候補など裏方の節も含める（既定は 要旨→読み上げ原稿 など本番で見る節だけ）
"""
import argparse, datetime, html, json, os, re, sys

import markdown

FOLDER_ID = "1Rm_mIT3ieiCn8c4zoSlBmbkZuLF0VvP3"       # マイドライブ/🗳2026選挙/01_演説原稿（旧名 2026選挙_演説原稿（スマホ用）・IDは同じ）
OLD_FOLDER_ID = "17zVZK_X2_2HYbYxVL7_tU2qzdRoBznqH"   # 同/旧版
FOLDER_URL = "https://drive.google.com/drive/folders/" + FOLDER_ID
LEDGER = os.path.expanduser("~/.claude/scripts/speech_to_drive_ledger.json")
OUTDIR = os.path.expanduser("~/outputs/speech_to_drive")

# 本番で見ない裏方の節（見出しにこの語があれば既定で外す）
BACKSTAGE_RE = re.compile(r"出典|切り出し|講演由来|動画にする|つながり|ファクト|リスク|チェック|作業メモ|変更点|差分")
GENERIC_STEMS = {"挨拶原稿", "原稿", "演説原稿", "手元メモ", "演説メモ", "本文"}
VER_RE = re.compile(r"[_\-\s]?v(\d+)$", re.I)

BODY_PT, H1_PT, H2_PT, H3_PT = 16, 22, 19, 17
FONT = ""  # 書体はDocs既定（Arial＋日本語フォールバック）。HTMLを軽くするため指定しない


def parse_name(md_path):
    folder = os.path.basename(os.path.dirname(os.path.abspath(md_path)))
    stem = os.path.splitext(os.path.basename(md_path))[0]
    m = VER_RE.search(stem)
    ver = int(m.group(1)) if m else 1
    base = VER_RE.sub("", stem).strip("_ ")
    fm = re.match(r"(\d{4})-(\d{2})-(\d{2})_(.+)", folder)
    date, theme = (f"{fm.group(2)}-{fm.group(3)}", fm.group(4)) if fm else ("", folder)
    parts = [p for p in [date, theme.replace("_", " ")] if p]
    if base and base not in GENERIC_STEMS and base not in theme:
        parts.append(base.replace("_", " "))
    key = f"{folder}/{base}"
    return key, " ".join(parts), ver


def split_sections(text):
    """preamble（最初の##より前）と ## 節のリストに分ける。"""
    chunks = re.split(r"(?m)^(?=## )", text)
    pre, secs = chunks[0], []
    for c in chunks[1:]:
        head = c.splitlines()[0][3:].strip()
        secs.append((head, c))
    return pre, secs


def reorder(text, include_all):
    pre, secs = split_sections(text)
    # preamble: 内部向けの「状態:」行と区切り線を落とす
    pre_lines = [l for l in pre.splitlines() if not re.match(r"\s*(状態|status)\s*[:：]", l)]
    pre = "\n".join(pre_lines).rstrip().rstrip("-").rstrip()
    if not include_all:
        secs = [s for s in secs if not BACKSTAGE_RE.search(s[0])]
    youshi = [s for s in secs if "要旨" in s[0]]
    rest = [s for s in secs if "要旨" not in s[0]]
    body = "\n\n".join(c.rstrip().rstrip("-").rstrip() for _, c in youshi + rest)
    return pre + "\n\n" + body + "\n"


def style_html(h):
    p = f"font-size:{BODY_PT}pt;line-height:1.7;{FONT}"
    h = re.sub(r"<h1>", f'<h1 style="font-size:{H1_PT}pt;{FONT}">', h)
    h = re.sub(r"<h2>", f'<h2 style="font-size:{H2_PT}pt;margin-top:24pt;{FONT}">', h)
    h = re.sub(r"<h3>", f'<h3 style="font-size:{H3_PT}pt;{FONT}">', h)
    h = re.sub(r"<p>", f'<p style="{p}">', h)
    h = re.sub(r"<li>", f'<li style="{p}">', h)
    h = re.sub(r"<(td|th)>", rf'<\1 style="font-size:{BODY_PT - 2}pt;border:1px solid #999;padding:4pt;{FONT}">', h)
    h = h.replace("<table>", '<table style="border-collapse:collapse;">')
    # 演出指示（全角かっこで始まり終わる段落）は灰色で目立たせ過ぎない。文字はそのまま
    h = re.sub(r'(<p style="[^"]*)">(（[^<]*?）)</p>', r'\1color:#777777;">\2</p>', h)
    return h


def plain(text):
    """読み上げ専用の薄い版（2026-10-18草川「スマホだと死ぬほど読みにくいし修正しにくい」）。
    要旨と読み上げ原稿の節だけ。見出し記号・太字・表・（間）などの演出指示を落とした普通の文字。"""
    _, secs = split_sections(text)
    picked = [s for s in secs if "要旨" in s[0]] + [s for s in secs if "読み上げ" in s[0] or "本文" in s[0]]
    if not picked:
        # 会場別など「## 会場名 > ### 読み上げ版」の入れ子構成（2026-10-18 地区演説v3で空になった）
        for head, c in secs:
            for sub in re.split(r"(?m)^(?=### )", c)[1:]:
                if "読み上げ" in sub.splitlines()[0] or "本文" in sub.splitlines()[0]:
                    picked.append(("【" + head + "】", sub))
    out = []
    for head, c in picked:
        out.append(head if head.startswith("【") else ("【要旨】" if "要旨" in head else "【本文】"))
        for l in c.splitlines()[1:]:
            l = l.strip()
            if re.fullmatch(r"-{3,}|（[^（）]*）|\|.*", l) or l.startswith("太字"):
                continue
            l = re.sub(r"\*\*|__|^#+\s*", "", l)
            if l or (out and out[-1]):
                out.append(l)
        out.append("")
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"


def build(md_path, include_all, rich=False):
    text = open(md_path, encoding="utf-8").read()
    key, title_base, ver = parse_name(md_path)
    title = f"{title_base} v{ver}"
    os.makedirs(OUTDIR, exist_ok=True)
    if rich:
        body = markdown.markdown(reorder(text, include_all), extensions=["tables", "nl2br", "sane_lists"])
        doc = (f"<html><head><meta charset='utf-8'><title>{html.escape(title)}</title></head>"
               f'<body style="font-size:{BODY_PT}pt;">'
               f"{style_html(body)}</body></html>")
        out = os.path.join(OUTDIR, re.sub(r"[\\/:\s]+", "_", title) + ".html")
    else:
        doc = plain(text)
        out = os.path.join(OUTDIR, re.sub(r"[\\/:\s]+", "_", title) + ".txt")
    open(out, "w", encoding="utf-8").write(doc)
    mime = "text/html" if rich else "text/plain"
    vault_copy = None
    if not rich:
        # 同じ薄い版をvaultの原稿の隣にも置く（Obsidianで #注記 を入れられるように・2026-10-18草川「注記はobsidianも」）
        stem = os.path.splitext(os.path.abspath(md_path))[0]
        vault_copy = stem + "_読み上げ.md"
        if not os.path.exists(vault_copy):
            open(vault_copy, "w", encoding="utf-8").write(
                f"# {title}（読み上げ版）\n\n直したい行の後ろに #注記 を書く。正本は {os.path.basename(md_path)}\n\n" + doc)
    led = load()
    prev = [e for e in led.get(key, []) if e.get("state") == "current"]
    same = [e for e in led.get(key, []) if e["title"] == title]
    print(json.dumps({
        "title": title, "html_path": out, "html_bytes": len(doc.encode()),
        "parentId": FOLDER_ID, "old_folder_id": OLD_FOLDER_ID,
        "move_to_old": [{"fileId": e["id"], "title": e["title"]} for e in prev],
        "warning": (f"同じ名前 {title} が既にある（{same[0]['url']}）。草川の編集が入っている可能性"
                    "＝上書き・削除しない。版を上げるか、題に「_再送」を付けて別名で作る") if same else None,
        "contentMimeType": mime,
        "vault_copy": vault_copy,
        "next": f"Drive MCP create_file(title, textContent=<html_pathの中身>, contentMimeType='{mime}', parentId) "
                "→ move_to_old を update_file(parentId=old_folder_id) → record --id",
    }, ensure_ascii=False, indent=1))


def load():
    try:
        return json.load(open(LEDGER, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def record(md_path, fid):
    key, title_base, ver = parse_name(md_path)
    led = load()
    for e in led.get(key, []):
        if e.get("state") == "current":
            e["state"] = "old"
    url = f"https://docs.google.com/document/d/{fid}/edit"
    led.setdefault(key, []).append({"title": f"{title_base} v{ver}", "id": fid, "url": url,
                                    "src": os.path.abspath(md_path), "state": "current",
                                    "at": datetime.datetime.now().isoformat(timespec="seconds")})
    json.dump(led, open(LEDGER, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(url)
    print("フォルダ:", FOLDER_URL)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build", "record", "list"])
    ap.add_argument("md", nargs="?")
    ap.add_argument("--id")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--rich", action="store_true", help="見出し・太字付きの旧形式（既定は読み上げ専用の薄い版）")
    a = ap.parse_args()
    if a.cmd == "list":
        for k, es in load().items():
            for e in es:
                print(f"[{e['state']}] {e['title']}  {e['url']}")
        print("フォルダ:", FOLDER_URL)
        return
    if not a.md or not os.path.isfile(a.md):
        sys.exit("mdのパスを指定してください")
    if a.cmd == "build":
        build(a.md, a.all, a.rich)
    else:
        if not a.id:
            sys.exit("--id <fileId> が必要")
        record(a.md, a.id)


if __name__ == "__main__":
    main()
