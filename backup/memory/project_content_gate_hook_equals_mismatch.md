---
name: project-content-gate-hook-equals-mismatch
description: Notion保存フックとgate.pyの正規化がずれていて「＝」やURL末尾「==」を含む発信物が誤denyされる。2026-09-16に草川は「後で判断」を選択・未修理
metadata: 
  node_type: memory
  type: project
  originSessionId: 68833bbc-6d91-47eb-874b-4fa6fb0d6cd4
  modified: 2026-09-15T23:27:10.741Z
---

2026-09-16発覚・**未修理（草川判断待ち）**。安全ゲートの本体に関わるため勝手に直さない。

## 症状
安全ゲート2段＋`gate.py --pass` を通した完成稿でも、Notion書込フック `~/.claude/hooks/content_safety_gate.py` が「承認済み原稿に無い」と誤deny。シャープAIサーバーブログ（2026-09-16）のNotion保存がこれで止まった。SNSは通った。

## 原因（実測で確認済み）
- `~/.claude/scripts/gate.py:43` … `re.sub(r"[*\`>#|=]", "", t)`（`=` を落とす＝Obsidianの `==蛍光マーカー==` 対策と明記）
- `~/.claude/hooks/content_safety_gate.py:102` … `re.sub(r"[*\`>#|]", "", t)`（**`=` が無い**）
両者の `norm()` がずれるため、本文の「＝」（NFKCで半角化）やブログ定型フッターのThreads URL末尾 `?igshid=...==` を含む行だけが不一致になる。

## 直すなら
フック102行目に `=` を足して gate.py と揃える1文字。ゲートの強度は変わらず、誤判定だけが消える。実施前に `.bak-<日付>` を取る。

## 回避策（フックを触らない場合）
ブログ本文から「＝」を消してもフッターのURL末尾 `==` が残るので回避できない。Obsidianの完成版＋貼り付け用HTMLで運用し、Notionのブログ保存だけ見送る。

**Why:** 発信フローの最後の保存工程が塞がる。SNSは通るのでブログだけ静かに落ちる。
**How to apply:** 同じ症状（fact/risk通過済みなのにNotionがdeny）を見たらここを疑う。修理は草川の承認後。[[feedback_maintenance_weekly_window]]
