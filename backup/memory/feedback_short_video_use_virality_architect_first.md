---
name: feedback_short_video_use_virality_architect_first
description: ショート動画原稿は最初からshort-video-virality-architectで作る。素朴生成の長尺はNG
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b0bba8ff-ab56-4683-9d90-c90ab7651703
---

ショート動画（TikTok/Shorts/Reels）の原稿は、**最初から `short-video-virality-architect` を使う**。daily-content-generator や素朴な生成で出すと、情報を詰め込みすぎて90秒超・冗長・分かりにくくなり、草川本人からNGが出る（2026-05-27 子ども医療費動画で実際に発生：「急いで読んでも90秒以上、想定が甘い、分かりにくい」と指摘）。

**草川のショート動画基準**：
- 尺は **35〜45秒厳守**（読み上げ実測。日本語ナレーション ≒ 6字/秒 → 40秒で約240字が上限目安）
- **1動画＝1メッセージ**。年表・試算額・制度の細部・数値羅列は完視聴率を削るノイズとしてカット
- 冒頭1.5秒で最強の数字/対比フック。「皆さんこんにちは」型・自己紹介・前置き禁止
- 1.5〜2秒ごとに画/テロップ切替、ループ設計、末尾コメント誘発の問い1つ
- 3バリアント（A数字ショック/B共感/C議論喚起）、各40秒前後

**Why**: ショート動画は完視聴率が命。長い＝即離脱＝アルゴリズム不利。専門エージェントは8軸自己診断（64/80でship）と retention curve 設計を持つ。

**How to apply**: 「ショート動画作って」「動画の原稿」系の依頼、および short-video-create / daily-content-generator のショート動画工程では、セリフ生成の主担当を必ず short-video-virality-architect にする。素朴生成→後で短縮は二度手間（2026-05-27は v1長尺→ファクト精査多数→本人NG→作り直しで往復が膨らんだ）。関連: [[feedback_kusagawa_short_video_script_style]] [[project_short_video_create_system]]
