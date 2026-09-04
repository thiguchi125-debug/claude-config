---
name: feedback_no_emoji_ai_smell
description: 印刷物・発信物で絵文字を使わない（AI臭いため）。アイコンはCSSのライムバー/角マーカー等の文字組みで代替
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ff9920af-ba3d-47a6-9949-9e1432ee8f36
---

チラシ・印刷物・SNS・ブログ等の発信物で **絵文字（📅📱📝🔔▶ 等）を使わない**。草川から「絵文字を使うのがAI臭いので絶対にやめて」と直接指示（2026-06-17 YouTubeライブ市政報告会A4チラシ制作中）。

**Why:** 絵文字は一発でAI生成物っぽさ＝安っぽさが出る。プロのデザイン・編集物では絵文字でセクション見出しや箇条書きを飾らない。

**How to apply:**
- セクション見出しの装飾 → ライムの細い縦バー（CSS `::before` の background ブロック、絵文字ではない）で代替
- 箇条書きマーカー → ライムの小さな角マーカー（CSS box）／中黒「・」／ダッシュ「—」で代替
- ラベル（日時など）→ ダークグリーンのピル（背景色＋角丸の文字ラベル）で代替
- 制作後は絵文字コードポイント（0x1F300〜0x1FAFF / 0x2600〜0x27BF / 0x25B6等）が残っていないかコードで検査してから確定
- print-designer / blog-writer / sns-content-creator 等すべての発信経路に適用

関連: DESIGN_RULES.md §1（AI製SaaS LP風NG）（AI製SaaS LP風NG）／[[feedback_no_abstract_poetic_phrases]]（情緒系メタファーNG）

**スライド資料（市政報告会等）も対象。** チープに見えるため絵文字は一切使わない（2026-06-13草川指示。旧 feedback_no_emoji_in_slides を統合）。
