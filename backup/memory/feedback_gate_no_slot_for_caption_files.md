---
name: feedback-gate-no-slot-for-caption-files
description: ショート動画の「キャプション」は台本でもブログでもなく、check_content_limits.pyの型判定に枠が無かった（2026-09-04に追加）
metadata:
  type: feedback
---

ショート動画のキャプション（投稿文）ファイルは、`check_content_limits.py` の型判定で必ず落ちていた。
ファイル名に `tiktok`／`shorts`／`reels`／`動画`／`video` が入れば **video（台本）** と判定されて
「尺・カット表・結びの決意・コメント誘発CTA」を要求され、入っていなければ **blog** に落ちて
「冒頭の名乗り・定型フッター・5段構成」を要求される。どちらでも通らない二択だった。

**Why:** キャプションは台本でもブログでもない第3の発信物なのに、型判定がファイル名の二分岐しか持っていなかった。
2026-09-04の周産期セッションで2回止まった（Write時は `short_video_limits_gate.py` がdeny、リネーム後は `gate.py` が違反3件）。
推奨投稿時刻「21:00〜22:00」をタイムコードとして拾って「尺 1320秒」と出る偽陽性まで発生する。

**How to apply:** ファイル名を `caption_` で始めるか「キャプション」を含めれば、SNS規定で検査される
（2026-09-04に `check_content_limits.py` へ追加。`INTERNAL_NAME_HINTS` の直後、SNS判定の前に挿入）。
ただし**見出しが `## TikTok` 形式でないとPF別の字数チェックは1件も効かず、違反0件でも実質ノーチェック**になる。
キャプションを作るときは見出しをPF名だけにするか、機械チェックに頼らず [[feedback_safety_gates_before_notion_save]] の
2ゲート（fact-checker／risk-reviewer）で担保すること。関連＝[[feedback_gate_kind_of_by_filename]]
