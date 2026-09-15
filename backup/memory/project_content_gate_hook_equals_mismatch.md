---
name: project-content-gate-hook-equals-mismatch
description: Notion保存フックとgate.pyのnorm()は別実装。2026-09-16に「=」の落とし忘れで発信物が誤denyされ、草川承認のうえ修理済み
metadata: 
  node_type: memory
  type: project
  originSessionId: 68833bbc-6d91-47eb-874b-4fa6fb0d6cd4
  modified: 2026-09-15T23:50:39.388Z
---

2026-09-16発覚・**同日修理済み（草川承認）**。安全ゲートの本体なので勝手に直さず、1問で承認を取ってから直した。

## 症状
安全ゲート2段＋`gate.py --pass` を通した完成稿でも、Notion書込フック `~/.claude/hooks/content_safety_gate.py` が「承認済み原稿に無い」と誤deny。シャープAIサーバーブログ（2026-09-16）のNotion保存がこれで止まった。SNSは通った。

## 原因（実測で確認済み）
- `~/.claude/scripts/gate.py:43` … `re.sub(r"[*\`>#|=]", "", t)`（`=` を落とす＝Obsidianの `==蛍光マーカー==` 対策と明記）
- `~/.claude/hooks/content_safety_gate.py:102` … `re.sub(r"[*\`>#|]", "", t)`（**`=` が無い**）
両者の `norm()` がずれるため、本文の「＝」（NFKCで半角化）やブログ定型フッターのThreads URL末尾 `?igshid=...==` を含む行だけが不一致になる。

## 修理（2026-09-16）
フック102行目を `re.sub(r"[*\`>#|=]", "", t)` に。控え＝`content_safety_gate.py.bak-20260916`。両者の `norm()` が同一結果になることを実測（`gp.norm(t)==h.norm(t)` True）→ブログのNotion保存が通った。

**Why:** ゲート通過済みなのに保存だけ静かに落ちる。SNSは通ってブログだけ落ちるので気づきにくい。**norm()がgate.pyとフックの2箇所に別実装**なのが根。片方を変えたらもう片方も直す。
**How to apply:** 同症状（fact/risk通過済みなのにNotionがdeny）を見たら2つの `norm()` の差分を先に見る。安全ゲート本体の変更は草川に1問で承認を取ってから。[[feedback_maintenance_weekly_window]]
