---
name: project-photo-post-skill
description: photo-postスキル（写真＋ひとこと→投稿文・画像・動画の統合1パス）2026-07-05実装
metadata: 
  node_type: memory
  type: project
  originSessionId: 6e8fa7bf-f02d-4dcb-a8ee-2bba653fb18e
---

2026-07-05実装完了。写真1〜3枚＋ひとこと→投稿文（1〜2PF）→SNS投稿画像（1:1＋9:16・実写無加工デザイン合成・テンプレ3種=下帯型/サイドバー型/座布団型）→ショート動画（ffmpeg Ken Burns＋透過見出し＋枠付きフォトカードのエンドカード・**合計10秒以内**9:16無音）を統合1パス生成。確認2回のみ。[[project_spark_skill]]と連携（写真つきの種→PAIRモード橋渡し）。設計正本=~/.claude/skills/photo-post/DESIGN.md。natural-design-reviewerゲート組込済（feedback_design_review_gate_no_skip）。初回実運用フィードバック待ち。

**Why:** 実運用は「画像＋ひらめき/活動記録を一緒に投稿」が基本形のため、文と画像を同じ接地・同じコピー素材から分岐させ、安全ゲート・保存を各1回に統合（燃費60〜80K）。政治家写真のAI生成改変は誤解リスクHIGHのため実写無加工＋デザイン合成方式。
**How to apply:** 写真＋ひとこと投入で提案起動。「画像だけ」で動画スキップ。優良レイアウトはdesign_system「SNSカード」昇格提案。動画エンジン=skills/photo-post/scripts/make_video.sh（-o出力 -eエンドカード -tオーバーレイ 写真1〜3枚）。

**エンドカード仕様（2026-07-05草川指示で確定・2026-07-06改訂）:** スローガンは「声をチカラに」または「ええやん亀山」。句読点付き「声を、チカラに。」は使わない。**方式＝枠付きフォトカード**：拳ポーズ公式写真（assets/kusagawa_portrait_src.jpg・無加工）をライム枠の丸角カードに額装し、上にkicker「亀山市議会議員」＋スローガン、右上に幾何ライムアクセント、カード直下に「草川たくや」＋タグ。テンプレ=templates/video_endcard.html（{{PORTRAIT}}/{{SLOGAN}}/{{TAG}}差込）。サンプル=assets/endcard_sample.png。**白背景の切り抜き（透過ポートレート）は廃止**＝襟と背景が同じ白でGrabCutでも分離破綻・明色除去は肌ハイライト誤除去で顔に穴。旧scripts/cutout_portrait.pyは実験残置で通常不使用。

**尺ルール（2026-07-06草川指示で確定）:** ショート動画は**合計10秒以内**が完視聴の限界（「よほどのクオリティでなければ10秒が限界」）。make_video.shの尺＝写真1枚6.5s/2枚各3.4s/3枚各2.4s＋エンドカード2.5s（実測1枚9.0s/2枚9.3s/3枚9.7s）。
