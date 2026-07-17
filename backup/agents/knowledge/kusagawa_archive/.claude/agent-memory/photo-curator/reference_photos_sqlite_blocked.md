---
name: photos-sqlite-blocked
description: Photos.sqlite への sqlite3/cp アクセスが権限クラシファイアにブロックされる。Photos.app顔DB検索が使えないときの扱い
metadata:
  type: reference
---

`~/Pictures/Photos Library.photoslibrary/database/Photos.sqlite` への `cp` および `sqlite3 "file:...?immutable=1"` は、Claude Code の auto mode classifier にブロックされる（2026-07-17 確認）。ZPERSON=18 の顔DB検索という photo-curator の第一機能が丸ごと使えない状態になる。

**How to apply:**
- ブロックされたら回避を試みず、草川に「Photos.app DB検索には Bash permission rule の追加が必要」と伝えて判断を仰ぐ。
- その間の代替は Drive `📷写真ストック`（[[drive-photo-stock-is-vertical-selfies]]）と Drive 全域の find。ただしストックは十数枚規模なので、Photos.app が使えない状態は「探索範囲が2桁小さい」と明示して報告する。
- 2026-07 以降メイン機が Pixel に移行済のため Photos.app は旧写真中心。新しい写真の欠落とは別問題である点に注意。
