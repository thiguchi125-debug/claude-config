#!/usr/bin/env python3
"""PreToolUse(Read): 中身が変わっていない画像/PDFの2度読みを止める。

2026-08実測: 8月の画像Read 602件のうち226件(38%)が同一ファイルの再読込。
画像1枚は約1.5Kトークンを消費し、しかも一度入った画像は文脈から消えないため、
以降の全呼び出しでそのコストを払い続ける。
mtime+sizeが同一＝中身が変わっていない場合だけ拒否する。
再レンダ後（mtimeが動いた）の読み直しは正当なので通す。
"""
import json, os, sys

EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".pdf", ".heic", ".bmp", ".tiff")
STATE_DIR = os.path.expanduser("~/.claude/hooks/state")


def main():
    try:
        inp = json.load(sys.stdin)
    except ValueError:
        return
    if inp.get("tool_name") != "Read":
        return
    path = (inp.get("tool_input") or {}).get("file_path") or ""
    if not path.lower().endswith(EXT):
        return
    try:
        st = os.stat(path)
    except OSError:
        return
    sig = f"{int(st.st_mtime)}:{st.st_size}"

    sid = inp.get("session_id") or "unknown"
    os.makedirs(STATE_DIR, exist_ok=True)
    sf = os.path.join(STATE_DIR, f"{sid}.imgs")
    try:
        seen = json.load(open(sf))
    except (OSError, ValueError):
        seen = {}

    if seen.get(path) == sig:
        json.dump({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"この画像はこのセッションで既に読み込み済みで、以後ファイルは変更されていない"
                f"（{os.path.basename(path)}）。同じ画像を2度読むと約1.5Kトークンを二重に消費し、"
                "以降の全ツール呼び出しでその分を払い続ける。既に見た内容をそのまま使うこと。"
                "作り直した版を確認したいなら、先に再レンダしてから読むこと。"
            ),
        }}, sys.stdout)
        return

    seen[path] = sig
    try:
        with open(sf, "w") as f:
            json.dump(seen, f)
    except OSError:
        pass
    prune(STATE_DIR)


def prune(d, days=14):
    """終了済みセッションの状態ファイルを溜めない。"""
    import time
    cutoff = time.time() - days * 86400
    try:
        names = os.listdir(d)
    except OSError:
        return
    for n in names:
        p = os.path.join(d, n)
        try:
            if os.path.getmtime(p) < cutoff:
                os.remove(p)
        except OSError:
            pass


if __name__ == "__main__":
    main()
