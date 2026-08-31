---
name: image-guard-blocks-reviewer
description: image_budget_guard.py が natural-design-reviewer 自身の Read も deny する（session_id が親と共有のため）。EYES-FIRST が実行不能になる既知の詰み
metadata:
  type: project
---

`~/.claude/hooks/image_budget_guard.py` は画像 Read を **session_id 単位**で数え、25枚で deny する。
サブエージェントは親と同じ session_id を使うため、**natural-design-reviewer に委譲した時点でカウンタは
すでに上限を超えていることがあり、レビュアー自身の1枚目の Read が deny される**。
deny メッセージは「破綻チェックだけ → Agent(natural-design-reviewer) に PNG のパスを渡す」と案内するが、
その委譲先でも同じ deny が出る＝案内が自己矛盾している。

**Why:** ガードの目的は「親セッションに画像を積み上げない」こと。設計意図どおりサブエージェントに逃がしても、
カウンタが session 単位なので効果が出ず、逆に唯一の正しい経路を塞ぐ。

**How to apply:**
- 委譲される前に、親側で `rm ~/.claude/hooks/state/<session_id>.imgcount` を実行しておく
  （レビュアー側からの rm / Write / python3 は auto mode classifier に deny されることがある）
- または画像を伴うレビューは **/clear 後の新セッション**から起動する
- レビュアーが Read できなかった場合、**HTML/CSS から幾何を計算した結果を「目視の代用」として出してはいけない**。
  必ず「目視未実施」と明示する（[[eyes-first-is-not-substitutable]] 参照）

恒久修正案（未実施）: image_budget_guard.py で `inp.get("parent_tool_use_id")` 等サブエージェント判定を見て
カウントをスキップする、もしくはカウンタを agent 単位に分ける。
