---
name: feedback-read-playbook-not-past-output
description: 制作物を作らせる前に正本のプレイブックを読む。過去の完成品1枚を見よう見まねで指示すると規範を丸ごと外す
metadata:
  type: feedback
---

2026-09-04、周産期ブログのアイキャッチで、正本 `content-pipeline/references/visual-assets-playbook.md` を読まずに、
過去の完成品（`thumbnails/2026-08-31_JC稲刈り/eyecatch.html`）を「参考にして」とだけ指示した。結果、規範をほぼ全部外した。

- サイズ **1600×900（16:9）** が正 → 1200×630（2026-08-31に改訂された旧規格）で作らせた
- **安全域＝中央800×800／左右各400pxは1:1クロップで消える捨て代** → 左に見出し・右にカードの左右構成にした（Yahoo!等で右半分が消える）
- 主見出しの文字高は **画像高の10〜14%（90〜126px）** → 64px
- **下端12%に文字を置かない**（Xのチップが重なる） → 署名を右下に置いた
- 確定前に `feed_preview.py still` → **feed-visual-reviewer でPASS必須** → 通していない

**Why:** 完成品には「なぜそうなっているか」も「いつ改訂されたか」も書かれていない。
過去作の模倣は、改訂前の版を再生産する。草川の評価は「全く使えない」だった。

**How to apply:** 制作系エージェントに投げる前に、**正本のプレイブック／SKILL.mdを自分でReadする**。
参照すべき正本＝サムネ・ショート動画は `content-pipeline/references/visual-assets-playbook.md`、
印刷物は `design_system/`。過去の完成品は「正本を読んだうえで」型を確認するために見る。
関連＝[[feedback_read_agent_spec_before_writing]]／[[feedback_design_reference_library_first]]／[[feedback_original_size_pass_is_half_a_pass]]
