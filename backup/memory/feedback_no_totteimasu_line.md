---
name: feedback_no_totteimasu_line
description: ショート動画で「だから、撮っています」型の一言は今後一切書かない。憲法の「撮っている理由」ブロックごと廃止
metadata:
  type: feedback
---

ショート動画のセリフに「**だから、撮っています**」「最近この声が本当に多いんです」といった**「撮っている理由」の一言を書かない**。2026-09-03 草川指示「だから撮っていますの一言は今後も一切不要」。

**Why**: この一言は元々「憲法5構成」の②として**必須**（無いと8軸満点でも出荷拒否）とされていた。だが実際には、撮る理由をわざわざ口に出すのは冗長で、尺35〜45秒のうち2秒前後を食う。本人が不要と判断した。

**How to apply**:
- 構成は「①コールドオープンのフック → ②名乗り → ③本論1メッセージ → ④結びの決意 → ⑤コメント誘発」。名乗りから本論へ直行する。
- 機械判定 `check_content_limits.py` は 2026-09-03 に**必須チェック→禁止フレーズ検出へ反転**済み。セリフに「撮っています／撮っている／撮影しています」が入ると違反として出る。
- 仕様も同日修正済み：`short-video-virality-architect.md`（憲法を4構成に・出荷拒否対象から除外）／`short-video-create/SKILL.md`。
- **注意**：過去の台本には②が入っている。流用するときは必ず落とす。

関連: [[feedback_short_video_use_virality_architect_first]] [[feedback_read_agent_spec_before_writing]]（スタイル13項目＝short-video-virality-architect.md 📌節）
