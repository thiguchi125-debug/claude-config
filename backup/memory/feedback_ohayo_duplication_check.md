---
name: ohayo-duplication-check
description: ohayoの朝のブリーフィングで「既発信テーマ」「既完了タスク」を重複表示しない、投稿管理DB横断突合チェックを必須化（v2.4）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 37ff2ffc-48be-4b94-9f41-ec718bf69e28
---

ohayoは朝のニュース解説／街頭演説テーマ／ブログ・SNS発信テーマ提案／タスク期限超過判定の前に、必ず 📣SNS投稿管理DB（collection://1bd98deb-624f-402c-aeb3-bdaa4782b389）の直近14日「完了」テーマを取得して、重複検出する。

**Why:** 2026-05-12 朝、ohayoがコミバス無料化（5/9発信済）・特別教室エアコン59室（5/4-6発信済）・部活動地域移行（4/30発信済）を新規テーマとして再提案し、さらに「ショート動画アップ」期限超過タスクが実態は完了済なのに残り続けた。データ取得は横展開しているのにデータ同士の整合性チェックが抜けていた。草川直接指摘「データをもとに意味のある朝のダッシュボード／既発信内容は避ける」。

**How to apply:**
- §3-PRE-B 投稿管理DB横断突合チェックを §3-PRE-A の直後に必須実行
  - filter: 更新日>=今日-14日 AND ステータス="完了" page_size:30
  - 内部メモ `recent_completed_posts[]` に保持
- §3-1c タスク実態整合化: タスクDB「ショート動画/ブログ/SNS」inboxは recent_completed_posts と突合→ヒット時は「⚙️実質完了候補（Done推奨）」ブロックへ移動
- §3-6 発信テーマ提案フィルタ: 街頭演説A/B/C・ブログ深掘り/ノーマル・SNS即時の各候補は類似度判定→既発信は除外 or [既発信+新規角度]タグ＋既発信URL併記
- §3-0 ニュース解説: 同テーマが既発信なら見出し末尾に [📝既発信] マーカー＋URL併記
- §3-X 過去発言連動: grep ヒット後に既ブログ発信URLを併記→「既深掘り済み」or「未深掘り」を判定
- 中期戦略タスク（期限>30日先・継続性語感）は「📌進行中マスタ」ブロックへ分離（超過扱いしない）

**関連:** [[feedback_news_briefing_hallucination_guard]] / [[feedback_ohayo_task_3block_display]] / [[feedback_3db_view_url_correction_v2]]
