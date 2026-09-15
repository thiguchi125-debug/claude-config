#!/usr/bin/env python3
"""
ショート動画台本を「規定違反のまま保存する」ことを出口で止める hook。

なぜ必要か（2026-09-03 かめやま健康弁当）:
  check_content_limits.py は 🚨「撮っている理由」欠落（＝憲法・出荷拒否）を
  出していた。にもかかわらず原稿は 60秒のまま「確定版」として drafts/ に保存され、
  引き継ぎメモにも「台本 確定」と書かれた。**チェッカーの出力が出荷を止めていない**。
  さらに尺とカット数は表記ゆれ（0:00.0–0:02.7）で判定そのものがスキップされ、
  「違反2件」としか出ていなかった（同日 checker 側も修正）。

  ルールをmarkdownに書く／人間が目視で拾う、では止まらない。書き込みの瞬間に落とす。

止める対象:
  Write / Edit のうち、保存先が動画台本（ファイル名に 動画・ショート・short-video・
  tiktok・reels・shorts）のもの。違反があれば deny し、違反リストを返す。

素通しする:
  Bash 経由の保存（heredoc 等）は PostToolUse で**警告のみ**（denyできないため）。
  草川承認済みの逸脱は原稿に <!-- FORMAT-EXCEPTION: 尺=NN秒 / 草川承認 ... --> を
  書けば checker 側が例外として通す。
失敗時はすべて素通し（hookのバグで作業を止めない）。
"""
import sys, os, json, importlib.util, re

CHECKER = os.path.expanduser("~/.claude/scripts/check_content_limits.py")
VIDEOISH = ("動画", "ショート", "short-video", "short_video", "tiktok", "reels", "shorts")

def load():
    spec = importlib.util.spec_from_file_location("cc", CHECKER)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

def is_video_path(p):
    b = os.path.basename(p or "").lower()
    return any(k in b for k in VIDEOISH)

def violations(text):
    m = load()
    return [msg for ok, msg in m.check_video(text) if not ok]

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    ev   = data.get("hook_event_name", "")
    tool = data.get("tool_name", "")
    ti   = data.get("tool_input", {}) or {}

    try:
        if ev == "PreToolUse" and tool in ("Write", "Edit"):
            path = ti.get("file_path", "")
            if not is_video_path(path):
                return 0
            if tool == "Write":
                text = ti.get("content", "")
            else:
                if not os.path.exists(path):
                    return 0
                text = open(path, encoding="utf-8").read()
                text = text.replace(ti.get("old_string", ""), ti.get("new_string", ""),
                                    -1 if ti.get("replace_all") else 1)
            bad = violations(text)
            if bad:
                reason = ("ショート動画の規定に違反したまま保存しようとしています。"
                          "**カットを詰めて延命せず、セリフを削って**直してから保存してください。\n\n"
                          + "\n".join("  🚨 " + b for b in bad)
                          + "\n\n規定: 尺35〜50秒・目標45〜50秒・1カット3.0秒以内・カット密度・憲法5構成"
                            "（コールドオープン／撮っている理由／本論1メッセージ／結びの決意／コメント誘発）"
                            "・一文30字以内・セリフ中の数値6個以下。\n"
                            "草川承認済みの逸脱のみ <!-- FORMAT-EXCEPTION: 尺=NN秒 / 草川承認 YYYY-MM-DD / 理由 --> で通せます（自己承認は不可）。")
                print(json.dumps({"hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason}}, ensure_ascii=False))
                return 0

        if ev == "PostToolUse" and tool == "Bash":
            cmd = (ti.get("command") or "")
            cands = set(re.findall(r"[^\s\"'<>|]+\.md", cmd))
            for c in cands:
                p = os.path.expanduser(c.strip("'\""))
                if not is_video_path(p) or not os.path.exists(p):
                    continue
                bad = violations(open(p, encoding="utf-8").read())
                if bad:
                    print(f"[動画台本ゲート] {os.path.basename(p)} に規定違反が残っています："
                          + " / ".join(bad)
                          + "  → 保存済みでも『確定版』として扱わないこと。セリフを削って直す。")
                    return 0
    except Exception:
        return 0
    return 0

if __name__ == "__main__":
    sys.exit(main())
