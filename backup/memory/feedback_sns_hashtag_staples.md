---
name: feedback_sns_hashtag_staples
description: SNS投稿のハッシュタグには
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ec62ed91-56d9-45b7-bd08-038b09c591b3
---

草川のSNS投稿（X・Instagram等、ハッシュタグを付けるPF）では、ブランディング用の定番タグを必ず含める。

**必須2つ:** `#草川たくや`（本人名・指名検索/個人ブランド）／`#ええやん亀山`（亀山ポジティブPRの定番スローガンタグ）。

**例外（2026-09-02 草川確認）:** **Threadsには付けない**（本人名タグも含めて一切）。sns-content-creator.md が「Threadsはハッシュタグ文化が薄く、付けてもリーチに寄与しない」と規定しており、`check_content_limits.py` も Threads のタグを違反として落とす。LINEも従来どおりタグなし。

**テーマ別タグ（その投稿の内容に合わせて2〜3個）と組み合わせる。** 例（温泉で産後ケア）: `#亀山市 #産後ケア #子育て #草川たくや #ええやん亀山`。

**How to apply:** sns-content-creator等でハッシュタグを生成・確定する際、テーマタグに加えて必ず `#草川たくや` `#ええやん亀山` を末尾に付ける。Xはリンクをリプライに回す運用だがハッシュタグは本文末でOK。

Why: 草川指示（2026-06-28）。**How to apply:** 出力チェックで2タグの有無を確認。
関連: [[feedback_x_post_lean_one_message]] [[feedback_x_no_char_limit]]
