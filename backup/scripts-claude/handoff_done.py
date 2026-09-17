#!/usr/bin/env python3
"""kugiri「終了」モード: 終わった案件の引き継ぎメモを archive/_done/ へ退避する。

使い方:
  python3 handoff_done.py <案件キーワード> [<キーワード2> ...]        # 候補を表示するだけ
  python3 handoff_done.py <案件キーワード> ... --apply                # 実際に移動

キーワードはファイル名の部分一致（OR）。同じ案件でも名前が揺れる
（例: アイリス町横断歩道 / アイリス町横断歩道_請願要望）ので部分一致で拾う。
削除はしない（即rm禁止ルール）。_done/ は SessionStart フックの注入対象外。
テストは KUGIRI_HANDOFF_DIR にダミーディレクトリを渡して行う。
"""
import glob, os, shutil, sys

DIR = os.environ.get("KUGIRI_HANDOFF_DIR") or os.path.expanduser("~/.claude/handoff/archive")


def main():
    args = [a for a in sys.argv[1:] if a != "--apply"]
    apply = "--apply" in sys.argv
    if not args:
        print(__doc__)
        sys.exit(1)
    hits = sorted(p for p in glob.glob(os.path.join(DIR, "*.md"))
                  if any(k in os.path.basename(p) for k in args))
    if not hits:
        print("該当なし: " + " / ".join(args))
        return
    done = os.path.join(DIR, "_done")
    for p in hits:
        print(("移動 " if apply else "候補 ") + os.path.basename(p))
        if apply:
            os.makedirs(done, exist_ok=True)
            shutil.move(p, os.path.join(done, os.path.basename(p)))
    if not apply:
        print("（--apply で _done/ へ移動）")


if __name__ == "__main__":
    main()
