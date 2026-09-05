---
name: feedback-blog-footer-iken-bako-no-arrow
description: ブログ定型フッターの【ご意見箱】は矢印「→」を使わず、【】の直後に半角スペース1つを置いてURLを書く
metadata:
  type: feedback
---

ブログ定型フッターの投函先表記は **`【ご意見箱】 https://forms.gle/VHfPR93VPCSnNorAA`**。2026-08-31 草川指示で確定。

- **矢印「→」は使わない**（旧表記 `【ご意見箱】→https://...` は廃止）
- **「】」の直後に半角スペース1つ**を置いてURLを続ける
- 以後 `【〇〇】` とURLを並べる箇所は同じ規則（半角スペース1つ・矢印なし）

**Why**: 旧ルールは「→とURLの間にスペースを入れない」だったが、矢印ごと廃止に変更された。テンプレ側に旧ルールが残っていると生成のたびに矢印が復活する。

**How to apply**: 正本は `~/.claude/agents/blog-writer.md` と `~/.claude/agents/blog-writer-normal.md` の2本（実例行とルール行の両方を2026-08-31に修正済み）。過去記事アーカイブ `02_publications/blog/` の旧表記は**公開済みの記録なので直さない**。なお本文中の `→「①」の見出しへ` のような矢印は対象外。

関連 blog-writer(-normal).md 📌節（◆AIインタビュー常設）／[[feedback_copypaste_draft_delivery]]
